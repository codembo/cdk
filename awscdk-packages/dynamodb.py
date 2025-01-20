import boto3

# Inicializar cliente do DynamoDB
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# Listar todas as tabelas
tables = dynamodb.list_tables()['TableNames']

# Iterar sobre as tabelas e obter informações de cada uma
for table in tables:
    response = dynamodb.describe_table(TableName=table)
    table_size = response['Table']['TableSizeBytes']
    print(f"Tabela: {table}, Tamanho: {table_size / (1024 * 1024):.2f} MB")
    print(f"Tabela: {table}, Tamanho: {table_size / (1024 * 1024)} MB")
