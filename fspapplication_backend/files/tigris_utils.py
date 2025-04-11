import logging
from django.conf import settings
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError, BotoCoreError

logger = logging.getLogger(__name__)

def check_s3_settings():
    """Check if necessary Tigris S3 settings are configured."""
    required_settings = [
        ('TIGRIS_ACCESS_KEY_ID', 'Tigris access key ID'),
        ('TIGRIS_SECRET_ACCESS_KEY', 'Tigris secret access key'),
        ('TIGRIS_STORAGE_BUCKET_NAME', 'Tigris S3 bucket name'),
        ('TIGRIS_REGION_NAME', 'Tigris region'),
        ('TIGRIS_ENDPOINT_URL_S3', 'Tigris S3 endpoint URL'),
    ]
    missing = [name for var, name in required_settings if not hasattr(settings, var) or not getattr(settings, var)]
    if missing:
        logger.warning(f"Missing required Tigris S3 settings: {', '.join(missing)}")
    return missing

def get_s3_client():
    """Initializes and returns a boto3 S3 client configured for Tigris."""
    missing = check_s3_settings()
    if missing:
        error_msg = f"Missing Tigris S3 configuration: {', '.join(missing)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    region = getattr(settings, 'TIGRIS_REGION_NAME', None)
    endpoint_url = getattr(settings, 'TIGRIS_ENDPOINT_URL_S3', None)

    if not endpoint_url:
        error_msg = "TIGRIS_ENDPOINT_URL_S3 is not configured in settings."
        logger.error(error_msg)
        raise ValueError(error_msg)

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.TIGRIS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.TIGRIS_SECRET_ACCESS_KEY,
            region_name=region,
            endpoint_url=endpoint_url
        )
        # Test connection by listing buckets (requires appropriate permissions)
        # s3_client.list_buckets() # This might fail if ListBuckets isn't allowed
        logger.info(f"Attempting to connect to Tigris S3 endpoint: {endpoint_url}")
        # A safer test might be to check bucket existence later or use get_bucket_location
        return s3_client
    except (NoCredentialsError, PartialCredentialsError) as e:
        logger.error(f"Tigris S3 credentials error: {e}")
        raise ValueError("Tigris S3 credentials not found or incomplete.") from e
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        logger.error(f"Tigris S3 ClientError ({error_code}): {e}")
        if error_code == 'InvalidAccessKeyId' or error_code == 'SignatureDoesNotMatch':
            raise ValueError("Invalid Tigris S3 credentials provided.") from e
        elif 'EndpointConnectionError' in str(e):
             raise ValueError(f"Could not connect to the Tigris S3 endpoint: {endpoint_url}") from e
        # Re-raise other client errors
        raise
    except BotoCoreError as e:
        logger.error(f"Tigris S3 BotoCoreError: {e}")
        # Could be a configuration issue or network problem
        raise ValueError(f"BotoCoreError connecting to Tigris S3: {e}") from e
    except Exception as e:
        logger.error(f"An unexpected error occurred during Tigris S3 client initialization: {e}")
        raise

def get_s3_configuration_details():
    """Returns a dictionary with Tigris S3 configuration details (masking sensitive info)."""
    details = {}
    config_vars = [
        'TIGRIS_ACCESS_KEY_ID',
        'TIGRIS_SECRET_ACCESS_KEY',
        'TIGRIS_STORAGE_BUCKET_NAME',
        'TIGRIS_REGION_NAME',
        'TIGRIS_ENDPOINT_URL_S3',
        'TIGRIS_DEFAULT_ACL',
        'TIGRIS_S3_OBJECT_PARAMETERS', # Added this one
    ]
    for var in config_vars:
        val = getattr(settings, var, 'Not set')
        # Mask sensitive keys
        if 'KEY_ID' in var and isinstance(val, str) and len(val) > 4:
            safe_val = f"{val[:4]}****"
        elif 'SECRET_KEY' in var and val != 'Not set':
             safe_val = "****"
        else:
            safe_val = val # Keep bucket names, region, endpoint, ACL, params as is
        details[var] = safe_val
    return details

