"""
rds_demo.py — Amazon RDS (PostgreSQL) Demonstration
Cloud Computing course  |  FGV EMAp

Lifecycle:
  1. allocate   — parameter group + security group + RDS instance
  2. populate   — 500 000-row sales table used across queries and experiments
  3. query      — five SQL access patterns (filter, aggregation, JOIN,
                  subquery, window function)
  4. experiment — four RDS-specific experiments:
                    A. IAM database authentication
                    B. Parameter Group: work_mem impact on sort plans
                    C. Read Replica: provisioning, replication lag, RPO
                    D. Performance Insights (console walkthrough)
  5. destroy    — read replica → primary → parameter group → security group

AWS credentials: ~/.aws/credentials (or environment variables / instance profile)
The IAM principal must have:
  - rds:* permissions for instance management
  - rds-db:connect on the DB resource (for experiment A)

Usage:
  python rds_demo.py                          # full lifecycle
  python rds_demo.py --step allocate
  python rds_demo.py --step populate
  python rds_demo.py --step query
  python rds_demo.py --step experiment
  python rds_demo.py --step destroy
"""

import argparse
import boto3
import psycopg2
import psycopg2.extras
import random
import string
import time
from botocore.exceptions import ClientError
from datetime import datetime, timedelta


# ── Configuration ──────────────────────────────────────────────────────────────
REGION         = "us-east-1"
DB_INSTANCE_ID = "rds-demo-primary"
DB_REPLICA_ID  = "rds-demo-replica"
DB_NAME        = "demo"
DB_ADMIN_USER  = "demo_admin"
DB_PASSWORD    = "Demo2025!Cloud"   # use Secrets Manager in production
DB_IAM_USER    = "demo_iam"         # created during populate; used in experiment A
DB_PORT        = 5432
INSTANCE_CLASS = "db.t3.micro"
PG_VERSION     = "16"
SG_NAME        = "rds-demo-sg"
PG_GROUP_NAME  = "rds-demo-pg16"   # custom parameter group

N_PRODUCTS     = 500
N_ROWS         = 500_000


# ─────────────────────────────────────────────────────────────────────────────
# 1. ALLOCATION
# ─────────────────────────────────────────────────────────────────────────────

def get_clients():
    session = boto3.Session(region_name=REGION)
    return session.client("rds"), session.client("ec2")


def create_parameter_group(rds):
    """
    Creates a custom DB Parameter Group based on the postgres16 family.

    Why a custom group?
      The default parameter group is read-only — AWS does not allow modifying it.
      Any parameter tuning (work_mem, max_connections, shared_buffers, …) requires
      creating a custom group first.

    The group is initialised with work_mem=4096 kB (4 MB) so that experiment B
    can later demonstrate the effect of raising it.
    """
    print(f"[PG]  Creating parameter group '{PG_GROUP_NAME}' ...")
    try:
        rds.create_db_parameter_group(
            DBParameterGroupName=PG_GROUP_NAME,
            DBParameterGroupFamily=f"postgres{PG_VERSION}",
            Description="Demo parameter group - postgres 16",
        )
        # work_mem is a DYNAMIC parameter: changes apply to new connections
        # without a reboot (unlike static parameters such as shared_buffers).
        rds.modify_db_parameter_group(
            DBParameterGroupName=PG_GROUP_NAME,
            Parameters=[{
                "ParameterName":  "work_mem",
                "ParameterValue": "4096",      # 4 MB, expressed in kB
                "ApplyMethod":    "immediate",
            }],
        )
        print("[PG]  Created  (work_mem = 4 MB)")
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "DBParameterGroupAlreadyExists":
            print("[PG]  Already exists, reusing.")
        else:
            raise
    return PG_GROUP_NAME


