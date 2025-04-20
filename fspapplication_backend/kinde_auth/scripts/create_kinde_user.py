import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from tenant.models import Client as Tenant  # Assuming your tenant model is tenant.models.Client
from kinde_auth.models import KindeUser  # Assuming your KindeUser model is auth.models.KindeUser

User = get_user_model()

def run():
    """
    Creates KindeUser entries for existing users in the public schema
    and associates them with their respective tenants.

    NOTE: This script assumes a way to link existing Users to Tenants.
          You might need to adjust the logic for finding the correct tenant
          for each user based on your application's structure.
    """
    print("Starting KindeUser creation script...")

    # Fetch all existing tenants (public schema usually has the main tenant list)
    try:
        tenants = Tenant.objects.all()
        if not tenants.exists():
            print("No tenants found. Exiting.")
            return
        print(f"Found {tenants.count()} tenants.")
    except Exception as e:
        print(f"Error fetching tenants: {e}")
        return

    # Fetch all existing users (adjust query as needed, e.g., filter by role, status)
    # This assumes User model is in the shared apps and accessible here.
    try:
        users_to_process = User.objects.all() # Example: Fetch all users
        # Or filter: users_to_process = User.objects.filter(is_active=True)
        if not users_to_process.exists():
            print("No users found to process. Exiting.")
            return
        print(f"Found {users_to_process.count()} users to potentially process.")
    except Exception as e:
        print(f"Error fetching users: {e}")
        return

    created_count = 0
    skipped_count = 0
    error_count = 0

    # --- Tenant Association Logic ---
    # This is a placeholder. You MUST adapt this section based on how
    # your users are related to tenants.
    # Example 1: If users have a direct foreign key to Tenant
    # Example 2: If users belong to a company/organization linked to a Tenant
    # Example 3: Using a default tenant for all users initially

    # Using a simple (likely incorrect) default: associate with the first tenant found
    # Replace this with your actual logic!
    default_tenant = tenants.first()
    print(f"WARNING: Using default tenant '{default_tenant.name}' for association. Adapt this logic!")
    # ---------------------------------

    with transaction.atomic(): # Use a transaction for atomicity
        for user in users_to_process:
            try:
                # --- Determine the correct tenant for the user ---
                # Replace this placeholder logic
                tenant_for_user = default_tenant # <<< ADAPT THIS LINE
                # ----------------------------------------------

                if not tenant_for_user:
                    print(f"Skipping user {user.email}: Could not determine tenant.")
                    skipped_count += 1
                    continue

                # Check if a KindeUser already exists for this user and tenant
                kinde_user_exists = KindeUser.objects.filter(user=user, tenant=tenant_for_user).exists()

                if not kinde_user_exists:
                    # Create a KindeUser record
                    # The 'kinde_id' will likely be null/empty until the first Kinde login
                    kinde_user = KindeUser.objects.create(
                        user=user,
                        tenant=tenant_for_user,
                        kinde_id=None # Kinde ID will be populated upon first login
                    )
                    print(f"Created KindeUser for {user.email} associated with tenant {tenant_for_user.name}")
                    created_count += 1
                else:
                    print(f"Skipping user {user.email}: KindeUser already exists for tenant {tenant_for_user.name}.")
                    skipped_count += 1

            except Exception as e:
                print(f"Error processing user {user.email}: {e}")
                error_count += 1
                # Decide if you want to continue or break on error

    print("--- Script Summary ---")
    print(f"Successfully created: {created_count}")
    print(f"Skipped (already exists or no tenant): {skipped_count}")
    print(f"Errors: {error_count}")
    print("KindeUser creation script finished.")

# Allows running the script directly if needed, though manage.py runscript is preferred
if __name__ == "__main__":
    run() 