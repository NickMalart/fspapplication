import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

from django.db import connection, IntegrityError
from tenant.models import Client
from account.models import User
from kinde_auth.models import KindeUser

# --- Configuration ---
TARGET_TENANT_SCHEMA = 'dev'
SUPERUSER_EMAIL = 'superuser@dev.com'
SUPERUSER_FIRST_NAME = 'Super'
SUPERUSER_LAST_NAME = 'User'
# --- End Configuration ---

def create_superuser_for_tenant(schema_name, email, first_name, last_name):
    """Creates a superuser within a specific tenant and the public KindeUser link."""
    
    print(f"Attempting to create superuser '{email}' for tenant schema '{schema_name}'...")
    
    # 1. Find the tenant in the public schema
    try:
        tenant = Client.objects.using('default').get(schema_name=schema_name)
        print(f"Found tenant: {tenant.name} (Schema: {tenant.schema_name})")
    except Client.DoesNotExist:
        print(f"Error: Tenant with schema name '{schema_name}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error finding tenant: {e}")
        sys.exit(1)

    # 2. Switch to the tenant's schema
    try:
        connection.set_tenant(tenant)
        print(f"Switched to tenant schema: {connection.schema_name}")
        
        # 3. Create the superuser within the tenant schema
        #    Passing password=None sets an unusable password automatically.
        superuser = User.objects.create_superuser(
            email=email, 
            password=None, 
            first_name=first_name, 
            last_name=last_name
        )
        print(f"Successfully created tenant superuser: {superuser.email} (ID: {superuser.id})")
        print(f"Password set to unusable for {superuser.email}.")

    except IntegrityError:
         # Handle case where user already exists in this tenant's schema
        print(f"Warning: User with email '{email}' already exists in schema '{schema_name}'. Attempting to ensure superuser status.")
        try:
            superuser = User.objects.get(email=email)
            updated = False
            if not superuser.is_superuser:
                superuser.is_superuser = True
                updated = True
            if not superuser.is_staff:
                superuser.is_staff = True
                updated = True
            if updated:
                superuser.save()
                print(f"Updated existing user '{email}' to be superuser/staff.")
            else:
                print(f"Existing user '{email}' is already a superuser/staff.")
        except User.DoesNotExist:
             # Should not happen if IntegrityError was raised, but check anyway
            print(f"Error: IntegrityError reported but user '{email}' not found.")
            connection.set_schema_to_public()
            sys.exit(1)
        except Exception as e:
            print(f"Error updating existing user: {e}")
            connection.set_schema_to_public()
            sys.exit(1)
            
    except Exception as e:
        print(f"Error creating superuser in tenant schema: {e}")
        connection.set_schema_to_public() # Ensure we switch back on error
        sys.exit(1)

    # 4. Switch back to the public schema
    connection.set_schema_to_public()
    print(f"Switched back to public schema: {connection.schema_name}")

    # 5. Create the KindeUser link in the public schema
    try:
        kinde_user, created = KindeUser.objects.using('default').get_or_create(
            email=email,
            defaults={
                'tenant': tenant,
                'first_name': first_name,
                'last_name': last_name,
                'kinde_user_id': '', # Will be filled in on first Kinde login
                'is_active': True, # Assuming superuser should be active
            }
        )
        if created:
            print(f"Created public KindeUser link for {email} to tenant '{tenant.name}'.")
        else:
            # Ensure the existing KindeUser points to the correct tenant
            if kinde_user.tenant != tenant:
                print(f"Warning: Existing KindeUser '{email}' linked to different tenant ({kinde_user.tenant.name}). Updating link to '{tenant.name}'.")
                kinde_user.tenant = tenant
                kinde_user.save()
            else:
                 print(f"Found existing public KindeUser link for {email} to tenant '{tenant.name}'.")

    except Exception as e:
        print(f"Error creating/updating KindeUser in public schema: {e}")
        # Don't exit here, tenant user was created, but log the error
        
    print("\nSuperuser creation process complete.")

if __name__ == '__main__':
    create_superuser_for_tenant(
        TARGET_TENANT_SCHEMA, 
        SUPERUSER_EMAIL, 
        SUPERUSER_FIRST_NAME, 
        SUPERUSER_LAST_NAME
    ) 