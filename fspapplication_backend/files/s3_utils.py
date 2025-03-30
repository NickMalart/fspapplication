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

def check_aws_settings():
    """Check that all required AWS settings are configured"""
    required_settings = [
        ('AWS_ACCESS_KEY_ID', 'AWS access key ID'),
        ('AWS_SECRET_ACCESS_KEY', 'AWS secret access key'),
        ('AWS_STORAGE_BUCKET_NAME', 'S3 bucket name'),
        ('AWS_S3_REGION_NAME', 'AWS region')
    ]
    
    missing_settings = []
    
    for setting_name, description in required_settings:
        if not hasattr(settings, setting_name) or not getattr(settings, setting_name):
            missing_settings.append(description)
    
    if missing_settings:
        error_message = f"Missing required AWS settings: {', '.join(missing_settings)}"
        logger.error(error_message)
        raise ValueError(error_message)
    
    # Special check for region name to ensure it's not a placeholder
    if hasattr(settings, 'AWS_S3_REGION_NAME'):
        region = getattr(settings, 'AWS_S3_REGION_NAME')
        if region == 'your-region-name' or 'your-region' in region or 'region' in region.lower():
            error_message = f"Invalid AWS region name: '{region}'. Please set a valid AWS region like 'us-east-1' or 'ap-southeast-2'."
            logger.error(error_message)
            raise ValueError(error_message)
    
    return True

def print_aws_settings():
    """Print AWS settings for debugging (with credentials partially hidden)"""
    aws_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', 'Not set')
    aws_secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', 'Not set')
    bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not set')
    region = getattr(settings, 'AWS_S3_REGION_NAME', 'Not set')
    cloudfront_domain = getattr(settings, 'CLOUDFRONT_DOMAIN', 'Not set')
    
    # Hide part of the credentials for security
    if aws_access_key and len(aws_access_key) > 4:
        safe_key = aws_access_key[:4] + '*' * (len(aws_access_key) - 4)
    else:
        safe_key = aws_access_key
    
    if aws_secret and len(aws_secret) > 4:
        safe_secret = '*' * len(aws_secret)
    else:
        safe_secret = aws_secret
    
    settings_str = (
        f"\nAWS Settings:\n"
        f"  AWS_ACCESS_KEY_ID: {safe_key}\n"
        f"  AWS_SECRET_ACCESS_KEY: {safe_secret}\n"
        f"  AWS_STORAGE_BUCKET_NAME: {bucket_name}\n"
        f"  AWS_S3_REGION_NAME: {region}\n"
        f"  CLOUDFRONT_DOMAIN: {cloudfront_domain}\n"
    )
    
    logger.info(settings_str)
    return settings_str

class S3Client:
    def __init__(self):
        logger.debug(f"Initializing S3Client with region: {settings.AWS_S3_REGION_NAME}, bucket: {settings.AWS_STORAGE_BUCKET_NAME}")
        try:
            # Print AWS settings
            print_aws_settings()
            
            # Verify AWS settings are configured
            check_aws_settings()
            
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            
            # Set CloudFront domain if available
            self.use_cloudfront = hasattr(settings, 'CLOUDFRONT_DOMAIN') and settings.CLOUDFRONT_DOMAIN
            self.cloudfront_domain = getattr(settings, 'CLOUDFRONT_DOMAIN', None)
            
            # Test connection
            self.s3_client.list_buckets()
            logger.info("S3 connection successful")
            if self.use_cloudfront:
                logger.info(f"Using CloudFront domain: {self.cloudfront_domain}")
        except Exception as e:
            logger.error(f"Error initializing S3 client: {str(e)}")
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
            
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, object_name, ExtraArgs=args)
            logger.info(f"File {object_name} uploaded to S3 bucket {self.bucket_name}")
            return True
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
            logger.debug(f"Generating URL for: {object_name}")
            
            # If CloudFront is configured, use CloudFront URL instead of S3 presigned URL
            if self.use_cloudfront and self.cloudfront_domain:
                # For CloudFront, we use the direct path without presigning
                cf_url = f"https://{self.cloudfront_domain}/{object_name}"
                logger.debug(f"Generated CloudFront URL: {cf_url}")
                return cf_url
            else:
                # Fall back to S3 presigned URL if CloudFront is not configured
                logger.debug(f"CloudFront not configured, generating S3 presigned URL")
                response = self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': self.bucket_name,
                        'Key': object_name
                    },
                    ExpiresIn=expiration
                )
                logger.debug(f"Generated S3 presigned URL: {response[:100]}...")
                return response
        except ClientError as e:
            logger.error(f"Error generating URL: {e}")
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