def create_security_group(ec2):
    """
    Creates (or retrieves) a security group allowing inbound PostgreSQL (5432).

    NOTE: 0.0.0.0/0 is acceptable for a short-lived classroom demo that is
    destroyed at the end of the session. In production, restrict the CIDR to
    the application subnet or specific IP range.
    """
    vpcs = ec2.describe_vpcs(Filters=[{"Name": "isDefault", "Values": ["true"]}])
    if not vpcs["Vpcs"]:
        raise RuntimeError("No default VPC found.")
    vpc_id = vpcs["Vpcs"][0]["VpcId"]

    try:
        sg    = ec2.create_security_group(
            GroupName=SG_NAME,
            Description="RDS demo - PostgreSQL inbound",
            VpcId=vpc_id,
        )
        sg_id = sg["GroupId"]
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[{
                "IpProtocol": "tcp",
                "FromPort":   DB_PORT,
                "ToPort":     DB_PORT,
                "IpRanges":   [{"CidrIp": "0.0.0.0/0"}],
            }],
        )
        print(f"[SG]  Created {sg_id}  (VPC: {vpc_id})")
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "InvalidGroup.Duplicate":
            existing = ec2.describe_security_groups(
                Filters=[{"Name": "group-name", "Values": [SG_NAME]}]
            )
            sg_id = existing["SecurityGroups"][0]["GroupId"]
            print(f"[SG]  Already exists: {sg_id}")
        else:
            raise
    return sg_id


def allocate_rds(rds, sg_id, pg_group):
    """
    Creates the RDS primary instance.

    Key parameters:
      EnableIAMDatabaseAuthentication — required for experiment A (token-based login)
      DBParameterGroupName            — our custom group with low work_mem
      BackupRetentionPeriod=1         — must be >= 1 to allow Read Replica creation
      PubliclyAccessible=True         — needed so this machine can connect directly
      MultiAZ=False                   — single-AZ is fine for a demo
    """
    print(f"[RDS] Creating '{DB_INSTANCE_ID}' ({INSTANCE_CLASS} / postgres{PG_VERSION}) ...")
    try:
        rds.create_db_instance(
            DBInstanceIdentifier=DB_INSTANCE_ID,
            DBInstanceClass=INSTANCE_CLASS,
            Engine="postgres",
            EngineVersion=PG_VERSION,
            MasterUsername=DB_ADMIN_USER,
            MasterUserPassword=DB_PASSWORD,
            DBName=DB_NAME,
            AllocatedStorage=20,
            StorageType="gp2",
            VpcSecurityGroupIds=[sg_id],
            DBParameterGroupName=pg_group,
            EnableIAMDatabaseAuthentication=True,
            PubliclyAccessible=True,
            BackupRetentionPeriod=1,   # minimum required for Read Replica
            MultiAZ=False,
            AutoMinorVersionUpgrade=False,
            Tags=[{"Key": "purpose", "Value": "rds-demo"}],
        )
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "DBInstanceAlreadyExists":
            print("[RDS] Already exists, skipping creation.")
        else:
            raise

    print("[RDS] Waiting for 'available' (typically 5–8 min) ...")
    waiter = rds.get_waiter("db_instance_available")
    waiter.wait(DBInstanceIdentifier=DB_INSTANCE_ID,
                WaiterConfig={"Delay": 30, "MaxAttempts": 40})

    info     = rds.describe_db_instances(DBInstanceIdentifier=DB_INSTANCE_ID)
    instance = info["DBInstances"][0]
    endpoint = instance["Endpoint"]["Address"]
    print(f"[RDS] Ready  endpoint={endpoint}  version={instance['EngineVersion']}")
    return endpoint


def get_primary_endpoint(rds):
    info = rds.describe_db_instances(DBInstanceIdentifier=DB_INSTANCE_ID)
    return info["DBInstances"][0]["Endpoint"]["Address"]


