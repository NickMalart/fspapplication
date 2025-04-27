import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from company.models import Company


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, default='')
    last_name = models.CharField(max_length=150, blank=True, default='')

    is_superuser = models.BooleanField(default=False, help_text="Designates whether this user has all permissions without explicitly assigning them.")
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(default=True)
    is_tenant_owner = models.BooleanField(default=False, help_text="Designates whether this user is the owner of the tenant")

    USER_TYPE_CHOICES = (
        ('agent', 'Agent'),
        ('client', 'Client'),
        ('employee', 'Employee'),
    )
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        blank=True, # Allow blank initially, might be set later
        null=True,  # Allow null initially
        help_text="Type of the user profile (Agent, Client, or Employee)"
    )

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_first_name = models.CharField(max_length=150, blank=True, null=True)
    emergency_contact_last_name = models.CharField(max_length=150, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True, help_text="S3 path to user avatar")


    street_number = models.CharField(max_length=20, blank=True, null=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    suburb = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    google_place_id = models.CharField(max_length=255, blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class AgentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agent_profile',
        limit_choices_to={'user_type': 'agent'}
    )
    company_name = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='agents')
    abn = models.CharField(max_length=50, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Agent Profile"
    
    class Meta:
        verbose_name = 'Agent Profile'
        verbose_name_plural = 'Agent Profiles'


class ClientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
        limit_choices_to={'user_type': 'client'}
    )
    company_name = models.ForeignKey('client.Client', on_delete=models.CASCADE, related_name='client_profiles')
    industry = models.CharField(max_length=100, blank=True, null=True)
    client_since = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Client Profile"
    
    class Meta:
        verbose_name = 'Client Profile'
        verbose_name_plural = 'Client Profiles'


class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        limit_choices_to={'user_type': 'employee'}
    )
    company_name = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='employees')
    department = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    reports_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )
    
    def save(self, *args, **kwargs):
        """Automatically assign the singleton company before saving."""
        # Ensure the company_name is set to the singleton Company instance
        # Only if it's not already set or if it's a new instance
        if not self.company_name_id:
            try:
                # Use the get_solo method from the Company model
                tenant_company = Company.get_solo()
                self.company_name = tenant_company
            except Company.DoesNotExist:
                # Handle the case where the company doesn't exist yet?
                # This shouldn't happen if the Company is truly a singleton
                # Maybe raise an error or log a warning
                print("WARNING: Singleton Company does not exist while saving EmployeeProfile.")
                # Depending on requirements, you might want to prevent saving:
                # raise ValidationError("Cannot save EmployeeProfile: Tenant Company not found.")
                pass # Or allow saving without company if that's acceptable
        
        super().save(*args, **kwargs) # Call the original save method
    
    def __str__(self):
        # Use try-except for company_name in case it's not set (though save should handle it)
        company_display_name = "Unknown Company"
        try:
            if self.company_name:
                company_display_name = self.company_name.name
        except Company.DoesNotExist: # Handle potential RelatedObjectDoesNotExist
            pass 
        return f"{self.user.first_name} {self.user.last_name} - {company_display_name}"
    
    class Meta:
        verbose_name = 'Employee Profile'
        verbose_name_plural = 'Employee Profiles'