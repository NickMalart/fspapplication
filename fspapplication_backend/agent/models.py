from django.db import models
import uuid

class Agent(models.Model):
    """
    Model to store agent information including business details, 
    location, contacts, and logistics information.
    """
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic Information
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Agent Logo", help_text="S3 path to agent logo")
    abn = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Primary Contact Info
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Location Information
    street_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Street Number")
    street_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Street Name")
    suburb = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Postal/Zip Code")
    country = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class AgentWarehouse(models.Model):
    """
    Model to store location information for agents.
    An agent can have multiple locations.
    """
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Address Information
    street_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Street Number")
    street_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Street Name")
    suburb = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Postal/Zip Code")
    country = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    
    # Contact Information
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    
    # Location Details
    is_primary = models.BooleanField(default=False)
    operating_hours = models.TextField(blank=True, null=True)
    facility_type = models.CharField(max_length=100, blank=True, null=True, help_text="Type of facility (e.g., Office, Warehouse, Terminal)")
    special_instructions = models.TextField(blank=True, null=True)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.agent.name}"
    
    def save(self, *args, **kwargs):
        # Generate full contact_name from first_name and last_name if provided
        if self.first_name or self.last_name:
            full_name_parts = []
            if self.first_name:
                full_name_parts.append(self.first_name)
            if self.last_name:
                full_name_parts.append(self.last_name)
            self.contact_name = " ".join(full_name_parts) if full_name_parts else None
        super().save(*args, **kwargs)
