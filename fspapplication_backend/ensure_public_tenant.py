import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

from tenant.models import Client, Domain


def ensure_public_tenant_and_domain():
    """Ensures the public tenant and its localhost domain exist."""
    public_schema_name = 'public'
    public_domain_name = 'localhost'
    
    print(f"--- Ensuring Public Tenant and Domain --- ")
    print(f"Target Schema: '{public_schema_name}'")
    print(f"Target Domain: '{public_domain_name}'")
    
    # 1. Ensure the public tenant exists
    try:
        public_tenant, created = Client.objects.get_or_create(
            schema_name=public_schema_name,
            defaults={
                'name': 'Public Tenant',
                # Add any other required fields for Client model with defaults
                # 'subscription_plan': None, 
                'is_subscription_active': True, 
                'paid_user_count': 0,
            }
        )
        if created:
            print(f"[OK] Created public tenant: {public_tenant.name} (Schema: {public_tenant.schema_name})")
        else:
            print(f"[OK] Found existing public tenant: {public_tenant.name}")
    except Exception as e:
        print(f"[ERROR] Failed to create/find public tenant: {e}")
        sys.exit(1)

    # 2. Ensure the domain for localhost exists and links to the public tenant
    try:
        domain, created = Domain.objects.get_or_create(
            domain=public_domain_name,
            tenant=public_tenant, # Ensure it points to the correct tenant
            defaults={'is_primary': True}
        )
        if created:
            print(f"[OK] Created domain '{domain.domain}' for public tenant.")
        else:
            # Verify the existing domain points to the correct tenant
            if domain.tenant != public_tenant:
                print(f"[WARNING] Domain '{domain.domain}' existed but pointed to wrong tenant ({domain.tenant.schema_name}). Updating link to '{public_schema_name}'.")
                domain.tenant = public_tenant
                domain.save()
            else:
                print(f"[OK] Found existing domain '{domain.domain}' linked to public tenant.")
                
    except Exception as e:
         print(f"[ERROR] Failed to create/find domain '{public_domain_name}': {e}")
         sys.exit(1)
         
    print("--- Public Tenant and Domain Setup Verified --- ")

if __name__ == '__main__':
    ensure_public_tenant_and_domain() 