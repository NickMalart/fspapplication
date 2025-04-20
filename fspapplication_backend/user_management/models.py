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
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.company_name.name}"
    
    class Meta:
        verbose_name = 'Employee Profile'
        verbose_name_plural = 'Employee Profiles'