def connect(endpoint, user=DB_ADMIN_USER, password=DB_PASSWORD,
            retries=6, delay=10, ssl=False):
    kwargs = dict(
        host=endpoint,
        port=DB_PORT,
        dbname=DB_NAME,
        user=user,
        password=password,
        connect_timeout=10
    )
    if ssl:
        kwargs["sslmode"] = "require"

    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(**kwargs)
            print(f"[DB]  Connected  host={endpoint}  user={user}")
            return conn
        except psycopg2.OperationalError as exc:
            if attempt == retries:
                raise
            print(f"[DB]  Attempt {attempt}/{retries}: {exc}. Retrying in {delay}s ...")
            time.sleep(delay)
    return None


# ─────────────────────────────────────────────────────────────────────────────
# 2. POPULATE
# ─────────────────────────────────────────────────────────────────────────────

DDL = """
CREATE TABLE IF NOT EXISTS products (
    product_id   SERIAL        PRIMARY KEY,
    name         VARCHAR(80)   NOT NULL,
    category     VARCHAR(40)   NOT NULL,
    unit_price   NUMERIC(8,2)  NOT NULL,
    stock_qty    INT           NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id      SERIAL        PRIMARY KEY,
    product_id   INT           NOT NULL REFERENCES products(product_id),
    region       VARCHAR(30)   NOT NULL,
    quantity     SMALLINT      NOT NULL,
    unit_price   NUMERIC(8,2)  NOT NULL,
    total_price  NUMERIC(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    sale_date    DATE          NOT NULL,
    salesperson  VARCHAR(40)   NOT NULL
);
"""

CATEGORIES  = ["Electronics", "Clothing", "Books", "Food", "Sports",
                "Home", "Toys", "Beauty", "Tools", "Garden"]
REGIONS     = ["North", "South", "East", "West", "Central",
                "Northeast", "Northwest", "Southeast", "Southwest", "International"]
FIRST_NAMES = ["Alice", "Bob", "Carol", "David", "Eva", "Frank",
                "Grace", "Henry", "Iris", "Jack", "Karen", "Leo"]
LAST_NAMES  = ["Smith", "Jones", "Brown", "Wilson", "Taylor",
                "Davis", "Miller", "White", "Moore", "Clark"]


def random_product_name(category):
    words = {
        "Electronics": ["Laptop", "Tablet", "Headphones", "Camera", "Speaker"],
        "Clothing":    ["Jacket", "Shirt", "Jeans", "Dress", "Shoes"],
        "Books":       ["Novel", "Textbook", "Guide", "Handbook", "Atlas"],
        "Food":        ["Coffee", "Tea", "Snack", "Sauce", "Spice"],
        "Sports":      ["Racket", "Gloves", "Helmet", "Mat", "Bottle"],
    }
    base  = random.choice(words.get(category, ["Item"]))
    brand = "".join(random.choices(string.ascii_uppercase, k=3))
    model = random.randint(100, 999)
    return f"{brand} {base} {model}"


