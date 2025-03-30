from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import get_object_or_404
import logging
import traceback
import os
import sys
from django.conf import settings

from .models import FileUpload
from .serializers import FileUploadSerializer, FileUploadCreateSerializer
from .s3_utils import S3Client, print_aws_settings

# Configure logger
logger = logging.getLogger(__name__)

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def options(self, request, *args, **kwargs):
        """Handle preflight CORS requests"""
        response = Response()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
    
    def post(self, request):
        logger.info("File upload initiated")
        try:
            logger.debug(f"Request data: {request.data}")
            
            serializer = FileUploadCreateSerializer(data=request.data)
            
            if serializer.is_valid():
                logger.info("Serializer validation passed")
                file_obj = serializer.validated_data['file']
                file_type = serializer.validated_data['file_type']
                module = serializer.validated_data['module']
                tenant = request.tenant
                
                # Get tenant identifier (try common attributes)
                tenant_id = None
                if hasattr(tenant, 'schema_name'):
                    tenant_id = tenant.schema_name
                elif hasattr(tenant, 'name'):
                    # Convert name to a slug-like format
                    tenant_id = tenant.name.lower().replace(' ', '-')
                elif hasattr(tenant, 'slug'):
                    tenant_id = tenant.slug
                elif hasattr(tenant, 'domain_url'):
                    # Extract subdomain
                    tenant_id = tenant.domain_url.split('.')[0]
                else:
                    # Last resort: use the tenant's primary key
                    tenant_id = f"tenant-{tenant.pk}"
                
                logger.debug(f"Tenant ID: {tenant_id}, File type: {file_type}, Module: {module}")
                logger.debug(f"File details - Name: {file_obj.name}, Size: {file_obj.size}, Content type: {getattr(file_obj, 'content_type', None)}")
                
                # Upload to S3
                s3_client = S3Client()
                logger.info("Initialized S3Client")
                
                try:
                    result = s3_client.tenant_upload(
                        file_obj=file_obj,
                        tenant_slug=tenant_id,  # Use tenant_id instead of tenant.slug
                        file_type=file_type,
                        module=module
                    )
                    logger.info(f"S3 upload result: {result}")
                except Exception as e:
                    logger.error(f"S3 upload error: {str(e)}")
                    logger.error(traceback.format_exc())
                    return Response({
                        'success': False,
                        'error': f"S3 upload error: {str(e)}"
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                if result['success']:
                    # Create database record
                    try:
                        file_upload = FileUpload.objects.create(
                            tenant=tenant,
                            path=result['path'],
                            original_filename=file_obj.name,
                            file_type=file_type,
                            module=module,
                            content_type=getattr(file_obj, 'content_type', None),
                            file_size=file_obj.size,
                            created_by=request.user
                        )
                        logger.info(f"Created database record with ID: {file_upload.id}")
                    except Exception as e:
                        logger.error(f"Database record creation error: {str(e)}")
                        logger.error(traceback.format_exc())
                        return Response({
                            'success': False,
                            'error': f"Database error: {str(e)}"
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
                    # Return file details and URL
                    response_data = {
                        'success': True,
                        'path': result['path'],
                        'url': result['url'],
                        'id': file_upload.id
                    }
                    logger.info("File upload successful")
                    return Response(response_data, status=status.HTTP_201_CREATED)
                else:
                    logger.error(f"S3 upload failed: {result.get('error', 'Unknown error')}")
                    return Response({
                        'success': False,
                        'error': result.get('error', 'Upload failed')
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error(f"Serializer validation failed: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in FileUploadView: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({
                'success': False,
                'error': f"Server error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tenant = request.tenant
        file_type = request.query_params.get('file_type')
        module = request.query_params.get('module')
        
        # Filter by tenant
        queryset = FileUpload.objects.filter(tenant=tenant)
        
        # Apply optional filters
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        if module:
            queryset = queryset.filter(module=module)
        
        serializer = FileUploadSerializer(queryset, many=True)
        return Response({'files': serializer.data})


class FileDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        tenant = request.tenant
        path = request.data.get('path')
        
        if not path:
            return Response({
                'success': False,
                'error': 'Path is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure file belongs to this tenant
        try:
            file_upload = FileUpload.objects.get(tenant=tenant, path=path)
        except FileUpload.DoesNotExist:
            return Response({
                'success': False,
                'error': 'File not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Delete from S3
        try:
            s3_client = S3Client()
            result = s3_client.delete_file(path)
            
            if result:
                # Delete the database record
                file_upload.delete()
                return Response({'success': True})
            else:
                return Response({
                    'success': False,
                    'error': 'Failed to delete file from S3'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({
                'success': False,
                'error': f"Error deleting file: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, file_path=None):
        # If path is provided in URL
        if file_path:
            path = file_path
        else:
            # If path is provided in query params
            path = request.query_params.get('path')
        
        if not path:
            return Response({
                'success': False,
                'error': 'Path is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate URL (CloudFront if configured, otherwise S3)
        s3_client = S3Client()
        expiration = int(request.query_params.get('expiration', 3600))  # Default 1 hour
        url = s3_client.generate_presigned_url(path, expiration)
        
        if url:
            # Log which URL type we're using
            if hasattr(s3_client, 'use_cloudfront') and s3_client.use_cloudfront:
                logger.info(f"Serving file via CloudFront: {path}")
            else:
                logger.info(f"Serving file via S3 presigned URL: {path}")
                
            response = Response({
                'success': True,
                'url': url
            })
            
            # Add CORS headers
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            
            return response
        else:
            return Response({
                'success': False,
                'error': 'Could not generate URL'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DiagnosticView(APIView):
    """View for diagnosing AWS S3 issues"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Get environment variables 
            env_vars = {
                'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID', 'Not set in env'),
                'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY', 'Not set in env') 
                                         and '****' or 'Not set in env',
                'AWS_STORAGE_BUCKET_NAME': os.environ.get('AWS_STORAGE_BUCKET_NAME', 'Not set in env'),
                'AWS_S3_REGION_NAME': os.environ.get('AWS_S3_REGION_NAME', 'Not set in env'),
                'CLOUDFRONT_DOMAIN': os.environ.get('CLOUDFRONT_DOMAIN', 'Not set in env'),
            }
            
            # Get settings
            settings_vars = {
                'AWS_ACCESS_KEY_ID': getattr(settings, 'AWS_ACCESS_KEY_ID', 'Not set in settings') 
                                      and settings.AWS_ACCESS_KEY_ID[:4] + '****' or 'Not set in settings',
                'AWS_SECRET_ACCESS_KEY': getattr(settings, 'AWS_SECRET_ACCESS_KEY', 'Not set in settings') 
                                          and '****' or 'Not set in settings',
                'AWS_STORAGE_BUCKET_NAME': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not set in settings'),
                'AWS_S3_REGION_NAME': getattr(settings, 'AWS_S3_REGION_NAME', 'Not set in settings'),
                'CLOUDFRONT_DOMAIN': getattr(settings, 'CLOUDFRONT_DOMAIN', 'Not set in settings'),
            }
            
            # Get python version
            python_version = sys.version
            
            # Get boto3 version
            import boto3
            boto3_version = boto3.__version__
            
            # Test S3 connection
            s3_connection_test = "Not tested"
            s3_error = None
            try:
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                buckets = s3_client.list_buckets()
                bucket_names = [b['Name'] for b in buckets.get('Buckets', [])]
                s3_connection_test = f"Success. Found {len(bucket_names)} buckets."
                s3_bucket_exists = settings.AWS_STORAGE_BUCKET_NAME in bucket_names
                s3_connection_test += f" Bucket '{settings.AWS_STORAGE_BUCKET_NAME}' exists: {s3_bucket_exists}"
            except Exception as e:
                s3_connection_test = "Failed"
                s3_error = str(e)
                
            # Test CloudFront URL generation
            cloudfront_test = "Not tested"
            test_path = "test/test.jpg"
            cloudfront_url = None
            cloudfront_status = "Unknown"
            try:
                if hasattr(settings, 'CLOUDFRONT_DOMAIN') and settings.CLOUDFRONT_DOMAIN:
                    cloudfront_url = f"https://{settings.CLOUDFRONT_DOMAIN}/{test_path}"
                    cloudfront_test = f"CloudFront configured and working. Sample URL: {cloudfront_url}"
                    cloudfront_status = "Configured and working properly"
                    
                    # Check if OAI is configured
                    if hasattr(settings, 'CLOUDFRONT_OAI_ID') and settings.CLOUDFRONT_OAI_ID:
                        cloudfront_test += f"\nOAI ID: {settings.CLOUDFRONT_OAI_ID}"
                else:
                    cloudfront_test = "CloudFront not configured"
                    cloudfront_status = "Not configured"
            except Exception as e:
                cloudfront_test = f"Error testing CloudFront: {str(e)}"
                cloudfront_status = f"Error: {str(e)}"
                
            # Generate a test URL to demonstrate current behavior
            test_url = None
            try:
                s3_client = S3Client()
                test_url = s3_client.generate_presigned_url(test_path, 3600)
                
                if test_url and test_url.startswith(f"https://{settings.CLOUDFRONT_DOMAIN}"):
                    cloudfront_test += "\nNow using CloudFront URLs for all file access."
                else:
                    cloudfront_test += "\nWarning: Not using CloudFront URLs. Please check your configuration."
            except Exception as e:
                cloudfront_test += f"\nError generating test URL: {str(e)}"
            
            # Compile diagnostic data
            diagnostic_data = {
                'environment_variables': env_vars,
                'settings_variables': settings_vars,
                'python_version': python_version,
                'boto3_version': boto3_version,
                's3_connection_test': s3_connection_test,
                's3_error': s3_error,
                'cloudfront_test': cloudfront_test,
                'cloudfront_url_example': cloudfront_url,
                'cloudfront_status': cloudfront_status,
                'current_url_generated': test_url,
                'tenant_id': request.tenant.schema_name if hasattr(request.tenant, 'schema_name') else str(request.tenant),
                'setup_guide': "Please see setup_cloudfront_s3_access.md for instructions on how to properly configure CloudFront with S3"
            }
            
            return Response(diagnostic_data)
        except Exception as e:
            return Response({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
