import os
from dotenv import load_dotenv
import boto3



load_dotenv(dotenv_path=".env", override=True)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')        
AWS_REGION= os.getenv('AWS_REGION', 'AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)