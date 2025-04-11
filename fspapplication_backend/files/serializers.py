from rest_framework import serializers
from .models import FileUpload
from .tigris_utils import TigrisClient

class FileUploadSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    filename = serializers.SerializerMethodField()
    
    class Meta:
        model = FileUpload
        fields = [
            'id', 'path', 'original_filename', 'file_type', 
            'module', 'content_type', 'file_size', 
            'created_at', 'url', 'filename'
        ]
        read_only_fields = fields
    
    def get_url(self, obj):
        """Generate a presigned URL for the file"""
        tigris_client = TigrisClient()
        return tigris_client.generate_presigned_url(obj.path)
    
    def get_filename(self, obj):
        """Extract just the filename from the path"""
        return obj.path.split('/')[-1]

class FileUploadCreateSerializer(serializers.Serializer):
    file = serializers.FileField()
    file_type = serializers.CharField(max_length=50)
    module = serializers.CharField(max_length=50)
    
    def validate_file_type(self, value):
        """Validate the file type is one of the accepted values"""
        allowed_types = ['images', 'documents', 'media', 'attachments', 'exports']
        if value not in allowed_types:
            raise serializers.ValidationError(f"File type must be one of: {', '.join(allowed_types)}")
        return value 