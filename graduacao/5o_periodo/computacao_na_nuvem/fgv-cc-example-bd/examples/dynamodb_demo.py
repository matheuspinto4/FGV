"""
dynamodb_demo.py — Amazon DynamoDB Demonstration
Cloud Computing course  |  FGV EMAp

Lifecycle:
  1. allocate   — create table (PAY_PER_REQUEST) with two GSIs (global secundary indexes)
  2. populate   — batch_writer: 100 000 items
  3. patterns   — 8 access patterns illustrating different read/write APIs
  4. experiment — four experiments comparing cost and latency of API choices:
                    A. Query vs Scan (same result, very different cost)
                    B. Eventually consistent vs strongly consistent reads
                    C. BatchGetItem vs individual GetItem
                    D. GSI Query vs Scan for the same logical query
  5. destroy    — delete table

Data model — sensor events:
  Table: demo-events
    PK  device_id  (String)  e.g. "DEVICE#0042"
    SK  event_id   (String)  e.g. "20240615T1402#a3f9b21c"  ← timestamp-prefixed

  GSI 1: gsi-type
    PK  event_type  (String)  e.g. "temperature", "motion"
    SK  event_id    (String)
    Projection: ALL
    → Query all events of a given type across all devices

  GSI 2: gsi-status
    PK  status    (String)   e.g. "ok", "alert", "offline"
    SK  event_id  (String)
    Projection: KEYS_ONLY   ← cheaper; sufficient for counting / key lookup
    → Count or retrieve keys of events in a given status

Design note:
  The sort key is timestamp-prefixed so lexicographic ordering gives us
  chronological ordering, and SK range queries (begins_with, between)
  efficiently slice events by time — without a GSI.

Usage:
  python dynamodb_demo.py                          # full lifecycle
  python dynamodb_demo.py --step allocate
  python dynamodb_demo.py --step populate
  python dynamodb_demo.py --step patterns
  python dynamodb_demo.py --step experiment
  python dynamodb_demo.py --step destroy
"""

import argparse
import random
import time
import uuid
from datetime import datetime, timedelta
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError


# ── Configuration ──────────────────────────────────────────────────────────────
REGION     = "us-east-1"
TABLE_NAME = "demo-events"
GSI_TYPE   = "gsi-type"
GSI_STATUS = "gsi-status"

N_DEVICES  = 500
N_ITEMS    = 100_000

DEVICE_IDS   = [f"DEVICE#{i:04d}" for i in range(1, N_DEVICES + 1)]
EVENT_TYPES  = ["temperature", "humidity", "motion", "pressure", "light",
                "vibration", "smoke", "door", "power", "network"]
STATUSES     = ["ok", "alert", "offline", "degraded"]
LOCATIONS    = ["floor-1", "floor-2", "floor-3", "warehouse", "lobby",
                "server-room", "roof", "parking", "lab", "cafeteria"]


# ─────────────────────────────────────────────────────────────────────────────
# 1. ALLOCATION
# ─────────────────────────────────────────────────────────────────────────────

def get_resource_and_client():
    """
    Returns both the high-level Resource and the low-level Client.

    Resource API  (ddb_resource.Table(...).put_item, .query, .scan, …)
      — Python-native types (int, str, Decimal), cleaner interface
      — batch_writer handles 25-item flush and UnprocessedItems retry

    Client API  (ddb_client.batch_get_item, .transact_get_items, …)
      — DynamoDB wire types required: {"S": "value"}, {"N": "42"}
      — Needed for operations not exposed on the Resource (e.g. batch_get_item
        across multiple tables, transact_write_items)
    """
    session = boto3.Session(region_name=REGION)
    return session.resource("dynamodb"), session.client("dynamodb")


