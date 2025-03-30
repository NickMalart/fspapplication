import os
import logging
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.utils import timezone
from urllib.parse import quote

logger = logging.getLogger(__name__)

class S3Client:
    """
    Utility class for AWS S3 operations.
    """
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file_obj, object_name=None, extra_args=None):
        """
        Upload a file to an S3 bucket
        
        :param file_obj: File to upload
        :param object_name: S3 object name. If not specified, file_obj.name is used
        :param extra_args: Optional parameters to define file properties
        :return: True if file was uploaded, else False
        """
        if object_name is None:
            object_name = file_obj.name
            
        # Ensure the object name doesn't start with a slash
        if object_name.startswith('/'):
            object_name = object_name[1:]
            
        try:
            args = extra_args or {}
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, object_name, ExtraArgs=args)
            logger.info(f"File {object_name} uploaded to S3 bucket {self.bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
            return False

    def download_file(self, object_name, file_path=None):
        """
        Download a file from an S3 bucket
        
        :param object_name: S3 object name
        :param file_path: Local path where the file will be saved
        :return: True if file was downloaded, else False
        """
        if file_path is None:
            file_path = os.path.basename(object_name)
            
        try:
            with open(file_path, 'wb') as f:
                self.s3_client.download_fileobj(self.bucket_name, object_name, f)
            logger.info(f"File {object_name} downloaded from S3 bucket {self.bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Error downloading file from S3: {e}")
            return False

    def generate_presigned_url(self, object_name, expiration=3600):
        """
        Generate a presigned URL to share an S3 object
        
        :param object_name: S3 object name
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None

    def list_files(self, prefix=''):
        """
        List files in the S3 bucket with an optional prefix
        
        :param prefix: Prefix to filter files by
        :return: List of file objects
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            files = response.get('Contents', [])
            return files
        except ClientError as e:
            logger.error(f"Error listing files in S3: {e}")
            return []

    def delete_file(self, object_name):
        """
        Delete a file from the S3 bucket
        
        :param object_name: S3 object name to delete
        :return: True if file was deleted, else False
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_name
            )
            logger.info(f"File {object_name} deleted from S3 bucket {self.bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {e}")
            return False 