import os
import logging
import boto3
import uuid
import traceback
from botocore.exceptions import ClientError
from django.conf import settings
from django.utils import timezone
from urllib.parse import quote

logger = logging.getLogger(__name__)

def check_tigris_settings():
    """Check that all required Tigris settings are configured"""
    required_settings = [
        ('TIGRIS_ACCESS_KEY_ID', 'Tigris access key ID'),
        ('TIGRIS_SECRET_ACCESS_KEY', 'Tigris secret access key'),
        ('TIGRIS_STORAGE_BUCKET_NAME', 'Tigris bucket name'),
        ('TIGRIS_REGION_NAME', 'Tigris region'),
        ('TIGRIS_ENDPOINT_URL', 'Tigris endpoint URL')
    ]
    
    missing_settings = []
    
    for setting_name, description in required_settings:
        if not hasattr(settings, setting_name) or not getattr(settings, setting_name):
            missing_settings.append(description)
    
    if missing_settings:
        error_message = f"Missing required Tigris settings: {', '.join(missing_settings)}"
        logger.error(error_message)
        raise ValueError(error_message)
    
    return True

def print_tigris_settings():
    """Print Tigris settings for debugging (with credentials partially hidden)"""
    tigris_access_key = getattr(settings, 'TIGRIS_ACCESS_KEY_ID', 'Not set')
    tigris_secret = getattr(settings, 'TIGRIS_SECRET_ACCESS_KEY', 'Not set')
    bucket_name = getattr(settings, 'TIGRIS_STORAGE_BUCKET_NAME', 'Not set')
    region = getattr(settings, 'TIGRIS_REGION_NAME', 'Not set')
    endpoint_url = getattr(settings, 'TIGRIS_ENDPOINT_URL', 'Not set')
    custom_domain = getattr(settings, 'TIGRIS_S3_CUSTOM_DOMAIN', 'Not set')
    
    # Hide part of the credentials for security
    if tigris_access_key and len(tigris_access_key) > 4:
        safe_key = tigris_access_key[:4] + '*' * (len(tigris_access_key) - 4)
    else:
        safe_key = tigris_access_key
    
    if tigris_secret and len(tigris_secret) > 4:
        safe_secret = '*' * len(tigris_secret)
    else:
        safe_secret = tigris_secret
    
    settings_str = (
        f"\nTigris Settings:\n"
        f"  TIGRIS_ACCESS_KEY_ID: {safe_key}\n"
        f"  TIGRIS_SECRET_ACCESS_KEY: {safe_secret}\n"
        f"  TIGRIS_STORAGE_BUCKET_NAME: {bucket_name}\n"
        f"  TIGRIS_REGION_NAME: {region}\n"
        f"  TIGRIS_ENDPOINT_URL: {endpoint_url}\n"
        f"  TIGRIS_S3_CUSTOM_DOMAIN: {custom_domain}\n"
    )
    
    logger.info(settings_str)
    return settings_str