def create_table(ddb):
    """
    Creates the events table with PAY_PER_REQUEST billing (on-demand).

    On-demand mode: AWS scales read/write capacity automatically; you pay per
    request. No capacity planning required, ideal for unpredictable workloads.
    Provisioned mode is cheaper for steady, predictable throughput.

    GSIs must be defined at table creation time. Adding a GSI later triggers
    a full backfill (table is not locked, but there is a cost and delay).

    AttributeDefinitions must include ONLY attributes used as PK or SK of the
    table or a GSI. Non-key attributes are schema-free; no declaration needed.
    """
    print(f"[DDB] Creating table '{TABLE_NAME}' ...")
    try:
        table = ddb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "device_id", "KeyType": "HASH"},
                {"AttributeName": "event_id",  "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "device_id",   "AttributeType": "S"},
                {"AttributeName": "event_id",    "AttributeType": "S"},
                {"AttributeName": "event_type",  "AttributeType": "S"},
                {"AttributeName": "status",      "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": GSI_TYPE,
                    "KeySchema": [
                        {"AttributeName": "event_type", "KeyType": "HASH"},
                        {"AttributeName": "event_id",   "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                },
                {
                    "IndexName": GSI_STATUS,
                    "KeySchema": [
                        {"AttributeName": "status",   "KeyType": "HASH"},
                        {"AttributeName": "event_id", "KeyType": "RANGE"},
                    ],
                    # KEYS_ONLY: the GSI stores only PK, SK, and index key
                    # attributes. Sufficient for counting or fetching keys
                    # for a follow-up GetItem. Cheaper to maintain and query.
                    "Projection": {"ProjectionType": "KEYS_ONLY"},
                },
            ],
            BillingMode="PAY_PER_REQUEST",
            Tags=[{"Key": "purpose", "Value": "dynamodb-demo"}],
        )
        print("[DDB] Waiting for ACTIVE ...")
        table.wait_until_exists()
        print(f"[DDB] Table active  ARN: {table.table_arn}")
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ResourceInUseException":
            print("[DDB] Table already exists, reusing.")
            table = ddb.Table(TABLE_NAME)
        else:
            raise
    return table


# ─────────────────────────────────────────────────────────────────────────────
# 2. POPULATE
# ─────────────────────────────────────────────────────────────────────────────

def populate(table, n=N_ITEMS):
    """
    Inserts items using batch_writer.

    batch_writer behaviour:
      - Buffers put_item / delete_item calls.
      - Flushes automatically in 25-item batches (BatchWriteItem API limit).
      - Retries UnprocessedItems transparently with exponential back-off.
      - A single context manager handles everything; no manual pagination.

    Important: DynamoDB rejects Python float. Use Decimal(str(value)) for
    all numeric attributes that are not integers.
    """
    print(f"[DDB] Inserting {n:,} items via batch_writer ...")
    base_ts = datetime(2024, 1, 1)
    t0      = time.perf_counter()

    with table.batch_writer() as batch:
        for i in range(n):
            ts       = base_ts + timedelta(
                days=random.randint(0, 1500),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59),
            )
            # SK is timestamp-prefixed: lexicographic = chronological.
            # Ex: begins_with("20240615") returns all events for a device on that day.
            event_id = f"{ts.strftime('%Y%m%dT%H%M')}#{uuid.uuid4().hex[:8]}"
            batch.put_item(Item={
                "device_id":   random.choice(DEVICE_IDS),
                "event_id":    event_id,
                "event_type":  random.choice(EVENT_TYPES),
                "status":      random.choice(STATUSES),
                "location":    random.choice(LOCATIONS),
                "value":       Decimal(str(round(random.uniform(-10.0, 100.0), 2))),
                "unit":        random.choice(["°C", "%", "hPa", "lux", "m/s²"]),
                "firmware":    f"v{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,9)}",
                "recorded_at": ts.isoformat(),
            })
            if (i + 1) % 20_000 == 0:
                elapsed = time.perf_counter() - t0
                print(f"  {i + 1:,}/{n:,}  ({elapsed:.1f}s, {(i + 1) / elapsed:,.0f} items/s)")

    elapsed = time.perf_counter() - t0
    print(f"[DDB] Done: {n:,} items in {elapsed:.1f}s  ({n / elapsed:,.0f} items/s)")


# ─────────────────────────────────────────────────────────────────────────────
# 3. ACCESS PATTERNS
# ─────────────────────────────────────────────────────────────────────────────

def demo_access_patterns(table, ddb_client):
    """
    Eight access patterns demonstrating the DynamoDB API surface.

    Core design principle: in DynamoDB, the data model must be designed around
    the access patterns. Unlike relational databases, you cannot write arbitrary
    queries against any attribute without a GSI or a full Scan (and its cost).
    """
    print("\n── Access Patterns " + "─" * 46)

    # Fetch a few real items to use as seeds in later patterns
    seed = table.query(
        KeyConditionExpression=Key("device_id").eq("DEVICE#0001"),
        Limit=10,
    )["Items"]
    sample_item = seed[0]
    sample_key  = {"device_id": sample_item["device_id"],
                   "event_id":  sample_item["event_id"]}
    sample_type = sample_item["event_type"]

    # ── P1: GetItem — O(1) point lookup ─────────────────────────────────────
    # Requires the full primary key (PK + SK).
    # Most efficient read: exactly one partition, one item.
    print("\n[P1] GetItem — single item by full primary key (O(1)):")
    t0   = time.perf_counter()
    resp = table.get_item(Key=sample_key, ConsistentRead=True)
    ms   = (time.perf_counter() - t0) * 1000
    item = resp["Item"]
    print(f"     device={item['device_id']}  event_id={item['event_id']}")
    print(f"     type={item['event_type']}  status={item['status']}  ({ms:.1f} ms)")

    # ── P2: Query by partition key (all events for one device) ───────────────
    # Reads only the partition belonging to this device.
    # ScannedCount == Count when no FilterExpression is applied.
    print("\n[P2] Query — all events for DEVICE#0001:")
    t0   = time.perf_counter()
    resp = table.query(KeyConditionExpression=Key("device_id").eq("DEVICE#0001"))
    ms   = (time.perf_counter() - t0) * 1000
    print(f"     Count={resp['Count']:,}  ScannedCount={resp['ScannedCount']:,}  ({ms:.1f} ms)")
    paginated = "LastEvaluatedKey" in resp
    print(f"     {'⚠ First page only — use ExclusiveStartKey for pagination' if paginated else '✓ All results fit in one page'}")

    # ── P3: Query with SK range (time window) ───────────────────────────────
    # Because event_id starts with YYYYMMDDTHHMM, between() on the SK
    # efficiently retrieves events within a time window — no GSI needed.
    print("\n[P3] Query + SK range — DEVICE#0001 events in June 2024:")
    t0   = time.perf_counter()
    resp = table.query(
        KeyConditionExpression=(
            Key("device_id").eq("DEVICE#0001") &
            Key("event_id").between("20240601", "20240701")
        ),
    )
    ms = (time.perf_counter() - t0) * 1000
    print(f"     Count={resp['Count']:,}  ({ms:.1f} ms)")

    # ── P4: Query via GSI (by event type) ───────────────────────────────────
    # Without gsi-type, finding all "temperature" events would require a Scan.
    # The GSI maintains a separate index keyed by event_type.
    print(f"\n[P4] GSI Query — all '{sample_type}' events (gsi-type):")
    t0   = time.perf_counter()
    resp = table.query(
        IndexName=GSI_TYPE,
        KeyConditionExpression=Key("event_type").eq(sample_type),
        Limit=200,
    )
    ms = (time.perf_counter() - t0) * 1000
    print(f"     Count (first page)={resp['Count']:,}  ({ms:.1f} ms)")

    # ── P5: Count via GSI (KEYS_ONLY projection) ────────────────────────────
    # gsi-status projects only keys → cheaper reads, lower storage.
    # Select="COUNT" avoids returning any attribute data — pure count.
    print("\n[P5] GSI Count — 'alert' events (gsi-status, KEYS_ONLY, paginated):")
    count, kwargs = 0, {
        "IndexName": GSI_STATUS,
        "KeyConditionExpression": Key("status").eq("alert"),
        "Select": "COUNT",
    }
    t0 = time.perf_counter()
    while True:
        resp   = table.query(**kwargs)
        count += resp["Count"]
        if "LastEvaluatedKey" not in resp:
            break
        kwargs["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
    ms = (time.perf_counter() - t0) * 1000
    print(f"     Total alert events = {count:,}  ({ms:.1f} ms)  [no table Scan]")

    # ── P6: Scan + FilterExpression ─────────────────────────────────────────
    # FilterExpression is applied AFTER DynamoDB reads every item.
    # Cost = full table scan regardless of how many items match.
    # ScannedCount >> Count reveals the waste.
    print("\n[P6] Scan + FilterExpression — 'alert' events (⚠ reads full table):")
    count, scanned, kwargs = 0, 0, {
        "FilterExpression": Attr("status").eq("alert"),
        "Select": "COUNT",
    }
    t0 = time.perf_counter()
    while True:
        resp     = table.scan(**kwargs)
        count   += resp["Count"]
        scanned += resp["ScannedCount"]
        if "LastEvaluatedKey" not in resp:
            break
        kwargs["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
    ms = (time.perf_counter() - t0) * 1000
    print(f"     Count={count:,}  ScannedCount={scanned:,}  ({ms:.1f} ms)")
    print(f"     ⚠ Read {scanned:,} items to match {count:,} ({scanned // max(count, 1)}× overhead vs GSI)")

    # ── P7: BatchGetItem — multiple items in one round trip ─────────────────
    # Up to 100 items per call, optionally across multiple tables.
    # UnprocessedKeys in the response must be retried (handled manually here).
    print("\n[P7] BatchGetItem — 20 specific items in a single API call:")
    keys_to_fetch = []
    for dev_num in range(1, 6):
        page = table.query(
            KeyConditionExpression=Key("device_id").eq(f"DEVICE#{dev_num:04d}"),
            Limit=4,
        )
        keys_to_fetch.extend([
            {"device_id": {"S": i["device_id"]}, "event_id": {"S": i["event_id"]}}
            for i in page["Items"]
        ])

    t0   = time.perf_counter()
    resp = ddb_client.batch_get_item(
        RequestItems={TABLE_NAME: {"Keys": keys_to_fetch[:20]}}
    )
    ms        = (time.perf_counter() - t0) * 1000
    retrieved = len(resp["Responses"].get(TABLE_NAME, []))
    unproc    = len(resp.get("UnprocessedKeys", {}).get(TABLE_NAME, {}).get("Keys", []))
    print(f"     Retrieved={retrieved}  UnprocessedKeys={unproc}  ({ms:.1f} ms, 1 round trip)")

    # ── P8: Conditional PutItem — idempotency guard ─────────────────────────
    # attribute_not_exists(event_id): the write succeeds only if the item does
    # not already exist. DynamoDB's mechanism for preventing duplicate inserts
    # without a separate read — atomic and single-item scoped.
    print("\n[P8] Conditional PutItem — attribute_not_exists guard:")
    demo_item = {
        "device_id":   "DEVICE#0001",
        "event_id":    "20240101T0000#DEMO0001",
        "event_type":  "temperature",
        "status":      "ok",
        "location":    "lab",
        "value":       Decimal("21.5"),
        "unit":        "°C",
        "firmware":    "v1.0.0",
        "recorded_at": "2024-01-01T00:00:00",
    }
    for attempt in range(1, 3):
        try:
            table.put_item(
                Item=demo_item,
                ConditionExpression="attribute_not_exists(event_id)",
            )
            print(f"     Attempt {attempt}: ✓ inserted.")
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                print(f"     Attempt {attempt}: ✗ ConditionalCheckFailed — item already exists (guard works).")
            else:
                raise


# ─────────────────────────────────────────────────────────────────────────────
# 4. EXPERIMENTS
# ─────────────────────────────────────────────────────────────────────────────

def _paginated_query_count(table, **kwargs):
    count, scanned = 0, 0
    while True:
        resp     = table.query(**kwargs)
        count   += resp["Count"]
        scanned += resp["ScannedCount"]
        if "LastEvaluatedKey" not in resp:
            break
        kwargs["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
    return count, scanned


def _paginated_scan_count(table, **kwargs):
    count, scanned = 0, 0
    while True:
        resp     = table.scan(**kwargs)
        count   += resp["Count"]
        scanned += resp["ScannedCount"]
        if "LastEvaluatedKey" not in resp:
            break
        kwargs["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
    return count, scanned


def experiment_query_vs_scan(table):
    """
    Experiment A — Query vs Scan
    Both retrieve all events for DEVICE#0001. The results are identical.
    The cost is not:
      Query reads only the partition for that device.
      Scan reads every item in the table and post-filters.

    ScannedCount is directly proportional to RCU cost.
    """
    print("\n── Experiment A: Query vs Scan " + "─" * 36)
    TARGET = "DEVICE#0001"

    t0             = time.perf_counter()
    q_count, q_sc  = _paginated_query_count(
        table,
        KeyConditionExpression=Key("device_id").eq(TARGET),
        Select="COUNT",
    )
    t_query = time.perf_counter() - t0

    t0             = time.perf_counter()
    s_count, s_sc  = _paginated_scan_count(
        table,
        FilterExpression=Attr("device_id").eq(TARGET),
        Select="COUNT",
    )
    t_scan = time.perf_counter() - t0

    print(f"  Query : {q_count:>6,} items  ScannedCount={q_sc:>8,}  {t_query * 1000:>8.1f} ms")
    print(f"  Scan  : {s_count:>6,} items  ScannedCount={s_sc:>8,}  {t_scan  * 1000:>8.1f} ms")
    print(f"  Scan was {t_scan / t_query:.1f}× slower and read {s_sc // max(q_sc, 1)}× more items.")
    print(f"  Approximate RCU cost — Query: ~{(q_sc + 1) // 2}   Scan: ~{(s_sc + 1) // 2}")
    print("  (eventually consistent: 0.5 RCU per 4 KB read)")


def experiment_read_consistency(table):
    """
    Experiment B — Eventually consistent vs strongly consistent reads

    DynamoDB replicates each partition across three AZs.
    Eventually consistent (default):
      May return data from any replica.
      Cost: 0.5 RCU per 4 KB item.
    Strongly consistent:
      Always reads from the primary partition node.
      Guarantees the latest committed data.
      Cost: 1.0 RCU per 4 KB item  (2× more expensive).

    The latency difference is small; the cost difference is always 2×.
    Default to eventually consistent unless your application cannot tolerate
    reading stale data (e.g., immediately after a write in the same session).
    """
    print("\n── Experiment B: Eventually Consistent vs Strongly Consistent " + "─" * 6)

    resp = table.query(
        KeyConditionExpression=Key("device_id").eq("DEVICE#0002"),
        Limit=50,
    )
    keys = [{"device_id": i["device_id"], "event_id": i["event_id"]}
            for i in resp["Items"]]
    n    = len(keys)

    t0 = time.perf_counter()
    for k in keys:
        table.get_item(Key=k, ConsistentRead=False)
    t_eventual = time.perf_counter() - t0

    t0 = time.perf_counter()
    for k in keys:
        table.get_item(Key=k, ConsistentRead=True)
    t_strong = time.perf_counter() - t0

    print(f"  Eventually consistent ({n} GetItem calls): {t_eventual * 1000:>7.1f} ms"
          f"   avg {t_eventual / n * 1000:.2f} ms/item")
    print(f"  Strongly consistent   ({n} GetItem calls): {t_strong   * 1000:>7.1f} ms"
          f"   avg {t_strong   / n * 1000:.2f} ms/item")
    print(f"  Latency overhead: {(t_strong / t_eventual - 1) * 100:.1f}%")
    print("  RCU cost: strongly consistent reads always consume 2× the RCUs.")


def experiment_batch_vs_individual(table, ddb_client):
    """
    Experiment C — BatchGetItem vs individual GetItem calls

    N individual GetItem calls = N sequential network round trips.
    One BatchGetItem call with N keys = 1 network round trip (up to 100 items).

    The speedup is proportional to the saved round-trip latency.
    This is one of the most actionable DynamoDB optimisations in practice.

    Caveat: BatchGetItem may return UnprocessedKeys — the caller must retry
    those keys. The DynamoDB Resource client does NOT retry automatically here.
    """
    print("\n── Experiment C: BatchGetItem vs Individual GetItem " + "─" * 16)

    resp = table.query(
        KeyConditionExpression=Key("device_id").eq("DEVICE#0003"),
        Limit=30,
    )
    keys  = [{"device_id": i["device_id"], "event_id": i["event_id"]}
             for i in resp["Items"]]
    n     = len(keys)

    # N sequential GetItem calls
    t0 = time.perf_counter()
    for k in keys:
        table.get_item(Key=k)
    t_individual = time.perf_counter() - t0

    # 1 BatchGetItem call — requires DynamoDB wire types via the low-level client
    batch_keys = [{"device_id": {"S": k["device_id"]},
                   "event_id":  {"S": k["event_id"]}}
                  for k in keys]
    t0 = time.perf_counter()
    resp = ddb_client.batch_get_item(
        RequestItems={TABLE_NAME: {"Keys": batch_keys}}
    )
    t_batch = time.perf_counter() - t0

    unproc = len(resp.get("UnprocessedKeys", {}).get(TABLE_NAME, {}).get("Keys", []))
    print(f"  {n} individual GetItem : {t_individual * 1000:>7.1f} ms  ({n} round trips)")
    print(f"  1  BatchGetItem       : {t_batch      * 1000:>7.1f} ms  (1 round trip)  UnprocessedKeys={unproc}")
    print(f"  Speedup: {t_individual / t_batch:.1f}×")


def experiment_gsi_vs_scan(table):
    """
    Experiment D — GSI Query vs Scan for the same logical query

    Goal: count all 'offline' events (identical result from both paths).

    GSI Query (gsi-status): reads only the 'offline' partition of the GSI.
      ScannedCount ≈ matching items.

    Scan + FilterExpression: reads the entire base table.
      ScannedCount ≈ N_ITEMS regardless of how many match.

    This experiment reinforces that DynamoDB never refuses a Scan —
    it just charges for every item read. The data model (specifically the
    choice of GSIs) determines whether efficient queries are possible.
    """
    print("\n── Experiment D: GSI Query vs Scan (same logical query) " + "─" * 11)
    STATUS = "offline"

    t0             = time.perf_counter()
    g_count, g_sc  = _paginated_query_count(
        table,
        IndexName=GSI_STATUS,
        KeyConditionExpression=Key("status").eq(STATUS),
        Select="COUNT",
    )
    t_gsi = time.perf_counter() - t0

    t0             = time.perf_counter()
    s_count, s_sc  = _paginated_scan_count(
        table,
        FilterExpression=Attr("status").eq(STATUS),
        Select="COUNT",
    )
    t_scan = time.perf_counter() - t0

    print(f"  GSI Query : {g_count:>6,} items  ScannedCount={g_sc:>8,}  {t_gsi  * 1000:>8.1f} ms")
    print(f"  Scan      : {s_count:>6,} items  ScannedCount={s_sc:>8,}  {t_scan * 1000:>8.1f} ms")
    print(f"  GSI was {t_scan / t_gsi:.1f}× faster  |  Scan read {s_sc // max(g_sc, 1)}× more items.")
    print("  Rule of thumb: a Scan with FilterExpression on a large table almost")
    print("  always signals a missing index in the data model.")


# ─────────────────────────────────────────────────────────────────────────────
# 5. TEARDOWN
# ─────────────────────────────────────────────────────────────────────────────

def destroy_table(ddb):
    print("\n── Teardown " + "─" * 55)
    print(f"[DDB] Deleting table '{TABLE_NAME}' ...")
    try:
        table = ddb.Table(TABLE_NAME)
        table.delete()
        table.wait_until_not_exists()
        print("[DDB] Table deleted.")
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ResourceNotFoundException":
            print("[DDB] Table not found, skipping.")
        else:
            raise


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="DynamoDB Demo")
    parser.add_argument(
        "--step",
        choices=["all", "allocate", "populate", "patterns", "experiment", "destroy"],
        default="all",
    )
    args = parser.parse_args()

    ddb, ddb_client = get_resource_and_client()

    if args.step in ("all", "allocate"):
        table = create_table(ddb)
    else:
        table = ddb.Table(TABLE_NAME)

    if args.step in ("all", "populate"):
        populate(table)

    if args.step in ("all", "patterns"):
        demo_access_patterns(table, ddb_client)

    if args.step in ("all", "experiment"):
        experiment_query_vs_scan(table)
        experiment_read_consistency(table)
        experiment_batch_vs_individual(table, ddb_client)
        experiment_gsi_vs_scan(table)

    if args.step in ("all", "destroy"):
        destroy_table(ddb)


if __name__ == "__main__":
    main()
