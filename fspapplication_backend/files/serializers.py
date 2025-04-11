from rest_framework import serializers
from .models import FileUpload
# from .s3_utils import S3Client # Remove old import
from .tigris_utils import TigrisClient # Add new import

class FileUploadSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField() # Keep for generating access URLs
    filename = serializers.SerializerMethodField()
    # Add file_url to store the potentially public URL if available
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FileUpload
        fields = [
            'id', 'path', 'original_filename', 'file_type', 
            'module', 'content_type', 'file_size', 'created_by', # Added created_by back
            'created_at', 'url', 'filename', 'file_url'
        ]
        # Keep read_only_fields minimal, allow updates if needed elsewhere
        read_only_fields = ['id', 'path', 'created_at', 'url', 'filename', 'file_url', 'created_by'] 
    
    def get_url(self, obj):
        """Generate a presigned URL for temporary access."""
        try:
            # Use TigrisClient to generate a presigned URL
            tigris_client = TigrisClient()
            # Generate a GET URL by default, maybe make expiration configurable?
            return tigris_client.generate_presigned_url(obj.path, expiration=3600) 
        except Exception as e:
            # Log the error and return None or an error indicator
            # logger.error(f"Error generating presigned URL for {obj.path}: {e}")
            # In a serializer, usually better to return None or empty string
            return None
    
    def get_filename(self, obj):
        """Extract just the filename from the path."""
        if obj.path:
            return obj.path.split('/')[-1]
        return None
        
    def get_file_url(self, obj):
        """Generate the direct/public URL (use with caution)."""
        try:
            # Use TigrisClient to generate the public URL
            tigris_client = TigrisClient()
            return tigris_client.get_public_url(obj.path)
        except Exception as e:
            # logger.error(f"Error generating public URL for {obj.path}: {e}")
            return None

class FileUploadCreateSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    # Make file_type and module optional with defaults if applicable
    file_type = serializers.CharField(max_length=50, required=False, default='documents')
    module = serializers.CharField(max_length=50, required=False, default='general')
    
    # Keep validation if specific types/modules are strictly enforced
    def validate_file_type(self, value):
        """Validate the file type is one of the accepted values."""
        allowed_types = ['images', 'documents', 'media', 'attachments', 'exports', 'avatars'] # Added avatars
        if value not in allowed_types:
            raise serializers.ValidationError(f"File type must be one of: {', '.join(allowed_types)}")
        return value

    def validate_module(self, value):
        """Basic validation for module name (e.g., prevent invalid characters)."""
        # Example: Allow alphanumeric and hyphens/underscores
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            raise serializers.ValidationError("Module name can only contain letters, numbers, hyphens, and underscores.")
        return value 