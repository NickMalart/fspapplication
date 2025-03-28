import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group
from django.db import models
from django.utils import timezone
from django.apps import apps

from organisation.models import Company


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
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


# Custom functional group model
class FunctionalGroup(models.Model):
    """
    Predefined functional groups with specific access rights.
    Each group controls access to particular pages or features in the system.
    """
    # Predefined group types
    GROUP_ADMINISTRATION = 'administration'
    GROUP_HELPDESK = 'helpdesk'
    GROUP_TECHNICIAN = 'technician'
    GROUP_AGENT = 'agent'
    GROUP_CLIENT = 'client'
    GROUP_WAREHOUSE = 'warehouse'
    GROUP_ADMIN = 'admin'
    GROUP_FINANCE = 'finance'
    GROUP_MANAGEMENT = 'management'
    
    GROUP_CHOICES = [
        (GROUP_ADMINISTRATION, 'Administration'),
        (GROUP_HELPDESK, 'Helpdesk'),
        (GROUP_TECHNICIAN, 'Technician'),
        (GROUP_AGENT, 'Agent'),
        (GROUP_CLIENT, 'Client'),
        (GROUP_WAREHOUSE, 'Warehouse'),
        (GROUP_ADMIN, 'Administrator'),
        (GROUP_FINANCE, 'Finance'),
        (GROUP_MANAGEMENT, 'Management'),
    ]
    
    code = models.CharField(
        max_length=50, 
        choices=GROUP_CHOICES,
        unique=True,
        help_text="System code for this group, used for permissions"
    )
    name = models.CharField(
        max_length=100, 
        help_text="Display name for this group"
    )
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default="#3B82F6")  
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Functional Group'
        verbose_name_plural = 'Functional Groups'
        ordering = ['name']


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_AGENT = 'agent'
    USER_TYPE_CLIENT = 'client'
    USER_TYPE_EMPLOYEE = 'employee'
    
    USER_TYPE_CHOICES = [
        (USER_TYPE_AGENT, 'Agent'),
        (USER_TYPE_CLIENT, 'Client'),
        (USER_TYPE_EMPLOYEE, 'Employee')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, default='')
    last_name = models.CharField(max_length=150, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    # Functional groups (custom implementation)
    functional_groups = models.ManyToManyField(
        FunctionalGroup, 
        related_name='users',
        blank=True,
        verbose_name='Functional Groups'
    )

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_agent(self):
        return self.user_type == self.USER_TYPE_AGENT
    
    @property
    def is_client(self):
        return self.user_type == self.USER_TYPE_CLIENT
    
    @property
    def is_employee(self):
        return self.user_type == self.USER_TYPE_EMPLOYEE
    
    def get_specific_profile(self):
        """Returns the specific profile based on user_type"""
        if self.is_agent:
            return self.agent_profile
        elif self.is_client:
            return self.client_profile
        elif self.is_employee:
            return self.employee_profile
        return None
    
    def belongs_to_group(self, group_code):
        """Check if user belongs to a functional group by code"""
        return self.functional_groups.filter(code=group_code).exists()

    def belongs_to_permission_group(self, group_name):
        """Check if user belongs to a Django permission group by name"""
        return self.groups.filter(name=group_name).exists()
    
    # Shortcut properties for common group membership checks
    @property
    def is_helpdesk(self):
        return self.belongs_to_group(FunctionalGroup.GROUP_HELPDESK)
    
    @property
    def is_technician(self):
        return self.belongs_to_group(FunctionalGroup.GROUP_TECHNICIAN)
    
    @property
    def is_warehouse(self):
        return self.belongs_to_group(FunctionalGroup.GROUP_WAREHOUSE)
    
    @property
    def is_admin(self):
        return self.belongs_to_group(FunctionalGroup.GROUP_ADMIN)

    @property
    def can_access_helpdesk(self):
        """Check if user can access the helpdesk page"""
        return (self.is_helpdesk or 
                self.is_admin or 
                self.is_superuser)
    
    @property
    def can_access_warehouse(self):
        """Check if user can access the warehouse management page"""
        return (self.is_warehouse or 
                self.is_admin or 
                self.is_superuser)
    
    @property
    def can_access_technician_tools(self):
        """Check if user can access technician tools"""
        return (self.is_technician or 
                self.is_admin or 
                self.is_superuser)


# Convenience model to track when users were added to groups and by whom
class UserGroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    group = models.ForeignKey(FunctionalGroup, on_delete=models.CASCADE, related_name='user_memberships')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_memberships')
    added_on = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'group')
        verbose_name = 'User Group Membership'
        verbose_name_plural = 'User Group Memberships'
    
    def __str__(self):
        return f"{self.user} - {self.group}"


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_first_name = models.CharField(max_length=150, blank=True, null=True)
    emergency_contact_last_name = models.CharField(max_length=150, blank=True, null=True)

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
        User, 
        on_delete=models.CASCADE, 
        related_name='agent_profile',
        limit_choices_to={'user_type': User.USER_TYPE_AGENT}
    )
    company_name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Agent Profile"
    
    class Meta:
        verbose_name = 'Agent Profile'
        verbose_name_plural = 'Agent Profiles'


class ClientProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='client_profile',
        limit_choices_to={'user_type': User.USER_TYPE_CLIENT}
    )
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True, null=True)
    client_since = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Client Profile"
    
    class Meta:
        verbose_name = 'Client Profile'
        verbose_name_plural = 'Client Profiles'


class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='employee_profile',
        limit_choices_to={'user_type': User.USER_TYPE_EMPLOYEE}
    )
    company = models.ForeignKey('organisation.Company', on_delete=models.CASCADE, related_name='employees')
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
        return f"{self.user.first_name} {self.user.last_name} - {self.company.name}"
    
    class Meta:
        verbose_name = 'Employee Profile'
        verbose_name_plural = 'Employee Profiles'


def get_company_model():
    return apps.get_model('organisation', 'Company')