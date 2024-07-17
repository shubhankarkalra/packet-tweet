import boto3
import os
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

s3_client = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

def upload_to_public_url(file_path):
    """
    Uploads a file to S3 and returns its public URL.
    """
    bucket_name = os.getenv('S3_BUCKET_NAME')
    if not bucket_name:
        logger.error("S3_BUCKET_NAME environment variable is not set")
        return None

    object_name = os.path.basename(file_path)
    
    try:
        s3_client.upload_file(
            file_path, 
            bucket_name, 
            object_name, 
            ExtraArgs={'ACL': 'public-read'}
        )
        logger.info(f"File uploaded successfully to {bucket_name}/{object_name}")
    except ClientError as e:
        logger.error(f"Error uploading file to S3: {e}")
        return None

    # Construct the public URL
    public_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    return public_url