class TigrisClient:
    def __init__(self):
        """Initializes the TigrisClient with S3 configuration from Django settings."""
        missing = check_s3_settings()
        if missing:
            config_details = get_s3_configuration_details()
            details_str = "\n".join([f"  {k}: {v}" for k, v in config_details.items()])
            error_message = (
                f"Missing or invalid Tigris S3 configuration: {', '.join(missing)}.\n"
                f"Current settings (sensitive info masked):\n{details_str}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

        self.region = getattr(settings, 'TIGRIS_REGION_NAME', None)
        self.endpoint_url = getattr(settings, 'TIGRIS_ENDPOINT_URL_S3', None)
        self.bucket_name = settings.TIGRIS_STORAGE_BUCKET_NAME
        self.default_acl = getattr(settings, 'TIGRIS_DEFAULT_ACL', 'private')
        # Use TIGRIS_S3_OBJECT_PARAMETERS if defined, otherwise AWS_S3_OBJECT_PARAMETERS
        # Ensure AWS_S3_OBJECT_PARAMETERS is defined in settings if TIGRIS_ version isn't
        self.object_parameters = getattr(settings, 'TIGRIS_S3_OBJECT_PARAMETERS', 
                                         getattr(settings, 'AWS_S3_OBJECT_PARAMETERS', {})) 

        logger.debug(f"Initializing TigrisClient - Region: {self.region}, Bucket: {self.bucket_name}, Endpoint: {self.endpoint_url}, Default ACL: {self.default_acl}, Object Params: {self.object_parameters}")

        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.TIGRIS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.TIGRIS_SECRET_ACCESS_KEY,
                region_name=self.region,
                endpoint_url=self.endpoint_url
                # Consider adding config=botocore.config.Config(signature_version='s3v4') if needed
            )
            # Verify connection by trying to get bucket location or head_bucket
            # This requires appropriate permissions on the bucket
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Successfully connected to Tigris bucket: {self.bucket_name} at {self.endpoint_url}")

        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.error(f"Tigris S3 credentials error during client init: {e}")
            raise ValueError("Tigris S3 credentials not found or incomplete.") from e
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            error_message_detail = str(e)
            error_message = f"Tigris S3 ClientError ({error_code}) connecting to bucket '{self.bucket_name}': {error_message_detail}"
            
            if error_code == 'InvalidAccessKeyId' or error_code == 'SignatureDoesNotMatch':
                 error_message = f"Invalid Tigris S3 credentials provided. Check TIGRIS_ACCESS_KEY_ID and TIGRIS_SECRET_ACCESS_KEY. Error: {error_message_detail}"
                 logger.error(error_message)
                 raise ValueError(error_message) from e
            elif error_code == 'NoSuchBucket':
                error_message = f"Tigris S3 bucket '{self.bucket_name}' not found at endpoint {self.endpoint_url}. Please ensure it exists and is accessible with the provided credentials. Error: {error_message_detail}"
                logger.error(error_message)
                raise ValueError(error_message) from e
            elif error_code == 'AccessDenied' or error_code == 'Forbidden':
                 error_message = f"Access Denied connecting to Tigris bucket '{self.bucket_name}'. Check bucket permissions for the provided credentials. Error: {error_message_detail}"
                 logger.error(error_message)
                 raise PermissionError(error_message) from e
            elif 'EndpointConnectionError' in str(e) or error_code == 'EndpointConnectionError':
                 error_message = f"Could not connect to the Tigris S3 endpoint: {self.endpoint_url}. Check network connectivity and endpoint URL. Error: {error_message_detail}"
                 logger.error(error_message)
                 raise ConnectionError(error_message) from e
            else:
                 # Log the full error for unexpected ClientErrors
                 logger.error(error_message)
                 raise # Re-raise the original ClientError
        except BotoCoreError as e:
             error_message = f"Tigris S3 BotoCoreError during client init: {e}"
             logger.error(error_message)
             raise ConnectionError(error_message) from e # Treat as connection/config issue
        except Exception as e:
             # Catch any other unexpected exceptions during initialization
             error_message = f"An unexpected error occurred during TigrisClient initialization: {e.__class__.__name__}: {e}"
             logger.exception(error_message) # Log with traceback
             raise RuntimeError(error_message) from e # Wrap in a generic runtime error


    def upload_file(self, file_obj, object_name=None, acl=None, content_type=None, extra_args=None):
        """Upload a file to the Tigris S3 bucket."""
        if object_name is None:
            object_name = os.path.basename(getattr(file_obj, 'name', 'uploaded_file'))
        
        # Remove leading slash if present
        if object_name.startswith('/'):
            object_name = object_name[1:]
            
        acl_to_use = acl if acl is not None else self.default_acl
        
        # Combine default object parameters with any specific extra_args provided
        final_extra_args = self.object_parameters.copy()
        final_extra_args['ACL'] = acl_to_use
        
        if content_type:
            final_extra_args['ContentType'] = content_type
        elif hasattr(file_obj, 'content_type'): # Handle Django UploadedFile
            final_extra_args['ContentType'] = file_obj.content_type

        # Merge explicitly passed extra_args, allowing them to override defaults
        if extra_args:
            final_extra_args.update(extra_args)

        logger.debug(f"Attempting to upload '{object_name}' to bucket '{self.bucket_name}' with ExtraArgs: {final_extra_args}")

        try:
            # Ensure file cursor is at the beginning
            if hasattr(file_obj, 'seek') and callable(file_obj.seek):
                file_obj.seek(0)
            else:
                 logger.warning(f"File object for '{object_name}' might not be seekable.")

            response = self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_name,
                ExtraArgs=final_extra_args # Pass the combined args here
            )
            logger.info(f"Successfully uploaded '{object_name}' to '{self.bucket_name}'.")
            
            # Construct the object URL using the endpoint
            endpoint_base = self.endpoint_url
            if not endpoint_base.startswith('https://'):
                endpoint_base = f'https://{endpoint_base}' 
            endpoint_base = endpoint_base.rstrip('/')
            object_url = f"{endpoint_base}/{self.bucket_name}/{object_name}"
            logger.debug(f"Constructed object URL: {object_url}")

            return object_url
        except ClientError as e:
            logger.error(f"Failed to upload '{object_name}' to '{self.bucket_name}': {e}")
            raise # Re-raise the client error
        except Exception as e:
            logger.exception(f"An unexpected error occurred during file upload of '{object_name}': {e}")
            raise # Re-raise the unexpected error

    def delete_file(self, object_name):
        """Delete a file from the Tigris S3 bucket."""
        # Remove leading slash if present
        if object_name.startswith('/'):
            object_name = object_name[1:]
            
        logger.debug(f"Attempting to delete '{object_name}' from bucket '{self.bucket_name}'")
        try:
            response = self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            logger.info(f"Successfully submitted delete request for '{object_name}' from '{self.bucket_name}'. Response status: {response.get('ResponseMetadata', {}).get('HTTPStatusCode')}")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete '{object_name}' from '{self.bucket_name}': {e}")
            return False
        except Exception as e:
            logger.exception(f"An unexpected error occurred during file deletion of '{object_name}': {e}")
            return False

    def generate_presigned_url(self, object_name, expiration=3600, http_method='GET'):
        """Generate a presigned URL to access an object in the bucket."""
        # Remove leading slash if present
        if object_name.startswith('/'):
            object_name = object_name[1:]
            
        logger.debug(f"Generating {http_method} presigned URL for '{object_name}' in bucket '{self.bucket_name}' (expires in {expiration}s)")
        
        client_method_map = {
            'GET': 'get_object',
            'PUT': 'put_object',
            'DELETE': 'delete_object',
            'HEAD': 'head_object',
        }
        client_method = client_method_map.get(http_method.upper())
        if not client_method:
             logger.error(f"Unsupported HTTP method '{http_method}' for presigned URL generation.")
             return None
             
        params = {'Bucket': self.bucket_name, 'Key': object_name}

        try:
            url = self.s3_client.generate_presigned_url(
                ClientMethod=client_method,
                Params=params,
                ExpiresIn=expiration,
                HttpMethod=http_method.upper()
            )
            logger.info(f"Generated {http_method} presigned URL for '{object_name}' expiring in {expiration}s.")
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL for '{object_name}': {e}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred generating presigned URL for '{object_name}': {e}")
            return None

    def get_public_url(self, object_name):
        """Generate a public URL for an object (assumes public accessibility)."""
        if not self.endpoint_url or not self.bucket_name:
            logger.warning("Cannot generate public URL without endpoint_url and bucket_name configured.")
            return None
            
        # Remove leading slash if present
        if object_name.startswith('/'):
            object_name = object_name[1:]

        endpoint_base = self.endpoint_url
        if not endpoint_base.startswith('https://'):
             endpoint_base = f'https://{endpoint_base}'
        endpoint_base = endpoint_base.rstrip('/')

        # Construct the URL (assuming path-style access)
        public_url = f"{endpoint_base}/{self.bucket_name}/{object_name}"
        logger.debug(f"Generated potential public URL for '{object_name}': {public_url}")
        return public_url

