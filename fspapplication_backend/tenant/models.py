from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class SubscriptionPlan(models.Model):
    """Subscription plans that define pricing tiers and features"""
    PLAN_BASIC = 'basic'
    PLAN_PRO = 'pro'
    PLAN_ENTERPRISE = 'enterprise'
    
    PLAN_CHOICES = [
        (PLAN_BASIC, 'Basic'),
        (PLAN_PRO, 'Pro'),
        (PLAN_ENTERPRISE, 'Enterprise'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default=PLAN_BASIC)
    description = models.TextField(blank=True, null=True)
    
    # Base pricing
    base_price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    base_price_yearly = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Per-user pricing
    price_per_user_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_user_yearly = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Optional included users in base price
    included_users = models.PositiveIntegerField(default=1, 
        help_text="Number of users included in the base price")
    
    is_active = models.BooleanField(default=True)
    features = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (${self.price_per_user_monthly}/user/month)"

    class Meta:
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    
    # Subscription fields
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients'
    )
    subscription_start_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)
    is_subscription_active = models.BooleanField(default=False)
    billing_frequency = models.CharField(
        max_length=10,
        choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')],
        default='monthly'
    )
    paid_user_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of users the tenant has paid for"
    )

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    
    def get_current_user_count(self):
        """Returns the current number of users for this tenant"""
        # This import is here to avoid circular imports
        from django.db import connection
        from account.models import User
        
        # Save the current schema to restore it later
        previous_schema = connection.schema_name
        
        try:
            # Set the connection to this tenant's schema
            connection.set_tenant(self)
            # Count the number of users
            return User.objects.count()
        finally:
            # Restore the previous schema
            if previous_schema:
                connection.set_schema_to_public()
    
    def calculate_monthly_cost(self):
        """Calculate the monthly cost based on plan and user count"""
        if not self.subscription_plan:
            return 0
            
        user_count = self.get_current_user_count()
        plan = self.subscription_plan
        
        # Calculate the cost for users beyond those included in the base price
        additional_users = max(0, user_count - plan.included_users)
        
        if self.billing_frequency == 'monthly':
            return plan.base_price_monthly + (additional_users * plan.price_per_user_monthly)
        else:  # yearly
            monthly_equivalent = (plan.base_price_yearly or 0) / 12
            monthly_per_user = (plan.price_per_user_yearly or 0) / 12
            return monthly_equivalent + (additional_users * monthly_per_user)
    
    def needs_payment_update(self):
        """Check if tenant needs to update their payment due to adding more users"""
        return self.get_current_user_count() > self.paid_user_count
    
    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass