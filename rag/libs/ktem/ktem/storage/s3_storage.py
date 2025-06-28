import mimetypes
import os

import boto3
from botocore.exceptions import ClientError
from theflow.settings import settings as flowsettings


class S3Storage:
    def __init__(self, prefix):
        self.bucket_name = flowsettings.KH_S3_BUCKET_NAME
        self.region = flowsettings.KH_S3_REGION
        self.prefix = prefix

        self.s3_client = boto3.client(
            's3',
            region_name=self.region,
            aws_access_key_id=flowsettings.KH_S3_ACCESS_KEY,
            aws_secret_access_key=flowsettings.KH_S3_SECRET_KEY
        )

    def upload_file(self, file_path, file_hash):
        """Upload a file to S3 bucket"""

        # Get MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"  # Default if unknown
        file_extension = os.path.splitext(file_path)[1]
        s3_key = f"{self.prefix}/{file_hash}{file_extension}"

        try:
            with open(file_path, 'rb') as file_data:
                self.s3_client.upload_fileobj(
                    file_data,
                    self.bucket_name,
                    s3_key,
                    ExtraArgs={'ACL': 'public-read', 'ContentType': mime_type}
                )
                print("s3 key:::", s3_key)
            return s3_key
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            raise

    def download_file(self, file_hash, local_path):
        """Download a file from S3 bucket to local path"""
        s3_key = f"{self.prefix}{file_hash}"

        try:
            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
            return local_path
        except ClientError as e:
            print(f"Error downloading file from S3: {e}")
            raise

    def get_file_url(self, file_hash, expiration=3600):
        """Generate a presigned URL for the file"""
        s3_key = f"{self.prefix}{file_hash}"

        try:
            # Todo fix
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            print("s3 url", url)
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            raise

    def delete_file(self, file_hash):
        """Delete a file from S3 bucket"""
        s3_key = f"{self.prefix}{file_hash}"

        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
        except ClientError as e:
            print(f"Error deleting file from S3: {e}")
            raise
