import os

from dotenv import load_dotenv

if os.getenv('ENVIRONMENT') == 'dev':
    load_dotenv('.env.dev')
elif os.getenv('ENVIRONMENT') == 'prod':
    load_dotenv('.env.prod')
elif os.getenv('ENVIRONMENT') == 'qa':
    load_dotenv('.env.qa')
elif os.getenv('ENVIRONMENT') == 'uat':
    load_dotenv('.env.uat')

AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
AWS_DEFAULT_ACCOUNT = os.getenv('AWS_DEFAULT_ACCOUNT')

ENVIRONMENT = os.getenv('ENVIRONMENT')
VPC_ID = os.getenv('VPC_ID')
ECS_FARGATE_CERTIFICATE_ARN = os.getenv('ECS_FARGATE_CERTIFICATE_ARN')
ECS_FARGATE_CONTAINER_IMAGE = os.getenv('ECS_FARGATE_CONTAINER_IMAGE')
WEB_APP_BUCKET = os.getenv('WEB_APP_BUCKET')
WEB_APP_DOMAIN_NAMES = os.getenv('WEB_APP_DOMAIN_NAMES').split(',')
WEB_APP_CERT = os.getenv('WEB_APP_CERT')
MANAGEMENT_ZONES_BUCKET = os.getenv('MANAGEMENT_ZONES_BUCKET')
CROSS_ACCOUNT_ACCESS_ACCOUNT_IDS = os.getenv('CROSS_ACCOUNT_ACCESS_ACCOUNT_IDS')

PASSWORD = os.getenv('PASSWORD')
NIDERA_AUTHENTICATION_FLAG = os.getenv('NIDERA_AUTHENTICATION_FLAG')
FARMSHOTS_USER_ID = os.getenv('FARMSHOTS_USER_ID')
CROPWISE_BASE_URL = os.getenv('CROPWISE_BASE_URL')
NIDERA_AUTH_URL = os.getenv('NIDERA_AUTH_URL')
BASE_AUTH_URL = os.getenv('BASE_AUTH_URL')
AWS_SECRETS_NAME = os.getenv('AWS_SECRETS_NAME')
CROPWISE_RS2_URL = os.getenv('CROPWISE_RS2_URL')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
CROPWISE_NIDERA_PASSWORD = os.getenv('CROPWISE_NIDERA_PASSWORD')
DD_LOGS_INJECTION = os.getenv('DD_LOGS_INJECTION')
DD_TAGS = os.getenv('DD_TAGS')
DD_TRACE_AGENT_URL = os.getenv('DD_TRACE_AGENT_URL')
