import os
import django
import sys
from django.conf import settings
import requests

# Set up Django environment - Moved *before* model import
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

# Import the KindeUser model
from kinde_auth.models import KindeUser

# --- Configuration ---
# Specify the email of the user you want to look up
TARGET_EMAIL = 'nmalartlp@gmail.com' 
# --- End Configuration ---

# --- Kinde API Helper (Copied from create_tenant_superuser.py) ---

def get_kinde_m2m_token():
    """Fetches an M2M access token from Kinde to use the Management API."""
    client_id = settings.KINDE_MGMNT_CLIENT_ID
    client_secret = settings.KINDE_MGMNT_CLIENT_SECRET
    audience = settings.KINDE_MGMNT_AUDIENCE
    token_url = f"{settings.KINDE_ISSUER}/oauth2/token"

    if not client_id or not client_secret:
        print("[ERROR] Kinde M2M Client ID or Secret not configured.")
        return None

    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': audience
    }

    try:
        print(f"Requesting Kinde M2M token from {token_url}...")
        response = requests.post(token_url, data=payload, timeout=15)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get('access_token')
        if not access_token:
            print(f"[ERROR] 'access_token' not found in Kinde M2M response.")
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

# --- Main Lookup Function ---

def find_kinde_user_id_by_email(email):
    """Queries Kinde API to find the user ID for a given email."""
    
    print(f"--- Attempting to find Kinde User ID for: {email} ---")
    
    # 1. Get M2M Token
    kinde_m2m_token = get_kinde_m2m_token()
    if not kinde_m2m_token:
        print("[ABORT] Cannot proceed without Kinde M2M token.")
        sys.exit(1)
        
    # 2. Construct API URL and Headers
    print(f"Attempting to GET user '{email}' from Kinde API...")
    try:
        # URL encode the email parameter
        encoded_email = requests.utils.quote(email)
        kinde_get_user_url = f"{settings.KINDE_ISSUER}/api/v1/users?email={encoded_email}"
    except Exception as url_err:
        print(f"[ERROR] Failed to construct Kinde API URL: {url_err}")
        sys.exit(1)
        
    headers = {
        'Authorization': f'Bearer {kinde_m2m_token}',
        'Accept': 'application/json'
    }
    
    # 3. Make API GET Request
    try:
        get_response = requests.get(kinde_get_user_url, headers=headers, timeout=15)
        print(f"API Request URL: {kinde_get_user_url}")
        print(f"API Response Status Code: {get_response.status_code}")
        get_response.raise_for_status() # Raise for 4xx/5xx errors
        
        get_data = get_response.json()
        users_list = get_data.get('users', [])
        
        # 4. Process Response
        if len(users_list) == 1:
            retrieved_kinde_id = users_list[0].get('id')
            if retrieved_kinde_id:
                print(f"\n[SUCCESS] Found Kinde User ID: {retrieved_kinde_id}")
                
                # --- Attempt to update local KindeUser record ---
                print(f"\nAttempting to update local KindeUser record for '{email}'...")
                try:
                    kinde_user_local = KindeUser.objects.using('default').get(email=email)
                    print(f"Found local KindeUser: Email='{kinde_user_local.email}', Current Kinde ID='{kinde_user_local.kinde_user_id}'")
                    
                    if kinde_user_local.kinde_user_id != retrieved_kinde_id:
                        print(f"Local Kinde ID ('{kinde_user_local.kinde_user_id}') differs from retrieved ID ('{retrieved_kinde_id}'). Updating...")
                        kinde_user_local.kinde_user_id = retrieved_kinde_id
                        kinde_user_local.save(using='default')
                        print(f"[OK] Successfully updated local KindeUser record with Kinde ID: {retrieved_kinde_id}")
                    else:
                        print(f"[INFO] Local KindeUser record already has the correct Kinde ID: {retrieved_kinde_id}")
                        
                except KindeUser.DoesNotExist:
                    print(f"[ERROR] Cannot update local record: KindeUser with email '{email}' not found in the database.")
                except KindeUser.MultipleObjectsReturned:
                     print(f"[ERROR] Cannot update local record: Multiple KindeUser records found for email '{email}'. Database integrity issue.")
                except Exception as db_err:
                    print(f"[ERROR] Failed to update local KindeUser record: {db_err}")
                # --- End local update ---
                
                return retrieved_kinde_id
            else:
                print(f"[WARNING] Found user '{email}' in Kinde API, but no 'id' field in response: {users_list[0]}")
                return None
        elif len(users_list) == 0:
            print(f"\n[NOT FOUND] Could not find user '{email}' via Kinde API GET request.")
            return None
        else:
            print(f"\n[AMBIGUOUS] Found multiple users ({len(users_list)}) for email '{email}' via Kinde API GET request. Cannot determine correct ID.")
            return None
            
    except requests.exceptions.RequestException as e:
        error_details = "No details available."
        if e.response is not None:
            try:
                error_details = e.response.json()
            except ValueError:
                error_details = e.response.text
            print(f"[ERROR] Failed GET request to find user in Kinde via API: {e}. Details: {error_details}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error during GET request to find user in Kinde via API: {e}")
        return None

# --- Script Execution ---

if __name__ == '__main__':
    if not TARGET_EMAIL:
        print("[CONFIG ERROR] Please set the TARGET_EMAIL variable in the script.")
    else:
        kinde_id = find_kinde_user_id_by_email(TARGET_EMAIL)
        if kinde_id:
            print(f"\nResult: The Kinde ID for {TARGET_EMAIL} is {kinde_id}")
        else:
            print(f"\nResult: Could not definitively retrieve the Kinde ID for {TARGET_EMAIL}.") 