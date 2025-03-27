from django.db import models
from django.core.exceptions import ValidationError


class Company(models.Model):
    """
    Represents the main company that owns the application.
    This is a singleton model - only one company should exist per application instance.
    """
    name = models.CharField(max_length=255, verbose_name="Company Name")
    logo = models.ImageField(upload_to='company', blank=True, null=True, verbose_name="Company Logo")
    address_line1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address Line 1")
    address_line2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address Line 2")
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Postal/Zip Code")
    country = models.CharField(max_length=100, blank=True, null=True)
    
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="Contact Email")
    website = models.URLField(blank=True, null=True)
    
    tax_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tax Number")
    abn_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Business Registration Number")
    
    primary_color = models.CharField(max_length=7, default="#3B82F6", verbose_name="Primary Brand Color")
    secondary_color = models.CharField(max_length=7, default="#1E40AF", verbose_name="Secondary Brand Color")
    
    established_date = models.DateField(blank=True, null=True, verbose_name="Established Date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company"  # Singular to emphasize there's only one
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Override save to ensure only one company instance exists"""
        if not self.pk and Company.objects.exists():
            # If you're trying to create a new object and one already exists
            raise ValidationError("Only one company can exist. Please edit the existing company.")
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_solo(cls):
        """Get the single company instance or create it if it doesn't exist"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
