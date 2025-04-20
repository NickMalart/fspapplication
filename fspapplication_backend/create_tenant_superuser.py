import os
import django
import sys
from django.conf import settings
import requests # Import requests
import time # Import time module for sleep
import subprocess # Added import

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

from django.db import connection, IntegrityError
from tenant.models import Client
from account.models import User
from kinde_auth.models import KindeUser

# --- Configuration ---
TARGET_TENANT_SCHEMA = 'dev'
SUPERUSER_EMAIL = 'nmalartlp@gmail.com'
SUPERUSER_FIRST_NAME = 'Nick'
SUPERUSER_LAST_NAME = 'Nike'
# --- End Configuration ---

# --- Kinde API Helper ---

def get_kinde_m2m_token():
    """Fetches an M2M access token from Kinde to use the Management API."""
    client_id = settings.KINDE_MGMNT_CLIENT_ID
    client_secret = settings.KINDE_MGMNT_CLIENT_SECRET
    audience = settings.KINDE_MGMNT_AUDIENCE
    token_url = f"{settings.KINDE_ISSUER}/oauth2/token"

    if not client_id or not client_secret:
        print("[ERROR] Kinde M2M Client ID or Secret not configured in environment variables.")
        return None

    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': audience
    }

    try:
        print(f"Requesting Kinde M2M token from {token_url} for audience {audience}...")
        response = requests.post(token_url, data=payload, timeout=15)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        token_data = response.json()
        access_token = token_data.get('access_token')
        if not access_token:
            print(f"[ERROR] 'access_token' not found in Kinde M2M response: {token_data}")
            return None
        print("[OK] Successfully obtained Kinde M2M access token.")
        return access_token
    except requests.exceptions.RequestException as e:
        error_details = "No details available."
        if e.response is not None:
            try:
                error_details = e.response.json()
            except ValueError:
                error_details = e.response.text
        print(f"[ERROR] Failed to get Kinde M2M token: {e}. Details: {error_details}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error getting Kinde M2M token: {e}")
        return None

# --- Main Function ---

