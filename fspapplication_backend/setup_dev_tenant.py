import os
import django
import uuid

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

from django.utils import timezone
from tenant.models import SubscriptionPlan, Client, Domain
from account.models import User, FunctionalGroup
from django.contrib.auth.hashers import make_password

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
    """Create a development tenant with a basic plan"""
    # Create or get the basic plan
    basic_plan = SubscriptionPlan.objects.filter(plan_type=SubscriptionPlan.PLAN_BASIC).first()
    if not basic_plan:
        basic_plan = create_subscription_plans()[0]
    
    # Create the tenant
    tenant, created = Client.objects.get_or_create(
        name='Dev Tenant',
        defaults={
            'schema_name': 'dev',
            'subscription_plan': basic_plan,
            'subscription_start_date': timezone.now().date(),
            'subscription_end_date': timezone.now().date().replace(year=timezone.now().date().year + 1),
            'is_subscription_active': True,
            'billing_frequency': 'monthly',
            'paid_user_count': 15  # Included in basic plan
        }
    )
    
    # Create domain
    Domain.objects.get_or_create(
        domain='dev.localhost',
        tenant=tenant,
        defaults={'is_primary': True}
    )
    
    return tenant

def create_dev_users(tenant):
    """Create development users for the tenant"""
    # Ensure we're in the tenant's schema
    from django.db import connection
    connection.set_tenant(tenant)
    
    # Create functional groups
    groups_data = [
        {
            'code': FunctionalGroup.GROUP_ADMIN,
            'name': 'System Administrators',
            'description': 'Full system access'
        },
        {
            'code': FunctionalGroup.GROUP_CLIENT,
            'name': 'Client Users',
            'description': 'Standard client access'
        }
    ]
    
    # Clear existing groups to avoid duplicates
    FunctionalGroup.objects.all().delete()
    
    # Create groups
    groups = []
    for group_data in groups_data:
        group = FunctionalGroup.objects.create(**group_data)
        groups.append(group)
    
    # Create admin user
    admin_user = User.objects.create(
        email='admin@devtenant.com',
        first_name='Dev',
        last_name='Admin',
        user_type=User.USER_TYPE_CLIENT,
        is_active=True,
        is_staff=True,
        is_superuser=True
    )
    admin_user.set_password('devadmin123')
    admin_user.save()
    
    # Add admin to admin group
    admin_user.functional_groups.add(groups[0])
    
    # Create additional users
    users_data = [
        {
            'email': f'user{i}@devtenant.com',
            'first_name': f'First{i}',
            'last_name': f'Last{i}',
            'user_type': User.USER_TYPE_CLIENT,
        } for i in range(1, 11)
    ]
    
    for user_data in users_data:
        user = User.objects.create(
            **user_data,
            is_active=True
        )
        user.set_password('devuser123')
        user.save()
        
        # Add to client group
        user.functional_groups.add(groups[1])
    
    return admin_user

def main():
    """Main setup function"""
    # Create subscription plans
    create_subscription_plans()
    
    # Create development tenant
    tenant = create_dev_tenant()
    
    # Create development users
    admin_user = create_dev_users(tenant)
    
    print("Development environment setup complete!")
    print(f"Tenant: {tenant.name}")
    print(f"Admin User: {admin_user.email}")
    print(f"Subscription Plan: {tenant.subscription_plan.name}")
    print(f"Paid User Count: {tenant.paid_user_count}")

if __name__ == '__main__':
    main() 