from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import get_object_or_404
import logging
import traceback
import os
import sys
import boto3
from django.conf import settings
import uuid
import re

from .models import FileUpload
from .serializers import FileUploadSerializer, FileUploadCreateSerializer
from .tigris_utils import TigrisClient, get_s3_configuration_details, check_s3_settings

# Configure logger
logger = logging.getLogger(__name__)

def get_s3_connection_status():
    """Check the connection to S3 and bucket existence."""
    status = {
        'env_vars_set': {},
        'settings_loaded': {},
        's3_connection_successful': False,
        's3_bucket_exists': False,
        's3_connection_test': "",
        'error': None
    }

    # 1. Check environment variables
    env_vars = [
        'TIGRIS_ACCESS_KEY_ID',
        'TIGRIS_SECRET_ACCESS_KEY',
        'TIGRIS_STORAGE_BUCKET_NAME',
        'TIGRIS_REGION_NAME',
        'TIGRIS_ENDPOINT_URL_S3'
    ]
    for var in env_vars:
        status['env_vars_set'][var] = os.environ.get(var, 'Not set in env')

    # 2. Check Django settings
    settings_vars = [
        'TIGRIS_ACCESS_KEY_ID',
        'TIGRIS_SECRET_ACCESS_KEY',
        'TIGRIS_STORAGE_BUCKET_NAME',
        'TIGRIS_REGION_NAME',
        'TIGRIS_ENDPOINT_URL_S3',
        'TIGRIS_DEFAULT_ACL'
    ]
    for var in settings_vars:
        val = getattr(settings, var, 'Not set in settings')
        # Mask sensitive keys
        if 'KEY' in var and isinstance(val, str) and len(val) > 4:
            val = val[:4] + '****'
        status['settings_loaded'][var] = val

    # 3. Test S3 Connection and Bucket Existence
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.TIGRIS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.TIGRIS_SECRET_ACCESS_KEY,
            region_name=settings.TIGRIS_REGION_NAME,
            endpoint_url=settings.TIGRIS_ENDPOINT_URL_S3 # Use the Tigris endpoint
        )
        
        # Test connection by listing buckets
        response = s3_client.list_buckets()
        status['s3_connection_successful'] = True
        status['s3_connection_test'] = "Successfully connected to Tigris S3 and listed buckets."
        logger.info("Tigris S3 connection successful.")

        # Check if the specific bucket exists
        bucket_names = [bucket['Name'] for bucket in response.get('Buckets', [])]
        if settings.TIGRIS_STORAGE_BUCKET_NAME in bucket_names:
            status['s3_bucket_exists'] = True
            status['s3_connection_test'] += f" Bucket '{settings.TIGRIS_STORAGE_BUCKET_NAME}' exists."
            logger.info(f"Tigris S3 bucket '{settings.TIGRIS_STORAGE_BUCKET_NAME}' found.")
        else:
            status['s3_connection_test'] += f" Bucket '{settings.TIGRIS_STORAGE_BUCKET_NAME}' NOT found."
            logger.warning(f"Tigris S3 bucket '{settings.TIGRIS_STORAGE_BUCKET_NAME}' not found.")

    except Exception as e:
        error_message = f"Unexpected error connecting to S3: {e}"
        status['error'] = error_message
        status['s3_connection_test'] = error_message
        logger.error(error_message)

    return status

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def options(self, request, *args, **kwargs):
        # Handle CORS preflight requests (though django-cors-headers is preferred)
        response = Response(status=status.HTTP_200_OK)
        # Headers will be added by middleware or django-cors-headers
        return response
    
    def post(self, request):
        logger.info(f"FileUploadView POST request received from user {request.user.pk}")
        tenant = request.tenant # Assumes tenant middleware is active
        if not tenant:
             logger.error("Tenant context not found in request.")
             return Response({'error': 'Tenant context required.'}, status=status.HTTP_400_BAD_REQUEST)
             
        logger.debug(f"Tenant: {tenant}, Request data: {request.data}")
            
        serializer = FileUploadCreateSerializer(data=request.data)
            
        if not serializer.is_valid():
            logger.warning(f"FileUploadCreateSerializer validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        logger.info("Serializer validation passed.")
        file_obj = serializer.validated_data['file']
        file_type = serializer.validated_data['file_type']
        module = serializer.validated_data['module']
                
        # Construct a unique object name within the tenant's structure
        original_filename = file_obj.name
        name, ext = os.path.splitext(original_filename)
        # Ensure filename is safe (e.g., replace spaces, problematic chars)
        safe_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', name)
        unique_suffix = uuid.uuid4().hex[:8]
        unique_filename = f"{safe_name}_{unique_suffix}{ext}"
        
        # Determine tenant identifier for path construction
        # Prioritize schema_name, fall back to other safe attributes
        tenant_identifier = None
        if hasattr(tenant, 'schema_name') and tenant.schema_name:
            tenant_identifier = tenant.schema_name
        else:
            tenant_identifier = f"tenant_{tenant.pk}" # Fallback to PK
            logger.warning(f"Tenant {tenant.pk} has no schema_name, using PK for path.")

        object_name = f"{tenant_identifier}/{file_type}/{module}/{unique_filename}"
        logger.debug(f"Generated object name: {object_name}")
                
        try:
            tigris_client = TigrisClient() # Initialize Tigris client
            logger.info("Initialized TigrisClient successfully.")

            # Upload using the Tigris client
            # Pass content_type explicitly if available and reliable
            content_type = getattr(file_obj, 'content_type', None)
            upload_url = tigris_client.upload_file(
                 file_obj=file_obj,
                 object_name=object_name,
                 # acl=tigris_client.default_acl, # Use default ACL from client/settings
                 content_type=content_type
             )
            logger.info(f"Tigris upload completed for {object_name}. URL: {upload_url}")

            # Create database record upon successful upload
            file_upload = FileUpload.objects.create(
                 tenant=tenant,
                 path=object_name, # Store the object name/key
                 original_filename=original_filename,
                 file_type=file_type,
                 module=module,
                 content_type=content_type,
                 file_size=file_obj.size,
                 created_by=request.user
             )
            logger.info(f"Created FileUpload record ID {file_upload.id} for {object_name}")

            # Return data using the main serializer
            response_serializer = FileUploadSerializer(file_upload)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except (ValueError, ConnectionError, PermissionError) as e:
             # Catch specific errors from TigrisClient initialization or upload
             logger.error(f"Tigris configuration or connection error: {e}")
             return Response({'error': f'Storage configuration error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
             # Catch unexpected errors during the process
             logger.exception(f"Unexpected error during file upload for tenant {tenant_identifier}: {e}")
             return Response({'error': 'An unexpected server error occurred during upload.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tenant = request.tenant
        if not tenant:
             return Response({'error': 'Tenant context required.'}, status=status.HTTP_400_BAD_REQUEST)
             
        file_type = request.query_params.get('file_type')
        module = request.query_params.get('module')
        
        # Filter by tenant (mandatory)
        queryset = FileUpload.objects.filter(tenant=tenant)
        
        # Apply optional filters
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        if module:
            queryset = queryset.filter(module=module)
            
        queryset = queryset.order_by('-created_at') # Order by most recent
        
        # Use the serializer that generates access URLs
        serializer = FileUploadSerializer(queryset, many=True)
        # Note: This generates a presigned URL for *every* file in the list.
        # Consider pagination or alternative approaches if performance is an issue.
        logger.info(f"Returning list of {queryset.count()} files for tenant {tenant.pk}")
        return Response({'files': serializer.data})


class FileDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        tenant = request.tenant
        if not tenant:
             return Response({'error': 'Tenant context required.'}, status=status.HTTP_400_BAD_REQUEST)
             
        # Get path from request data (consider using URL parameter pk/path instead)
        path = request.data.get('path') 
        if not path:
            return Response({'error': 'File path ("path") is required in request body.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Find the file record ensuring it belongs to the requesting tenant
        try:
            file_upload = FileUpload.objects.get(tenant=tenant, path=path)
            logger.info(f"Found FileUpload record ID {file_upload.id} for path {path}")
        except FileUpload.DoesNotExist:
            logger.warning(f"File not found for tenant {tenant.pk} with path {path}")
            return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Attempt to delete from Tigris storage
        try:
            tigris_client = TigrisClient()
            logger.info(f"Attempting deletion of object {path} from Tigris bucket {tigris_client.bucket_name}")
            delete_successful = tigris_client.delete_file(path)
            
            if delete_successful:
                logger.info(f"Successfully deleted object {path} from Tigris.")
                # Delete the database record *after* successful storage deletion
                file_upload_id = file_upload.id
                file_upload.delete()
                logger.info(f"Deleted FileUpload record ID {file_upload_id}.")
                return Response({'success': True, 'message': 'File deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                # If delete_file returned False (e.g., ClientError)
                logger.error(f"TigrisClient failed to delete object {path}. Check Tigris logs.")
                # Consider if the DB record should be deleted even if storage fails
                return Response({'error': 'Failed to delete file from storage. Check logs.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (ValueError, ConnectionError, PermissionError) as e:
             logger.error(f"Tigris configuration or connection error during delete: {e}")
             return Response({'error': f'Storage configuration error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.exception(f"Unexpected error deleting file {path} for tenant {tenant.pk}: {e}")
            return Response({'error': 'An unexpected server error occurred during deletion.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tenant = request.tenant
        if not tenant:
             return Response({'error': 'Tenant context required.'}, status=status.HTTP_400_BAD_REQUEST)
             
        path = request.query_params.get('path')
        if not path:
            return Response({'error': 'File path ("path") query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Optional: Verify the file exists in the DB for this tenant before generating URL
        # This adds a DB query but prevents generating URLs for invalid paths
        try:
           file_exists = FileUpload.objects.filter(tenant=tenant, path=path).exists()
           if not file_exists:
               logger.warning(f"Download URL requested for non-existent or non-tenant file: {path}")
               return Response({'error': 'File not found or access denied.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as db_exc:
             logger.error(f"Database error checking file existence for path {path}: {db_exc}")
             # Proceed cautiously or return an error depending on policy

        # Generate presigned URL using TigrisClient
        try:
            tigris_client = TigrisClient()
            expiration = int(request.query_params.get('expiration', 3600)) # Default 1 hour
            logger.info(f"Generating presigned URL for path: {path}, expiration: {expiration}s")
            url = tigris_client.generate_presigned_url(path, expiration=expiration, http_method='GET')
            
            if url:
                logger.info(f"Successfully generated presigned URL for {path}")
                response_data = {
                    'success': True,
                    'url': url,
                    'path': path,
                    'expires_in_seconds': expiration
                }
                # Note: CORS headers should be handled by middleware (like django-cors-headers)
                # or the custom middleware if still in use.
                return Response(response_data)
            else:
                logger.error(f"TigrisClient failed to generate presigned URL for {path}. Check Tigris logs.")
                return Response({'error': 'Could not generate download URL for the file.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (ValueError, ConnectionError, PermissionError) as e:
             logger.error(f"Tigris configuration or connection error generating URL: {e}")
             return Response({'error': f'Storage configuration error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.exception(f"Unexpected error generating download URL for {path}: {e}")
            return Response({'error': 'An unexpected server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TigrisDiagnosticView(APIView):
    """View for diagnosing Tigris S3 connection and configuration issues."""
    # Typically requires admin or superuser permissions
    permission_classes = [IsAuthenticated] # Adjust permissions as needed (e.g., IsAdminUser) 
    
    def get(self, request):
        logger.info(f"TigrisDiagnosticView requested by user {request.user.pk}")
        diagnostic_data = {
            'service': 'Tigris Object Storage',
            'python_version': sys.version,
            'boto3_version': boto3.__version__,
            'django_storages_version': self._get_package_version('django-storages'),
            'settings_config (masked)': {},
            'tigris_client_init_status': 'Not Attempted',
            'tigris_client_init_error': None,
            'head_bucket_status': 'Not Attempted',
            'head_bucket_error': None,
            'example_presigned_url_status': 'Not Attempted',
            'example_presigned_url_error': None,
            'example_public_url': None, # Include if relevant
            'recommendations': []
        }

        # 1. Check Settings Configuration
        diagnostic_data['settings_config (masked)'] = get_s3_configuration_details()
        missing_settings = check_s3_settings() # Uses the helper from tigris_utils
        if missing_settings:
             diagnostic_data['recommendations'].append(f"Missing required settings: {missing_settings}. Check .env and settings.py.")
             # Return early if critical settings are missing? Maybe not, let other checks run.

        # 2. Attempt to Initialize TigrisClient
        try:
            client = TigrisClient() # This performs initial checks including head_bucket
            diagnostic_data['tigris_client_init_status'] = 'Success'
            diagnostic_data['head_bucket_status'] = 'Success (Verified by TigrisClient init)'
            logger.info("TigrisDiagnosticView: TigrisClient initialized successfully.")

            # 3. Attempt to Generate Example URLs (if client init succeeded)
            test_object_name = f"diagnostic_test_{uuid.uuid4().hex[:6]}.txt"
            try:
                presigned_url = client.generate_presigned_url(test_object_name, expiration=60)
                if presigned_url:
                    diagnostic_data['example_presigned_url_status'] = f'Success (URL generated for non-existent object \'{test_object_name}\')' # Escaped braces
                    logger.info(f"TigrisDiagnosticView: Generated example presigned URL for {test_object_name}")
                else:
                    diagnostic_data['example_presigned_url_status'] = 'Failed (generate_presigned_url returned None)'
                    diagnostic_data['example_presigned_url_error'] = client.s3_client.exceptions.ClientError.__name__ + "? (Check logs)" # Placeholder
                    diagnostic_data['recommendations'].append("Failed to generate presigned URL. Check IAM permissions (s3:GetObject?) and object key format.")
                    logger.warning(f"TigrisDiagnosticView: Failed to generate presigned URL for {test_object_name}")
            except Exception as url_e:
                 diagnostic_data['example_presigned_url_status'] = 'Failed (Exception)'
                 diagnostic_data['example_presigned_url_error'] = f"{url_e.__class__.__name__}: {url_e}"
                 diagnostic_data['recommendations'].append("Exception during presigned URL generation. Check logs.")
                 logger.error(f"TigrisDiagnosticView: Exception generating presigned URL: {url_e}")

            # Optionally generate public URL example
            diagnostic_data['example_public_url'] = client.get_public_url(test_object_name)

        except (ValueError, ConnectionError, PermissionError) as client_e:
            diagnostic_data['tigris_client_init_status'] = 'Failed (Initialization Error)'
            diagnostic_data['tigris_client_init_error'] = f"{client_e.__class__.__name__}: {client_e}"
            # Error during init implies head_bucket also failed or wasn't reached
            diagnostic_data['head_bucket_status'] = 'Failed (Due to client init error)'
            diagnostic_data['head_bucket_error'] = str(client_e)
            diagnostic_data['recommendations'].append(f"Failed to initialize TigrisClient: {client_e}. Check credentials, endpoint, bucket name, network, and permissions (HeadBucket/GetBucketLocation).")
            logger.error(f"TigrisDiagnosticView: Failed to initialize TigrisClient: {client_e}")
        except Exception as unexpected_e:
             diagnostic_data['tigris_client_init_status'] = 'Failed (Unexpected Exception)'
             diagnostic_data['tigris_client_init_error'] = f"{unexpected_e.__class__.__name__}: {unexpected_e}"
             diagnostic_data['head_bucket_status'] = 'Failed (Due to unexpected client init error)'
             diagnostic_data['recommendations'].append(f"Unexpected error initializing TigrisClient: {unexpected_e}. Check application logs.")
             logger.exception(f"TigrisDiagnosticView: Unexpected error initializing TigrisClient: {unexpected_e}")

        if not diagnostic_data['recommendations']:
             diagnostic_data['recommendations'].append("Basic checks passed. If issues persist, verify CORS, IAM permissions for specific actions (PutObject, GetObject, DeleteObject), and application logic.")

        return Response(diagnostic_data)

    def _get_package_version(self, package_name):
        try:
            import importlib.metadata
            return importlib.metadata.version(package_name)
        except ImportError:
            # Fallback for older Python versions
            try:
                import pkg_resources
                return pkg_resources.get_distribution(package_name).version
            except Exception:
                return "Unknown (Error getting version)"

# Keep old diagnostic view name for URL compatibility if needed, but point to new one
# Or update urls.py to use TigrisDiagnosticView directly
DiagnosticView = TigrisDiagnosticView 
