
### Código Boto3 para AWS Learner Lab

import boto3
import time
from botocore.exceptions import ClientError

# =====================================================================
# 1. CONFIGURAÇÕES DO SEU REDSHIFT (LAB ENVIRONMENT)
# =====================================================================
REGION_NAME = 'us-west-2'                 
CLUSTER_IDENTIFIER = 'meu-cluster-teste-dw' 
DATABASE_NAME = 'dev'                       
DATABASE_USER = 'awsuser'                   
MASTER_PASSWORD = 'Password123!'            
# Tente dc2.large primeiro. Se der o erro "Invalid node type", mude para 'ra3.xlplus'
NODE_TYPE = 'ra3.xlplus' 
# NODE_TYPE = 'dc2.large'                  

# Inicializa os clientes Boto3
cliente_sts = boto3.client('sts', region_name=REGION_NAME)
cliente_admin = boto3.client('redshift', region_name=REGION_NAME)
cliente_dw = boto3.client('redshift-data', region_name=REGION_NAME)

# Descobre o ID da conta AWS dinamicamente para montar a LabRole
conta_aws_id = cliente_sts.get_caller_identity()['Account']
LAB_ROLE_ARN = f"arn:aws:iam::{conta_aws_id}:role/LabRole"

# =====================================================================
# 2. FUNÇÕES DE INFRAESTRUTURA
# =====================================================================

def criar_cluster_redshift():
    print(f"=== INICIANDO CRIAÇÃO DO CLUSTER '{CLUSTER_IDENTIFIER}' ===")
    print(f"🔗 Conta AWS: {conta_aws_id}")
    print(f"🔗 Anexando LabRole: {LAB_ROLE_ARN}")
    
    try:
        cliente_admin.create_cluster(
            ClusterIdentifier=CLUSTER_IDENTIFIER,
            NodeType=NODE_TYPE,
            MasterUsername=DATABASE_USER,
            MasterUserPassword=MASTER_PASSWORD,
            DBName=DATABASE_NAME,
            ClusterType='single-node',
            # MUDANÇAS CRÍTICAS PARA O VOCLABS:
            PubliclyAccessible=False, 
            IamRoles=[LAB_ROLE_ARN]   
        )
        print("⏳ Solicitação enviada. O cluster está sendo provisionado.")
        return True
    except ClientError as e:
        codigo_erro = e.response['Error']['Code']
        if codigo_erro == 'ClusterAlreadyExists':
            print(f"ℹ️ O cluster '{CLUSTER_IDENTIFIER}' já existe. Prosseguindo...")
            return True
        else:
            print(f"❌ Erro ao criar o cluster: {e.response['Error']['Message']}")
            return False

def aguardar_cluster_disponivel():
    print("⏳ Aguardando o cluster ficar disponível (Isso pode levar de 3 a 10 minutos)...")
    while True:
        try:
            resposta = cliente_admin.describe_clusters(ClusterIdentifier=CLUSTER_IDENTIFIER)
            status = resposta['Clusters'][0]['ClusterStatus']
            
            if status == 'available':
                print("\n✅ O cluster está DISPONÍVEL e pronto para uso!")
                break
            elif status in ['deleting', 'failed']:
                print(f"\n❌ Falha: O cluster caiu no status '{status}' de novo. O robô do lab o destruiu.")
                return False
                
            print(f"[{status}]", end='...', flush=True)
            time.sleep(30)  
            
        except Exception as e:
            print(f"\n❌ Erro ao verificar o status: {e}")
            return False
    return True

# =====================================================================
# 3. FUNÇÕES DO DATA WAREHOUSE (SQL)
# =====================================================================

def rodar_sql(sql, aguardar_resultados=False):
    print(f"Enviando query: {sql[:50].strip()}...")
    try:
        resposta = cliente_dw.execute_statement(
            ClusterIdentifier=CLUSTER_IDENTIFIER,
            Database=DATABASE_NAME,
            DbUser=DATABASE_USER,
            Sql=sql
        )
        query_id = resposta['Id']
        
        status = 'SUBMITTED'
        while status in ['SUBMITTED', 'PICKED', 'STARTED']:
            time.sleep(1)
            status_query = cliente_dw.describe_statement(Id=query_id)
            status = status_query['Status']
            
        if status == 'FAILED':
            print(f"❌ Erro na execução do SQL: {status_query.get('Error')}")
            return None
            
        if aguardar_resultados and status_query['HasResultSet']:
            resultados = cliente_dw.get_statement_result(Id=query_id)
            return resultados.get('Records', [])
            
        return True

    except Exception as e:
        print(f"❌ Falha de comunicação com o Redshift Data API.\nDetalhes: {e}")
        return None

def testar_data_warehouse():
    print("\n=== INICIANDO TESTE DE FUNCIONAMENTO DO DW ===")

    sql_criar_tabela = """
    CREATE TABLE IF NOT EXISTS teste_vendas_dw (
        id_venda INT,
        produto VARCHAR(50),
        quantidade INT,
        preco_unitario DECIMAL(10,2)
    );
    """
    rodar_sql(sql_criar_tabela)
    rodar_sql("TRUNCATE TABLE teste_vendas_dw;")

    sql_inserir_dados = """
    INSERT INTO teste_vendas_dw (id_venda, produto, quantidade, preco_unitario) VALUES 
    (1, 'Notebook', 2, 4500.00),
    (2, 'Monitor Ultrawide', 5, 1200.50),
    (3, 'Teclado Mecânico', 10, 350.00),
    (4, 'Mouse Sem Fio', 15, 120.00);
    """
    rodar_sql(sql_inserir_dados)

    sql_consulta = """
    SELECT 
        produto, 
        quantidade, 
        preco_unitario, 
        (quantidade * preco_unitario) as faturamento_total 
    FROM teste_vendas_dw 
    ORDER BY faturamento_total DESC;
    """
    
    print("\nProcessando consulta analítica...")
    linhas = rodar_sql(sql_consulta, aguardar_resultados=True)

    if linhas:
        print("\n✅ DATA WAREHOUSE OPERACIONAL! Veja os resultados:")
        print("-" * 70)
        print(f"{'PRODUTO':<20} | {'QTD':<5} | {'PREÇO (R$)':<12} | {'FATURAMENTO (R$)'}")
        print("-" * 70)
        
        for linha in linhas:
            produto = linha[0]['stringValue']
            qtd = linha[1]['longValue']
            preco = linha[2]['stringValue']
            faturamento = linha[3]['stringValue']
            print(f"{produto:<20} | {qtd:<5} | {preco:<12} | {faturamento}")
        print("-" * 70)

# =====================================================================
# EXECUÇÃO PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    if criar_cluster_redshift():
        if aguardar_cluster_disponivel():
            testar_data_warehouse()
            print("\n🏁 Lembre-se de deletar o cluster via console ou código quando terminar!")
