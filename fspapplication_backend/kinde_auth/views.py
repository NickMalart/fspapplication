from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.conf import settings
import requests # Make sure requests is installed

# Placeholder for JWT verification later
# from jose import jwt, jwk
# from jose.exceptions import JOSEError

# Placeholder for Django auth later
# from django.contrib.auth import login

# Placeholder for tenant/auth models later
# from tenant.models import Client
# from .models import KindeUser

class KindeCallbackView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        print("--- Kinde Callback Received ---")
        code = request.GET.get('code')
        state = request.GET.get('state') # We will need to validate this later

        if not code:
            print("Callback Error: 'code' parameter missing.")
            return HttpResponseBadRequest("Missing authorization code.")
        
        print(f"Received code: {code[:10]}... (truncated)") # Truncate code for logging
        print(f"Received state: {state}")
        
        # --- TODO: Step 1: Validate state parameter --- 
        # Compare 'state' with the value stored in the session before redirecting to Kinde
        # If mismatch, return error (potential CSRF)
        print("State validation is currently skipped.")

        # --- TODO: Step 2: Exchange code for tokens --- 
        print("Attempting to exchange code for tokens...")
        token_url = f"{settings.KINDE_DOMAIN}/oauth2/token"
        redirect_uri = request.build_absolute_uri(request.path) # Or construct from settings/request
        
        payload = {
            'grant_type': 'authorization_code',
            'client_id': settings.KINDE_CLIENT_ID,
            'client_secret': settings.KINDE_CLIENT_SECRET,
            'code': code,
            'redirect_uri': redirect_uri,
            # 'scope': 'openid profile email' # Often needed, depends on Kinde setup
        }
        
        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            token_data = response.json()
            print("Successfully exchanged code for tokens.")
            # print(f"Token data received: {token_data}") # Careful logging tokens
            id_token = token_data.get('id_token')
            access_token = token_data.get('access_token') # May need this later

            if not id_token:
                 print("Token Error: ID token missing in response.")
                 return HttpResponse("Authentication failed: ID token missing.", status=500)

            # --- TODO: Step 3: Verify ID Token --- 
            print("ID Token verification is currently skipped.")
            # Fetch JWKS from Kinde
            # Verify signature using JWKS
            # Verify claims (iss, aud, exp, nonce if used)
            # Extract user info (sub, email, name etc.) from verified token
            # placeholder_kinde_id = "real_kinde_id_from_token"
            # placeholder_email = "real_email_from_token"
            
            # --- TODO: Step 4: Find/Update KindeUser and Get Tenant --- 
            print("Finding/Updating KindeUser is currently skipped.")
            # Look up KindeUser by placeholder_email in public schema
            # If found:
            #   Update user record with placeholder_kinde_id
            #   Get associated tenant
            # If not found:
            #   Handle error: User not pre-associated
            # placeholder_tenant = None # Get the actual tenant object
            
            # --- TODO: Step 5: Switch Schema and Log In --- 
            print("Switching schema and logging in is currently skipped.")
            # if placeholder_tenant:
            #   connection.set_tenant(placeholder_tenant)
            #   # Find corresponding account.User if necessary
            #   # login(request, django_user_object) 
            #   print(f"Switched to tenant: {placeholder_tenant.schema_name}")
            # else:
            #   Handle error: Tenant not found for user
            
            # --- TODO: Step 6: Redirect --- 
            print("Redirecting to placeholder dashboard...")
            # Replace with actual tenant dashboard URL
            return redirect('/') # Redirect to homepage for now

        except requests.exceptions.RequestException as e:
            print(f"Token Exchange Error: {e}")
            # Log the error details securely
            return HttpResponse("Authentication failed during token exchange.", status=500)
        except Exception as e:
            print(f"Callback Processing Error: {e}")
            # Log the error details securely
            return HttpResponse("An internal error occurred during authentication.", status=500)

        # Fallback return (should ideally be handled above)
        return HttpResponse("Authentication callback processing finished (intermediate stage).")

# TODO: Add KindeLoginView
# TODO: Add KindeLogoutView