def create_superuser_for_tenant(schema_name, email, first_name, last_name):
    """Creates a superuser within a specific tenant and the public KindeUser link."""
    
    print(f"Attempting to create superuser '{email}' for tenant schema '{schema_name}'...")
    
    # *** Get Kinde M2M Token FIRST ***
    print("\nAttempting to get Kinde Management API token...")
    kinde_m2m_token = get_kinde_m2m_token()
    if not kinde_m2m_token:
        print("[ABORT] Cannot proceed without Kinde M2M token.")
        sys.exit(1)

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

    # 5. Create/Update the KindeUser link in the public schema
    try:
        # Get or create the base KindeUser by email
        kinde_user_link, created = KindeUser.objects.using('default').get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'kinde_user_id': None, # Set to None initially
                'is_active': True, 
            }
        )
        
        # Ensure the tenant is associated with this KindeUser
        if not kinde_user_link.tenants.filter(pk=tenant.pk).exists():
            kinde_user_link.tenants.add(tenant)
            print(f"Associated KindeUser '{email}' with tenant '{tenant.name}'.")
            created = True # Treat association as part of creation for messaging
        else:
            print(f"KindeUser '{email}' already associated with tenant '{tenant.name}'.")
            # Ensure the 'created' flag is false if only association existed
            if not created: # if the base KindeUser object wasn't just created
                created = False
            
        if created:
            print(f"Created/Updated public KindeUser link for {email} to tenant '{tenant.name}'.")
        else:
            print(f"Found existing public KindeUser link for {email} associated with tenant '{tenant.name}'.")

    except Exception as e:
        print(f"Error creating/updating KindeUser in public schema or associating tenant: {e}")
        # sys.exit(1) # Decide if this should be fatal
        
    # 6. Create User in Kinde via Management API
    print(f"\nAttempting to create/verify user '{email}' in Kinde via API...")
    kinde_api_user_url = f"{settings.KINDE_ISSUER}/api/v1/user"
    headers = {
        'Authorization': f'Bearer {kinde_m2m_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        'profile': {
            'given_name': first_name,
            'family_name': last_name
        },
        'identities': [
            {
                'type': 'email',
                'details': {
                    'email': email
                }
            }
        ]
        # Add other fields like 'password' if needed/allowed by Kinde API for creation,
        # but typically for OIDC flows, the user sets their own password.
    }

    try:
        response = requests.post(kinde_api_user_url, headers=headers, json=payload, timeout=15)
        
        # Check for success or if user already exists
        kinde_user_created_or_exists = False
        if response.status_code == 201: # 201 Created
            print(f"[OK] Kinde API reported user '{email}' was created.")
            kinde_user_created_or_exists = True
        elif response.status_code == 200: # 200 OK (Treat as existing user for this endpoint)
             print(f"[INFO] Kinde API returned 200 OK for user '{email}'. Assuming user already exists.")
             kinde_user_created_or_exists = True
        elif response.status_code == 400 or response.status_code == 409: # Bad Request or Conflict (likely exists)
            error_data = response.json()
            print(f"[INFO] Kinde API reported user '{email}' might already exist (Code: {response.status_code}). Details: {error_data}")
            # Assume user exists if we get a conflict/bad request related to existence
            if "already exists" in str(error_data).lower() or response.status_code == 409:
                 kinde_user_created_or_exists = True
        else:
            # For other errors, raise exception or log but don't assume existence
            print(f"[WARNING] Unexpected status code {response.status_code} when trying to create user in Kinde.")
            try: 
                response.raise_for_status()
            except Exception as http_err:
                 print(f"[ERROR] Details: {http_err}")
            
    except requests.exceptions.RequestException as e:
        error_details = "No details available."
        if e.response is not None:
            try:
                error_details = e.response.json()
            except ValueError:
                error_details = e.response.text
        print(f"[ERROR] Failed POST request to create user in Kinde via API: {e}. Details: {error_details}")
        # Decide if this should be a fatal error for the script
        # sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error during POST request to create user in Kinde via API: {e}")
        # Decide if this should be a fatal error for the script
        # sys.exit(1)

    # --- Add delay before attempting to GET the user --- 
    print("\nWaiting 5 seconds before querying Kinde API for user ID...")
    time.sleep(5)
    # --- End Delay ---

    # 7. Fetch User from Kinde API to Confirm ID (if creation/existence was indicated)
    retrieved_kinde_id = None
    if kinde_user_created_or_exists:
        print(f"\nAttempting to GET user '{email}' from Kinde API to retrieve ID...")
        # Note: Ensure URL encoding if email can contain special characters
        kinde_get_user_url = f"{settings.KINDE_ISSUER}/api/v1/users?email={requests.utils.quote(email)}"
        headers = {
            'Authorization': f'Bearer {kinde_m2m_token}',
            'Accept': 'application/json'
        }
        try:
            get_response = requests.get(kinde_get_user_url, headers=headers, timeout=15)
            get_response.raise_for_status() # Raise for 4xx/5xx errors
            
            get_data = get_response.json()
            users_list = get_data.get('users', [])
            
            if len(users_list) == 1:
                retrieved_kinde_id = users_list[0].get('id')
                if retrieved_kinde_id:
                    print(f"[OK] Successfully retrieved Kinde ID for '{email}': {retrieved_kinde_id}")
                else:
                    print(f"[WARNING] Found user '{email}' in Kinde API, but no 'id' field in response.")
            elif len(users_list) == 0:
                print(f"[ERROR] Could not find user '{email}' via Kinde API GET request, even though POST indicated success/existence.")
            else:
                print(f"[ERROR] Found multiple users ({len(users_list)}) for email '{email}' via Kinde API GET request. Cannot determine correct ID.")
                
        except requests.exceptions.RequestException as e:
            error_details = "No details available."
            if e.response is not None:
                try:
                    error_details = e.response.json()
                except ValueError:
                    error_details = e.response.text
            print(f"[ERROR] Failed GET request to find user in Kinde via API: {e}. Details: {error_details}")
        except Exception as e:
            print(f"[ERROR] Unexpected error during GET request to find user in Kinde via API: {e}")
    else:
         print("\nSkipping Kinde API GET request because user creation/existence was not confirmed by POST.")
         
    # 8. Update Local KindeUser Record with Retrieved ID
    if retrieved_kinde_id:
        print(f"\nAttempting to update local KindeUser record for '{email}' with Kinde ID '{retrieved_kinde_id}'...")
        try:
            # Ensure kinde_user_link object from Step 5 is accessible
            # It should be, as it was fetched/created before this point
            if kinde_user_link:
                 print(f"Found local KindeUser object: Email='{kinde_user_link.email}', Current Kinde ID='{kinde_user_link.kinde_user_id}'")
                 if kinde_user_link.kinde_user_id != retrieved_kinde_id:
                     print(f"Current local ID ('{kinde_user_link.kinde_user_id}') differs from retrieved ID ('{retrieved_kinde_id}'). Updating...")
                     kinde_user_link.kinde_user_id = retrieved_kinde_id
                     kinde_user_link.save(using='default')
                     print(f"[OK] Successfully saved updated local KindeUser record with Kinde ID: {retrieved_kinde_id}")
                 elif kinde_user_link.kinde_user_id == retrieved_kinde_id:
                     print(f"[INFO] Local KindeUser record already had the correct Kinde ID: {retrieved_kinde_id}")
            else:
                 print(f"[WARNING] Could not find local KindeUser link object (kinde_user_link) to update Kinde ID. This should not happen.")
        except Exception as update_err:
            print(f"[ERROR] Failed to update local KindeUser record with Kinde ID: {update_err}")
    else:
        print("\nSkipping update of local KindeUser record as no Kinde ID was retrieved.")

    print("\nSuperuser creation process complete.")
    
    # --- Call get_kinde_user_id.py script ---
    print("\n--- Executing get_kinde_user_id.py ---")
    get_user_id_script_path = os.path.join(os.path.dirname(__file__), 'get_kinde_user_id.py')
    
    # Check if the script exists before trying to run it
    if os.path.exists(get_user_id_script_path):
        try:
            # Use sys.executable to ensure the same Python environment is used
            result = subprocess.run([sys.executable, get_user_id_script_path], check=True, capture_output=True, text=True, timeout=60)
            print("[OK] Successfully executed get_kinde_user_id.py.")
            print(f"Output:\n{result.stdout}") 
            if result.stderr:
                 print(f"Errors:\n{result.stderr}") # Print stderr if any
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] get_kinde_user_id.py exited with status {e.returncode}.")
            print(f"Stderr:\n{e.stderr}")
            print(f"Stdout:\n{e.stdout}")
        except subprocess.TimeoutExpired:
            print(f"[ERROR] get_kinde_user_id.py timed out after 60 seconds.")
        except FileNotFoundError:
             print(f"[ERROR] Could not find Python executable specified by sys.executable: {sys.executable}")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while executing get_kinde_user_id.py: {e}")
    else:
        print(f"[ERROR] Could not find the script to execute: {get_user_id_script_path}")
    # --- End script call ---

if __name__ == '__main__':
    create_superuser_for_tenant(
        TARGET_TENANT_SCHEMA, 
        SUPERUSER_EMAIL, 
        SUPERUSER_FIRST_NAME, 
        SUPERUSER_LAST_NAME
    ) 