# Example Usage Block (remains largely the same, ensure it uses the updated client methods)
# ... (rest of the file including __main__ block) ...
# Make sure the __main__ block calls the updated methods correctly if used for testing
# Example adjustment within __main__ if needed:
# upload_url = client.upload_file(dummy_file_obj, 
#                                 object_name=test_object_name, 
#                                 acl='public-read', # Example ACL
#                                 content_type='text/plain') # Example content type
# presigned_get_url = client.generate_presigned_url(test_object_name, expiration=60, http_method='GET') 

# Example Usage (optional, for testing)
if __name__ == '__main__':
    # This block will only run if the script is executed directly
    # Requires Django settings to be configured (e.g., via manage.py shell or environment setup)
    # You might need to mock settings or run within a Django context for this to work
    
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.getLogger('boto3').setLevel(logging.INFO)
    logging.getLogger('botocore').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.INFO)

    print("--- Tigris S3 Utility Test --- (Requires Django settings loaded)")
    
    try:
        print("\n1. Checking S3 settings...")
        missing_settings = check_s3_settings()
        if missing_settings:
            print(f"   Result: Missing settings: {', '.join(missing_settings)}")
            config = get_s3_configuration_details()
            print("   Current Config:")
            for k, v in config.items():
                print(f"     {k}: {v}")
        else:
            print("   Result: All required Tigris settings seem present.")
            config = get_s3_configuration_details()
            print("   Current Config:")
            for k, v in config.items():
                print(f"     {k}: {v}")

        print("\n2. Initializing TigrisClient...")
        client = TigrisClient()
        print("   Result: TigrisClient initialized successfully.")

        # Example: Upload a dummy file
        print("\n3. Uploading a test file (dummy.txt)...")
        from io import BytesIO
        dummy_file_content = b"This is a test file for Tigris S3 upload."
        dummy_file_obj = BytesIO(dummy_file_content)
        dummy_file_obj.name = "dummy.txt" # Provide a name attribute
        upload_url = client.upload_file(dummy_file_obj, object_name="test/dummy.txt")
        if upload_url:
            print(f"   Result: Upload successful. Object URL: {upload_url}")

            # Example: Generate presigned URL
            print("\n4. Generating presigned URL for test/dummy.txt...")
            presigned_url = client.generate_presigned_url("test/dummy.txt")
            if presigned_url:
                print(f"   Result: Presigned URL: {presigned_url}")
            else:
                print("   Result: Failed to generate presigned URL.")
            
            # Example: Generate public URL (assuming public read - less common for Tigris)
            print("\n5. Generating public URL for test/dummy.txt...")
            public_url = client.get_public_url("test/dummy.txt")
            if public_url:
                 print(f"   Result: Public URL: {public_url}")
            else:
                print("   Result: Could not generate public URL (check endpoint/bucket config).")

            # Example: Delete the test file
            print("\n6. Deleting test file test/dummy.txt...")
            delete_success = client.delete_file("test/dummy.txt")
            print(f"   Result: Deletion {'successful' if delete_success else 'failed'}.")
        else:
            print("   Result: Upload failed.")

    except ValueError as e:
        print(f"\n*** Configuration Error: {e} ***")
    except Exception as e:
        print(f"\n*** An unexpected error occurred: {e} ***")
        import traceback
        traceback.print_exc() 