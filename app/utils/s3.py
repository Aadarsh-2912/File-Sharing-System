import os
import boto3
from botocore.exceptions import NoCredentialsError

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")

s3_client = boto3.client(
    "s3",
    region_name=AWS_S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def upload_file_to_s3(file_obj, filename, content_type):
    try:
        s3_client.upload_fileobj(
            file_obj,
            AWS_S3_BUCKET_NAME,
            filename,
            ExtraArgs={"ContentType": content_type}
        )
        return True
    except NoCredentialsError:
        return False

def generate_presigned_url(filename, expiration=3600):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": AWS_S3_BUCKET_NAME, "Key": filename},
        ExpiresIn=expiration
    ) 