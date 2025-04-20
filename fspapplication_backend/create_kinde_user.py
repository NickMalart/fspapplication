# scripts/create_kinde_user.py
# Runnable with: python manage.py runscript create_kinde_user

import sys
from django.core.exceptions import ObjectDoesNotExist

def run(*args):
    print("--- Starting create_kinde_user script ---")
    # --- Imports moved inside run() ---
    # Import models here to ensure Django settings are loaded first
    try:
        from tenant.models import Client  # Assuming your Tenant model is Client
        from kinde_auth.models import KindeUser   # Use the correct path to your KindeUser model
        print("Successfully imported models.")
    except ImportError as e:
        print(f"Error importing models: {e}", file=sys.stderr)
        return # Cannot proceed without models
    # ---------------------------------

    # --- Configuration ---
    target_email = 'nmalart@gmail.com'
    target_tenant_schema_name = 'dev'
    # Generate a placeholder Kinde ID (replace if you have the real one)
    placeholder_kinde_id = f'kinde_placeholder_{target_email.replace("@", "_").replace(".", "_")}'
    print(f"Configuration: email='{target_email}', schema='{target_tenant_schema_name}'")
    # ---------------------

    print(f"Attempting to create KindeUser for {target_email} in tenant '{target_tenant_schema_name}'...")

    try:
        print("Looking for tenant...")
        # Find the target tenant
        tenant = Client.objects.get(schema_name=target_tenant_schema_name)
        print(f"Found tenant: {tenant.name} (ID: {tenant.id}, Schema: {tenant.schema_name})")

        print("Attempting KindeUser.objects.get_or_create...")
        # Check if user already exists
        kinde_user, created = KindeUser.objects.get_or_create(
            email=target_email,
            defaults={
                'kinde_user_id': placeholder_kinde_id,
                'tenant': tenant,
                'first_name': 'Nico',  # Example first name
                'last_name': 'Malart',   # Example last name
                'is_active': True
            }
        )
        print(f"get_or_create completed. User object: {kinde_user}, Created flag: {created}")

        if created:
            print(f"---> Successfully CREATED KindeUser: {kinde_user}")
            print(f"  Kinde User ID (Placeholder): {kinde_user.kinde_user_id}")
            print(f"  Tenant: {kinde_user.tenant.name}")
        else:
            print(f"---> KindeUser with email {target_email} ALREADY EXISTS: {kinde_user}")
            print(f"  Existing Kinde User ID: {kinde_user.kinde_user_id}")
            print(f"  Existing Tenant: {kinde_user.tenant.name}")
            # Optional: Update existing user if needed
            # ... (update logic commented out) ...

    except Client.DoesNotExist:
        print(f"!!! Error: Tenant with schema_name '{target_tenant_schema_name}' not found.", file=sys.stderr)
    except KindeUser.DoesNotExist:
        # This shouldn't happen with get_or_create, but added for completeness
        print(f"!!! Error: KindeUser query failed unexpectedly.", file=sys.stderr)
    except Exception as e:
        import traceback
        print(f"!!! An unexpected error occurred: {e}", file=sys.stderr)
        print("--- Traceback --- ", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("-----------------", file=sys.stderr)
    finally:
        print("--- Script finished ---")