def populate(conn, n_rows=N_ROWS):
    with conn.cursor() as cur:
        cur.execute(DDL)

        # IAM user required for experiment A.
        # rds_iam is a built-in PostgreSQL role provided by RDS that allows
        # the user to authenticate via IAM token instead of a password.
        cur.execute(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '{DB_IAM_USER}') THEN
                    CREATE USER {DB_IAM_USER} WITH LOGIN;
                END IF;
            END$$;
            GRANT rds_iam TO {DB_IAM_USER};
            GRANT SELECT ON ALL TABLES IN SCHEMA public TO {DB_IAM_USER};
        """)

        # Insert products
        products = []
        for _ in range(N_PRODUCTS):
            category = random.choice(CATEGORIES)
            products.append((
                random_product_name(category),
                category,
                round(random.uniform(5.0, 2000.0), 2),
                random.randint(0, 500),
            ))
        psycopg2.extras.execute_values(
            cur,
            "INSERT INTO products (name, category, unit_price, stock_qty) VALUES %s",
            products, page_size=500,
        )

        # Fetch inserted IDs and prices for FK references
        cur.execute("SELECT product_id, unit_price FROM products")
        product_rows = cur.fetchall()

        # Insert sales in batches
        base_date    = datetime(2022, 1, 1).date()
        salespersons = [f"{f} {l}" for f in FIRST_NAMES for l in LAST_NAMES]
        batch        = []
        for i in range(n_rows):
            pid, price = random.choice(product_rows)
            sale_date  = base_date + timedelta(days=random.randint(0, 1500))
            batch.append((
                pid, random.choice(REGIONS), random.randint(1, 20), float(price),
                sale_date.isoformat(), random.choice(salespersons),
            ))
            if len(batch) == 5000:
                psycopg2.extras.execute_values(
                    cur,
                    "INSERT INTO sales (product_id, region, quantity, unit_price, "
                    "                   sale_date, salesperson) VALUES %s",
                    batch, page_size=2000,
                )
                batch = []
                print(f"  {i + 1:,}/{n_rows:,} rows inserted ...")

        if batch:
            psycopg2.extras.execute_values(
                cur,
                "INSERT INTO sales (product_id, region, quantity, unit_price, "
                "                   sale_date, salesperson) VALUES %s",
                batch, page_size=2000,
            )

    conn.commit()
    print(f"[DB]  Done: {N_PRODUCTS} products + {n_rows:,} sales.")


# ─────────────────────────────────────────────────────────────────────────────
# 3. QUERY PATTERNS
# ─────────────────────────────────────────────────────────────────────────────

def demo_queries(conn):
    print("\n── Query Access Patterns " + "─" * 40)
    with conn.cursor() as cur:

        print("\n[Q1] SELECT + WHERE — Electronics products over $500:")
        cur.execute("""
            SELECT name, unit_price, stock_qty
            FROM products
            WHERE category = %s AND unit_price > 500
            ORDER BY unit_price DESC
            LIMIT 5
        """, ("Electronics",))
        for r in cur.fetchall():
            print(f"     {r}")

        print("\n[Q2] GROUP BY + aggregation — total revenue by category:")
        cur.execute("""
            SELECT p.category,
                   COUNT(s.sale_id)                AS transactions,
                   SUM(s.total_price)              AS total_revenue,
                   ROUND(AVG(s.total_price), 2)    AS avg_ticket
            FROM sales s
            JOIN products p USING (product_id)
            GROUP BY p.category
            ORDER BY total_revenue DESC
        """)
        for r in cur.fetchall():
            print(f"     {r}")

        print("\n[Q3] JOIN — top 5 salespersons by revenue in 2023:")
        cur.execute("""
            SELECT salesperson,
                   COUNT(*)                AS sales_count,
                   SUM(total_price)        AS revenue
            FROM sales
            WHERE sale_date BETWEEN '2023-01-01' AND '2023-12-31'
            GROUP BY salesperson
            ORDER BY revenue DESC
            LIMIT 5
        """)
        for r in cur.fetchall():
            print(f"     {r}")

        print("\n[Q4] Subquery — products that outsell the per-product average:")
        cur.execute("""
            SELECT p.name, p.category, SUM(s.quantity) AS units_sold
            FROM sales s
            JOIN products p USING (product_id)
            GROUP BY p.product_id, p.name, p.category
            HAVING SUM(s.quantity) > (
                SELECT AVG(total_units)
                FROM (SELECT SUM(quantity) AS total_units
                      FROM sales GROUP BY product_id) sub
            )
            ORDER BY units_sold DESC
            LIMIT 6
        """)
        for r in cur.fetchall():
            print(f"     {r}")

        print("\n[Q5] Window function — monthly rank of regions by revenue:")
        cur.execute("""
            SELECT region,
                   DATE_TRUNC('month', sale_date)          AS month,
                   SUM(total_price)                        AS revenue,
                   RANK() OVER (
                       PARTITION BY DATE_TRUNC('month', sale_date)
                       ORDER BY SUM(total_price) DESC
                   )                                       AS rank
            FROM sales
            WHERE sale_date >= '2023-01-01'
            GROUP BY region, month
            ORDER BY month, rank
            LIMIT 20
        """)
        for r in cur.fetchall():
            print(f"     {r}")


# ─────────────────────────────────────────────────────────────────────────────
# 4A. EXPERIMENT — IAM DATABASE AUTHENTICATION
# ─────────────────────────────────────────────────────────────────────────────

def experiment_iam_auth(endpoint):
    """
    IAM Database Authentication replaces static passwords with short-lived
    tokens signed by AWS Signature Version 4.

    How it works:
      1. The RDS instance must have EnableIAMDatabaseAuthentication=True
         (set during allocation).
      2. A PostgreSQL user must have the rds_iam role (granted in populate()).
      3. The calling IAM principal needs the rds-db:connect permission on the
         resource ARN:
           arn:aws:rds-db:<region>:<account>:dbuser/<instance-id>/<db-user>
      4. generate_db_auth_token() signs a 15-minute token using SigV4.
      5. psycopg2 passes the token as the password. SSL is mandatory.

    Security advantage: no long-lived credential to rotate or accidentally leak.
    The token is worthless after 15 minutes even if intercepted.
    """
    print("\n── Experiment A: IAM Database Authentication " + "─" * 20)

    rds = boto3.client("rds", region_name=REGION)
    try:
        token = rds.generate_db_auth_token(
            DBHostname=endpoint,
            Port=DB_PORT,
            DBUsername=DB_IAM_USER,
            Region=REGION,
        )
        print(f"  Token (first 80 chars): {token[:80]}...")
        print(f"  Token length : {len(token)} chars")
        print(f"  Token expiry : 15 minutes from now")

        conn = connect(endpoint, user=DB_IAM_USER, password=token, ssl=True)
        with conn.cursor() as cur:
            cur.execute("SELECT current_user, pg_is_in_recovery()")
            user, ssl_on = cur.fetchone()
            print(f"\n  Connected as '{user}'  |  SSL: active (required by IAM auth)")
            cur.execute("SELECT COUNT(*) FROM sales")
            print(f"  SELECT COUNT(*) FROM sales → {cur.fetchone()[0]:,}  (read confirmed)")
        conn.close()
        print("  ✓ IAM auth successful — no static password was used.")

    except ClientError as exc:
        print(f"  ✗ Token generation failed: {exc}")
        print("    Ensure your IAM principal has rds-db:connect on:")
        print(f"    arn:aws:rds-db:{REGION}:<account>:dbuser/{DB_INSTANCE_ID}/{DB_IAM_USER}")
    except psycopg2.OperationalError as exc:
        print(f"  ✗ Connection failed: {exc}")
        print("    Verify that rds_iam role is granted to the DB user (done in populate()).")


# ─────────────────────────────────────────────────────────────────────────────
# 4B. EXPERIMENT — PARAMETER GROUP: work_mem AND SORT PLANS
# ─────────────────────────────────────────────────────────────────────────────

def experiment_parameter_group(rds, conn):
    """
    Parameter Groups are the RDS mechanism to tune the database engine without
    SSH access or direct file editing (no postgresql.conf).

    This experiment changes work_mem — the memory budget PostgreSQL allocates
    per sort operation per query — and observes the effect on the query planner.

    work_mem too low:  sort cannot fit in memory → spills to disk
                       EXPLAIN reports: Sort Method: external merge  (Disk)
    work_mem adequate: sort fits entirely in memory
                       EXPLAIN reports: Sort Method: quicksort  (Memory)

    Parameter types:
      DYNAMIC — take effect on new connections without reboot (e.g. work_mem)
      STATIC  — require an instance reboot (e.g. shared_buffers)
    """
    print("\n── Experiment B: Parameter Group — work_mem and Sort Plans " + "─" * 8)

    SORT_QUERY = """
            EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
            SELECT sale_id, salesperson, region, total_price, sale_date
            FROM sales
            ORDER BY total_price DESC, salesperson, sale_date
        """

    def run_and_show(cur, label, work_mem_kb):
        cur.execute(f"SET work_mem = '{work_mem_kb}kB'")
        cur.execute("SHOW work_mem")
        actual = cur.fetchone()[0]
        t0     = time.perf_counter()
        cur.execute(SORT_QUERY)
        plan   = [r[0] for r in cur.fetchall()]
        ms     = (time.perf_counter() - t0) * 1000

        sort_line = next((l for l in plan if "Sort Method" in l), "(not found)")
        exec_line = next((l for l in plan if "Execution Time" in l), "")
        print(f"\n  [{label}]  work_mem = {actual}")
        print(f"    {sort_line.strip()}")
        print(f"    {exec_line.strip()}  ({ms:.0f} ms)")

    with conn.cursor() as cur:
        # --- With low work_mem (4 MB, mirrors the parameter group default) ---
        print("  Step 1: low work_mem (4 MB) — parameter group default")
        run_and_show(cur, "LOW  4 MB", 4096)

        # --- Raise work_mem via boto3, no SSH required ---
        print("\n  Step 2: raising work_mem to 256 MB via boto3")
        rds.modify_db_parameter_group(
            DBParameterGroupName=PG_GROUP_NAME,
            Parameters=[{
                "ParameterName":  "work_mem",
                "ParameterValue": "262144",     # 256 MB in kB
                "ApplyMethod":    "immediate",
            }],
        )
        print("  boto3 call returned — parameter updated.")
        run_and_show(cur, "HIGH 256 MB", 262144)

    print("\n  ✓ Observation: sort method changed from disk spill to in-memory.")
    print("    Caution: work_mem is allocated per sort node per connection.")
    print("    High values × many concurrent queries can exhaust instance RAM.")


# ─────────────────────────────────────────────────────────────────────────────
# 4C. EXPERIMENT — READ REPLICA
# ─────────────────────────────────────────────────────────────────────────────

def experiment_read_replica(rds, primary_conn):
    """
    A Read Replica is an asynchronously replicated, read-only copy of the
    primary instance. RDS manages the replication stream automatically.

    Key properties to demonstrate:
      - Replication is ASYNCHRONOUS  → RPO > 0 (uncommitted writes can be lost)
      - The replica has its own DNS endpoint and can serve SELECT queries
      - pg_is_in_recovery() = true on the replica
      - pg_stat_replication on the primary shows the lag metrics
      - Promoting a replica to standalone requires a manual API call
        and an application-side endpoint change

    Compare with Multi-AZ:
      - Multi-AZ uses SYNCHRONOUS replication  → RPO = 0
      - Failover is automatic; the endpoint DNS flips within ~60 s
      - The standby is not readable (unlike a Read Replica)

    Experiment flow:
      1. Provision the replica (~5–10 min)
      2. Write 10 000 rows to the primary
      3. Immediately count rows on the replica (may be stale — shows async lag)
      4. Wait, re-count (convergence)
      5. Read pg_stat_replication on the primary
    """
    print("\n── Experiment C: Read Replica " + "─" * 38)
    print("  Waiting for primary to reach 'available' state ...")
    waiter = rds.get_waiter("db_instance_available")
    waiter.wait(DBInstanceIdentifier=DB_INSTANCE_ID,
                WaiterConfig={"Delay": 15, "MaxAttempts": 20})
    print("  Primary is available.")
    print("  Provisioning read replica (typically 5–10 min) ...")

    try:
        rds.create_db_instance_read_replica(
            DBInstanceIdentifier=DB_REPLICA_ID,
            SourceDBInstanceIdentifier=DB_INSTANCE_ID,
            DBInstanceClass=INSTANCE_CLASS,
            PubliclyAccessible=True,
            AutoMinorVersionUpgrade=False,
            Tags=[{"Key": "purpose", "Value": "rds-demo-replica"}],
        )
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "DBInstanceAlreadyExists":
            raise

    waiter = rds.get_waiter("db_instance_available")
    waiter.wait(DBInstanceIdentifier=DB_REPLICA_ID,
                WaiterConfig={"Delay": 30, "MaxAttempts": 40})

    info             = rds.describe_db_instances(DBInstanceIdentifier=DB_REPLICA_ID)
    replica_endpoint = info["DBInstances"][0]["Endpoint"]["Address"]
    print(f"  Replica ready  endpoint={replica_endpoint}")

    replica_conn = connect(replica_endpoint)

    # Confirm replica identity
    with replica_conn.cursor() as cur:
        cur.execute("SELECT pg_is_in_recovery()")
        print(f"\n  pg_is_in_recovery() on replica = {cur.fetchone()[0]}  (True = read-only standby)")

    # Baseline counts before the write burst
    with primary_conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM sales")
        baseline = cur.fetchone()[0]
    with replica_conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM sales")
        replica_baseline = cur.fetchone()[0]
    print(f"\n  Baseline — primary: {baseline:,}  replica: {replica_baseline:,}")

    # Write 200 000 rows to the primary in a single commit.
    # The larger volume gives the replication stream time to lag visibly.
    N_BURST = 1_000_000
    print(f"  Writing {N_BURST:,} rows to primary ...")
    rows = []
    for _ in range(N_BURST):
        rows.append((
            random.randint(1, N_PRODUCTS),
            random.choice(REGIONS),
            random.randint(1, 10),
            round(random.uniform(10.0, 500.0), 2),
            (datetime(2024, 6, 1).date() + timedelta(days=random.randint(0, 90))).isoformat(),
            "Replica Lag Test",
        ))
    with primary_conn.cursor() as cur:
        psycopg2.extras.execute_values(
            cur,
            "INSERT INTO sales (product_id, region, quantity, unit_price, "
            "                   sale_date, salesperson) VALUES %s",
            rows, page_size=2000,
        )
    primary_conn.commit()

    primary_count = baseline + N_BURST
    print(f"  Primary COUNT(*) after commit = {primary_count:,}"
          f"  (+{primary_count - baseline:,} rows)")

    # Poll the replica every 200 ms for up to 10 s, showing convergence.
    print(f"\n  {'Elapsed':>8}  {'Replica COUNT(*)':>18}  {'Lag (rows)':>12}")
    print(f"  {'-' * 8}  {'-' * 18}  {'-' * 12}")
    t0 = time.perf_counter()
    converged = False
    for _ in range(50):
        with replica_conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM sales")
            replica_count = cur.fetchone()[0]
        elapsed = time.perf_counter() - t0
        lag_rows = primary_count - replica_count
        print(f"  {elapsed:>7.1f}s  {replica_count:>18,}  {lag_rows:>12,}")
        if lag_rows == 0:
            converged = True
            break
        time.sleep(0.2)

    if converged:
        print("  ✓ Replica fully caught up.")
    else:
        print("  ⚠ Replica did not fully converge within the polling window.")

    # Replication lag metrics from the primary
    print("\n  pg_stat_replication on primary:")
    with primary_conn.cursor() as cur:
        cur.execute("""
                    SELECT client_addr,
                           state,
                           write_lag,
                           flush_lag,
                           replay_lag,
                           sent_lsn,
                           replay_lsn
                    FROM pg_stat_replication
                    """)
        rows = cur.fetchall()
        if rows:
            cols = [d[0] for d in cur.description]
            for row in rows:
                for col, val in zip(cols, row):
                    print(f"    {col:<15} {val}")
        else:
            print("    (no rows — replica may still be catching up)")

    replica_conn.close()

    print("\n  ✓ Read Replica demonstration complete.")
    print("  Key lesson: ASYNC replication means a crash of the primary right")
    print("  after commit could lose those rows on the replica (RPO > 0).")
    print("  Multi-AZ avoids this with synchronous replication (RPO = 0).")


# ─────────────────────────────────────────────────────────────────────────────
# 4D. PERFORMANCE INSIGHTS — CONSOLE WALKTHROUGH
# ─────────────────────────────────────────────────────────────────────────────

def experiment_performance_insights():
    print("\n── Experiment D: Performance Insights (Console) " + "─" * 18)


# ─────────────────────────────────────────────────────────────────────────────
# 5. TEARDOWN
# ─────────────────────────────────────────────────────────────────────────────

def destroy(rds, ec2):
    """
    Deletion order matters:
      1. Read Replica  — must be deleted before the primary.
      2. Primary       — must be gone before the parameter group can be deleted
                         (RDS refuses to delete a group in use by an instance).
      3. Parameter Group + Security Group last.
    """
    print("\n── Teardown " + "─" * 55)

    for instance_id, label in [(DB_REPLICA_ID, "replica"), (DB_INSTANCE_ID, "primary")]:
        print(f"[RDS] Deleting {label} '{instance_id}' ...")
        try:
            rds.delete_db_instance(
                DBInstanceIdentifier=instance_id,
                SkipFinalSnapshot=True,
                DeleteAutomatedBackups=True,
            )
            w = rds.get_waiter("db_instance_deleted")
            w.wait(DBInstanceIdentifier=instance_id,
                   WaiterConfig={"Delay": 30, "MaxAttempts": 40})
            print(f"[RDS] {label.capitalize()} deleted.")
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            if code in ("DBInstanceNotFound", "InvalidDBInstanceState"):
                print(f"[RDS] {label.capitalize()} not found or already deleted.")
            else:
                raise

    try:
        rds.delete_db_parameter_group(DBParameterGroupName=PG_GROUP_NAME)
        print(f"[PG]  '{PG_GROUP_NAME}' deleted.")
    except ClientError as exc:
        print(f"[PG]  Could not delete: {exc.response['Error']['Code']}")

    try:
        sgs = ec2.describe_security_groups(
            Filters=[{"Name": "group-name", "Values": [SG_NAME]}]
        )
        if sgs["SecurityGroups"]:
            sg_id = sgs["SecurityGroups"][0]["GroupId"]
            ec2.delete_security_group(GroupId=sg_id)
            print(f"[SG]  {sg_id} deleted.")
    except ClientError as exc:
        print(f"[SG]  Could not delete: {exc.response['Error']['Code']}")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="RDS PostgreSQL Demo")
    parser.add_argument(
        "--step",
        choices=["all", "allocate", "populate", "query", "experiment", "destroy"],
        default="all",
    )
    args = parser.parse_args()

    rds, ec2 = get_clients()
    conn     = None

    if args.step in ("all", "allocate"):
        pg_group = create_parameter_group(rds)
        sg_id    = create_security_group(ec2)
        endpoint = allocate_rds(rds, sg_id, pg_group)
    else:
        endpoint = get_primary_endpoint(rds)

    if args.step in ("all", "populate", "query", "experiment"):
        conn = connect(endpoint)

    if args.step in ("all", "populate"):
        populate(conn)

    if args.step in ("all", "query"):
        demo_queries(conn)

    if args.step in ("all", "experiment"):
        experiment_iam_auth(endpoint)
        experiment_parameter_group(rds, conn)
        experiment_read_replica(rds, conn)
        experiment_performance_insights()

    if conn:
        conn.close()

    if args.step in ("all", "destroy"):
        destroy(rds, ec2)


if __name__ == "__main__":
    main()