class TigrisClient:
    def __init__(self):
        logger.debug(f"Initializing TigrisClient with region: {settings.TIGRIS_REGION_NAME}, bucket: {settings.TIGRIS_STORAGE_BUCKET_NAME}, endpoint: {settings.TIGRIS_ENDPOINT_URL}")
        try:
            # Print Tigris settings
            print_tigris_settings()
            
            # Verify Tigris settings are configured
            check_tigris_settings()
            
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.TIGRIS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.TIGRIS_SECRET_ACCESS_KEY,
                region_name=settings.TIGRIS_REGION_NAME,
                endpoint_url=settings.TIGRIS_ENDPOINT_URL
            )
            self.bucket_name = settings.TIGRIS_STORAGE_BUCKET_NAME
            
            # Test connection
            self.s3_client.list_buckets()
            logger.info("S3 (Tigris) connection successful")
        except Exception as e:
            logger.error(f"Error initializing S3 (Tigris) client: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def generate_path(self, tenant_slug, file_type, module, filename):
        # Add timestamp or UUID to filename to prevent collisions
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        
        # Create the path following the structure: tenant/file_type/module/filename
        path = f"{tenant_slug}/{file_type}/{module}/{unique_filename}"
        
        logger.debug(f"Generated path: {path} from filename: {filename}")
        return path

    def upload_file(self, file_obj, object_name=None, extra_args=None):
        if object_name is None:
            object_name = file_obj.name
            
        # Ensure the object name doesn't start with a slash
        if object_name.startswith('/'):
            object_name = object_name[1:]
            
        try:
            args = extra_args or {}
            logger.debug(f"Uploading file to S3: {object_name} with args: {args}")
            
            # Use multipart upload for improved memory efficiency
            # This prevents loading the entire file into memory at once
            chunk_size = 5 * 1024 * 1024  # 5MB chunks (S3 minimum is 5MB)
            
            # Create a multipart upload
            mpu = self.s3_client.create_multipart_upload(
                Bucket=self.bucket_name,
                Key=object_name,
                **args
            )
            
            upload_id = mpu['UploadId']
            parts = []
            
            # Upload file in chunks
            part_number = 1
            
            try:
                # Handle both file-like objects and Django's UploadedFile
                file_obj.seek(0)
                
                while True:
                    # Read a chunk of data
                    chunk = file_obj.read(chunk_size)
                    if not chunk:
                        break
                    
                    # Upload the part
                    response = self.s3_client.upload_part(
                        Body=chunk,
                        Bucket=self.bucket_name,
                        Key=object_name,
                        PartNumber=part_number,
                        UploadId=upload_id
                    )
                    
                    # Add the part to our parts list
                    parts.append({
                        'PartNumber': part_number,
                        'ETag': response['ETag']
                    })
                    
                    part_number += 1
                    logger.debug(f"Uploaded part {part_number-1} of file {object_name}")
                
                # Complete the multipart upload
                self.s3_client.complete_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    UploadId=upload_id,
                    MultipartUpload={'Parts': parts}
                )
                
                logger.info(f"File {object_name} uploaded to S3 bucket {self.bucket_name} in {part_number-1} parts")
                return True
                
            except Exception as e:
                # Abort the multipart upload if something goes wrong
                logger.error(f"Error during multipart upload: {str(e)}")
                self.s3_client.abort_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    UploadId=upload_id
                )
                raise
                
        except ClientError as e:
            logger.error(f"S3 ClientError uploading file: {e}")
            logger.error(traceback.format_exc())
            return False
        except Exception as e:
            logger.error(f"Unexpected error uploading file to S3: {str(e)}")
            logger.error(traceback.format_exc())
            return False

    def download_file(self, object_name, file_path=None):
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
        try:
            logger.debug(f"Generating presigned URL for: {object_name} using Tigris endpoint")
            
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            logger.debug(f"Generated Tigris presigned URL: {response[:100]}...")
            return response
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None

    def list_files(self, prefix=''):
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

    def tenant_upload(self, file_obj, tenant_slug, file_type, module, extra_args=None):
        try:
            filename = getattr(file_obj, 'name', 'unnamed_file')
            logger.debug(f"Tenant upload for file: {filename}, tenant: {tenant_slug}, type: {file_type}, module: {module}")
            
            object_name = self.generate_path(tenant_slug, file_type, module, filename)
            
            # Set default content type based on file extension
            if extra_args is None:
                extra_args = {}
            
            if 'ContentType' not in extra_args:
                _, ext = os.path.splitext(filename)
                content_type = None
                
                # Set common MIME types
                if ext.lower() in ['.jpg', '.jpeg']:
                    content_type = 'image/jpeg'
                elif ext.lower() == '.png':
                    content_type = 'image/png'
                elif ext.lower() == '.pdf':
                    content_type = 'application/pdf'
                elif ext.lower() in ['.doc', '.docx']:
                    content_type = 'application/msword'
                elif ext.lower() in ['.xls', '.xlsx']:
                    content_type = 'application/vnd.ms-excel'
                
                if content_type:
                    extra_args['ContentType'] = content_type
                    logger.debug(f"Set content type to {content_type} for file with extension {ext}")
            
            logger.debug(f"Starting upload to S3 with object_name: {object_name}")
            success = self.upload_file(file_obj, object_name, extra_args)
            
            if success:
                presigned_url = self.generate_presigned_url(object_name)
                logger.info(f"Tenant upload successful for {object_name}")
                return {
                    'success': True,
                    'path': object_name,
                    'url': presigned_url
                }
            else:
                logger.error(f"Tenant upload failed for {object_name}")
                return {
                    'success': False,
                    'error': 'Failed to upload file'
                }
        except Exception as e:
            logger.error(f"Unexpected error in tenant_upload: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                'success': False,
                'error': f"Error: {str(e)}"
            }

    def tenant_list_files(self, tenant_slug, file_type=None, module=None):
        # Build the prefix based on provided parameters
        prefix = tenant_slug + '/'
        if file_type:
            prefix += file_type + '/'
            if module:
                prefix += module + '/'
        
        # Get files with the constructed prefix
        files = self.list_files(prefix=prefix)
        
        # Add presigned URLs to each file
        for file in files:
            file['url'] = self.generate_presigned_url(file['Key'])
            
            # Extract just the filename from the path
            file['filename'] = os.path.basename(file['Key'])
            
            # Add file_type and module if not explicitly provided
            if not file_type or not module:
                path_parts = file['Key'].split('/')
                if len(path_parts) >= 2 and not file_type:
                    file['file_type'] = path_parts[1]
                if len(path_parts) >= 3 and not module:
                    file['module'] = path_parts[2]
        
        return files

    def simple_upload(self, file_obj, object_name, extra_args=None):
        """A simpler upload method for small files that doesn't use multipart upload"""
        if object_name.startswith('/'):
            object_name = object_name[1:]
            
        try:
            args = extra_args or {}
            logger.info(f"Using simple upload for small file: {object_name}")
            
            # Reset file pointer to beginning
            file_obj.seek(0)
            
            # Get file size to log progress
            try:
                file_size = file_obj.size
                logger.info(f"File size: {file_size/1024/1024:.2f}MB")
            except AttributeError:
                file_size = None
                logger.info("File size unknown")
            
            # Stream directly to S3 using put_object to avoid loading entire file into memory
            logger.info(f"Uploading file directly to S3 using streaming")
            
            # Upload directly using the file object as a streaming body
            # This avoids reading the entire file content into memory
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_name,
                ExtraArgs=args
            )
            
            logger.info(f"Simple upload successful for {object_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error during simple upload: {str(e)}")
            logger.error(traceback.format_exc())
            return False 