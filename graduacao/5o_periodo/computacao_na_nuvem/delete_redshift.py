import boto3

# Mantenha a mesma região onde o cluster foi criado com sucesso
REGION_NAME = 'us-west-2' 
CLUSTER_IDENTIFIER = 'meu-cluster-teste-dw'

cliente_admin = boto3.client('redshift', region_name=REGION_NAME)

print(f"Iniciando exclusão do cluster '{CLUSTER_IDENTIFIER}'...")

try:
    resposta = cliente_admin.delete_cluster(
        ClusterIdentifier=CLUSTER_IDENTIFIER,
        SkipFinalClusterSnapshot=True
    )
    status = resposta['Cluster']['ClusterStatus']
    print(f"✅ Comando enviado! Status atual: {status}")
    print("O cluster desaparecerá da sua conta em alguns minutos e não gerará mais custos.")
    
except Exception as e:
    print(f"❌ Erro ao deletar o cluster: {e}")