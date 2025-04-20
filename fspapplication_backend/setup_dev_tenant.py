import os
import django
import uuid

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

from django.utils import timezone
from tenant.models import SubscriptionPlan, Client, Domain
from account.models import User
from django.contrib.auth.hashers import make_password
from kinde_auth.models import KindeUser

def create_subscription_plans():
    """Create default subscription plans"""
    plans = [
        {
            'name': 'Basic Plan',
            'plan_type': SubscriptionPlan.PLAN_BASIC,
            'description': 'Entry-level plan for small teams',
            'base_price_monthly': 49.99,
            'base_price_yearly': 499.99,
            'price_per_user_monthly': 9.99,
            'price_per_user_yearly': 99.99,
            'included_users': 2,
            'features': {
                'max_projects': 5,
                'storage_gb': 10,
                'support_level': 'email'
            }
        },
        {
            'name': 'Pro Plan',
            'plan_type': SubscriptionPlan.PLAN_PRO,
            'description': 'Advanced plan for growing businesses',
            'base_price_monthly': 99.99,
            'base_price_yearly': 999.99,
            'price_per_user_monthly': 19.99,
            'price_per_user_yearly': 199.99,
            'included_users': 5,
            'features': {
                'max_projects': 20,
                'storage_gb': 50,
                'support_level': 'priority'
            }
        },
        {
            'name': 'Enterprise Plan',
            'plan_type': SubscriptionPlan.PLAN_ENTERPRISE,
            'description': 'Comprehensive plan for large organizations',
            'base_price_monthly': 299.99,
            'base_price_yearly': 2999.99,
            'price_per_user_monthly': 49.99,
            'price_per_user_yearly': 499.99,
            'included_users': 10,
            'features': {
                'max_projects': 100,
                'storage_gb': 500,
                'support_level': 'dedicated'
            }
        }
    ]
    
    existing_plans = SubscriptionPlan.objects.filter(name__in=[p['name'] for p in plans])
    existing_plans.delete()  # Clear existing plans
    
    created_plans = []
    for plan_data in plans:
        plan = SubscriptionPlan.objects.create(**plan_data)
        created_plans.append(plan)
    
    return created_plans

def create_dev_tenant():
    """Create the development tenant with a basic plan"""
    # Create or get the basic plan
    basic_plan = SubscriptionPlan.objects.filter(plan_type=SubscriptionPlan.PLAN_BASIC).first()
    if not basic_plan:
        basic_plan = create_subscription_plans()[0]
    
    # Tenant details
    tenant_name = 'Dev Tenant'
    schema_name = 'dev'
    domain_name = 'dev.localhost'
    
    # Create the tenant
    tenant, created = Client.objects.get_or_create(
        schema_name=schema_name,
        defaults={
            'name': tenant_name,
            'subscription_plan': basic_plan,
            'subscription_start_date': timezone.now().date(),
            'subscription_end_date': timezone.now().date().replace(year=timezone.now().date().year + 99),
            'is_subscription_active': True,
            'billing_frequency': 'yearly',
            'paid_user_count': 1
        }
    )
    
    # Create domain
    Domain.objects.get_or_create(
        domain=domain_name,
        tenant=tenant,
        defaults={'is_primary': True}
    )
    
    return tenant

def main():
    """Main setup function"""
    # Create subscription plans
    print("Ensuring subscription plans exist...")
    create_subscription_plans()
    
    # Create development tenant
    print("Creating development tenant...")
    tenant = create_dev_tenant()
    
    print("\n--- Development Tenant Setup Complete ---")
    print(f"Tenant Name:    {tenant.name}")
    print(f"Schema Name:    {tenant.schema_name}")
    # Find the primary domain to print
    primary_domain = tenant.domains.filter(is_primary=True).first()
    print(f"Primary Domain: {primary_domain.domain if primary_domain else 'N/A'}")
    print(f"Plan:           {tenant.subscription_plan.name}")
    print("-----------------------------------------")

if __name__ == '__main__':
    main() 