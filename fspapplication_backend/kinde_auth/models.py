from django.db import models
import uuid

# Import the Tenant model (Client) from the tenant app
from tenant.models import Client

class KindeUser(models.Model):
    """
    Represents a user authenticated via Kinde in the public schema.
    This model links the Kinde identity to a specific tenant.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kinde_user_id = models.CharField(max_length=255, unique=True, db_index=True, 
                                     help_text="Unique user ID provided by Kinde.")
    email = models.EmailField(unique=True, help_text="User's email address, typically from Kinde.")
    first_name = models.CharField(max_length=150, blank=True, default='')
    last_name = models.CharField(max_length=150, blank=True, default='')
    tenant = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE,  
        related_name='kinde_users',
        help_text="The tenant this Kinde user belongs to."
    )
    
    is_active = models.BooleanField(default=True, help_text="Designates whether this user is considered active.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['kinde_user_id', 'tenant']

    def __str__(self):
        return f"{self.email} ({self.tenant.name})"

    class Meta:
        verbose_name = 'Kinde User'
        verbose_name_plural = 'Kinde Users'
        ordering = ['tenant', 'email']
