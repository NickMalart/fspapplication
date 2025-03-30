from django.db import models
from django_tenants.models import TenantMixin
from django.conf import settings

class FileUpload(models.Model):
    """
    Tracks files uploaded to S3 for each tenant
    """
    tenant = models.ForeignKey(
        settings.TENANT_MODEL,
        on_delete=models.CASCADE,
        related_name='file_uploads'
    )
    path = models.CharField(max_length=255)
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)  # images, documents, etc.
    module = models.CharField(max_length=50)     # profiles, products, etc.
    content_type = models.CharField(max_length=100, blank=True, null=True)
    file_size = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_files'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.original_filename} ({self.file_type}/{self.module})"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'file_type', 'module']),
            models.Index(fields=['path']),
        ]
