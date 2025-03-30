from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .s3_utils import S3Client

class GooglePlacesAPIView(APIView):
    """
    API view to proxy requests to Google Places API for address auto-completion
    """
    
    def get(self, request):
        try:
            # Get the query parameter from the request
            input_text = request.query_params.get('input', '')
            
            if not input_text:
                return Response(
                    {"error": "Input parameter is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Build request to Google Places API
            url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
            params = {
                'input': input_text,
                'key': settings.GOOGLE_PLACES_API_KEY,
            }
            
            # Make request to Google API
            response = requests.get(url, params=params)
            data = response.json()
            
            return Response(data)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
class GooglePlaceDetailsAPIView(APIView):
    """
    API view to get full address details from a Place ID
    """
    
    def get(self, request):
        try:
            # Get the place_id parameter from the request
            place_id = request.query_params.get('place_id', '')
            
            if not place_id:
                return Response(
                    {"error": "place_id parameter is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Build request to Google Place Details API
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'key': settings.GOOGLE_PLACES_API_KEY,
                'fields': 'address_component,formatted_address,geometry'
            }
            
            # Make request to Google API
            response = requests.get(url, params=params)
            data = response.json()
            
            return Response(data)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """
    Upload a file to S3 bucket
    """
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    file_obj = request.FILES['file']
    folder = request.POST.get('folder', 'uploads')
    
    # Create a path that includes tenant information for multi-tenancy
    tenant_schema = request.tenant.schema_name
    object_name = f"{folder}/{tenant_schema}/{file_obj.name}"
    
    s3_client = S3Client()
    extra_args = {'ContentType': file_obj.content_type}
    
    success = s3_client.upload_file(file_obj, object_name, extra_args)
    
    if success:
        return JsonResponse({
            'status': 'success',
            'file_path': object_name,
            'file_name': file_obj.name
        })
    else:
        return JsonResponse({'error': 'Failed to upload file'}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_download_url(request, file_path):
    """
    Generate a presigned URL for downloading a file
    """
    s3_client = S3Client()
    expiration = int(request.GET.get('expiration', 3600))  # Default 1 hour
    
    url = s3_client.generate_presigned_url(file_path, expiration)
    
    if url:
        return JsonResponse({'url': url})
    else:
        return JsonResponse({'error': 'Could not generate URL'}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    """
    List files in a specified folder
    """
    prefix = request.GET.get('prefix', '')
    tenant_schema = request.tenant.schema_name
    
    # Include tenant schema in the prefix for multi-tenancy
    if prefix and not prefix.endswith('/'):
        prefix += '/'
    
    tenant_prefix = f"{prefix}{tenant_schema}/"
    
    s3_client = S3Client()
    files = s3_client.list_files(tenant_prefix)
    
    # Format the response
    file_list = [{
        'key': file.get('Key'),
        'size': file.get('Size'),
        'last_modified': file.get('LastModified').isoformat() if file.get('LastModified') else None,
    } for file in files]
    
    return JsonResponse({'files': file_list})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request, file_path):
    """
    Delete a file from S3
    """
    s3_client = S3Client()
    success = s3_client.delete_file(file_path)
    
    if success:
        return JsonResponse({'status': 'success', 'message': 'File deleted successfully'})
    else:
        return JsonResponse({'error': 'Failed to delete file'}, status=500)