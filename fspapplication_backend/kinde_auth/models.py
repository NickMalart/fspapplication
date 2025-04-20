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
    kinde_user_id = models.CharField(
        max_length=255, 
        unique=True, 
        db_index=True, 
        null=True,  # Allow NULL in the database
        blank=True, # Allow empty value in forms/admin (though less relevant here)
        default=None, # Default to NULL instead of empty string
        help_text="Unique user ID provided by Kinde (null until first login)."
    )
    email = models.EmailField(unique=True, help_text="User's email address, typically from Kinde.")
    first_name = models.CharField(max_length=150, blank=True, default='')
    last_name = models.CharField(max_length=150, blank=True, default='')
    tenants = models.ManyToManyField(
        Client, 
        related_name='kinde_users',
        blank=True, # User might initially have no tenants, or association happens later
        help_text="Tenants this Kinde user has access to."
    )
    
    is_active = models.BooleanField(default=True, help_text="Designates whether this user is considered active.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    # Tenant is no longer required at creation time, association is separate
    REQUIRED_FIELDS = [] # Removed tenant

    def __str__(self):
        # Adjust __str__ to show email only or handle multiple tenants if desired
        return self.email # Simpler representation for now

    class Meta:
        verbose_name = 'Kinde User'
        verbose_name_plural = 'Kinde Users'
        ordering = ['email']
