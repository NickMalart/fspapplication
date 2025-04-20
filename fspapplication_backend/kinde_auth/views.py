from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.conf import settings
from django.contrib.auth import login
from django.db import connection
from django.urls import reverse
import requests
import uuid
from urllib.parse import urljoin

# JWT verification
from jose import jwt, jwk
from jose.exceptions import JOSEError, JWTError
import time 

# Models
from tenant.models import Client
from .models import KindeUser
from django.contrib.auth import get_user_model
User = get_user_model()

# --- Helper Functions ---

def fetch_jwks(jwks_url):
    """Fetches JWKS keys from Kinde."""
    try:
        response = requests.get(jwks_url, timeout=10) # Add timeout
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JWKS: {e}")
        return None

def verify_id_token(id_token, jwks, audience, issuer, access_token):
    """Verifies the ID token signature and claims."""
    try:
        # Find the key used to sign the token
        header = jwt.get_unverified_header(id_token)
        signing_key = None
        for key in jwks['keys']:
            if key['kid'] == header['kid']:
                signing_key = key
                break
        
        if not signing_key:
            print("Signing key not found in JWKS.")
            return None

        # Decode and verify
        # `audience` check is strict. If KINDE_AUDIENCE is None, it won't check audience.
        options = {
            "verify_signature": True,
            "verify_aud": audience is not None,
            "verify_iss": True,
            "verify_exp": True,
        }
        payload = jwt.decode(
            id_token,
            signing_key,
            algorithms=[header['alg']],
            audience=audience,
            issuer=issuer,
            options=options,
            access_token=access_token
        )
        print("ID Token verified successfully.")
        return payload

    except JWTError as e:
        print(f"JWT Verification Error: {e}")
        return None
    except Exception as e:
        print(f"General Token Verification Error: {e}")
        return None

# --- Kinde Views ---

class KindeLoginView(View):
    """Initiates the Kinde OIDC login flow."""
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        state = uuid.uuid4().hex # Generate unique state
        request.session['oauth_state'] = state # Store state in session
        # Store nonce and expiry if using nonce validation (recommended)

        auth_url = f"{settings.KINDE_ISSUER}/oauth2/auth"
        params = {
            'response_type': 'code',
            'client_id': settings.KINDE_CLIENT_ID,
            'redirect_uri': settings.KINDE_CALLBACK_URL,
            'scope': 'openid profile email', # Request necessary scopes
            'state': state,
            # 'nonce': nonce, # Add if using nonce validation
        }
        
        # Use requests library to correctly encode parameters
        login_url = requests.Request('GET', auth_url, params=params).prepare().url
        print(f"Redirecting to Kinde: {login_url}")
        return redirect(login_url)

class KindeCallbackView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        print("--- Kinde Callback Received ---")
        error = request.GET.get('error')
        if error:
            error_desc = request.GET.get('error_description', 'No description provided.')
            print(f"Kinde Error: {error} - {error_desc}")
            return HttpResponseBadRequest(f"Error during Kinde authentication: {error_desc}")

        code = request.GET.get('code')
        state = request.GET.get('state')

        if not code:
            print("Callback Error: 'code' parameter missing.")
            return HttpResponseBadRequest("Missing authorization code.")
        
        print(f"Received code: {code[:10]}... (truncated)")
        print(f"Received state: {state}")
        
        # --- Step 1: Validate state parameter --- 
        session_state = request.session.pop('oauth_state', None)
        if not state or state != session_state:
            print("State mismatch error. Potential CSRF attack.")
            return HttpResponseBadRequest("Invalid state parameter.")
        print("State validation successful.")

        # --- Step 2: Exchange code for tokens --- 
        print("Attempting to exchange code for tokens...")
        token_url = f"{settings.KINDE_ISSUER}/oauth2/token"
        # Ensure redirect_uri matches exactly what was sent in the initial auth request
        redirect_uri = settings.KINDE_CALLBACK_URL 
        
        payload = {
            'grant_type': 'authorization_code',
            'client_id': settings.KINDE_CLIENT_ID,
            'client_secret': settings.KINDE_CLIENT_SECRET,
            'code': code,
            'redirect_uri': redirect_uri,
            # 'scope': 'openid profile email' # Scope usually not needed here
        }
        
        try:
            response = requests.post(token_url, data=payload, timeout=15)
            response.raise_for_status() 
            token_data = response.json()
            print("Successfully exchanged code for tokens.")
            
            id_token = token_data.get('id_token')
            access_token = token_data.get('access_token') 
            refresh_token = token_data.get('refresh_token') # Store if needed

            if not id_token:
                 print("Token Error: ID token missing in response.")
                 return HttpResponse("Authentication failed: ID token missing.", status=500)

            # --- Step 3: Verify ID Token --- 
            print("Fetching JWKS...")
            jwks = fetch_jwks(settings.KINDE_JWKS_URL)
            if not jwks:
                return HttpResponse("Failed to fetch JWKS for token verification.", status=500)
                
            print("Verifying ID Token...")
            verified_payload = verify_id_token(
                id_token,
                jwks,
                settings.KINDE_AUDIENCE, # Can be None if no specific audience
                settings.KINDE_ISSUER,
                access_token # Pass the received access token here
            )
            
            if not verified_payload:
                print("ID Token verification failed.")
                return HttpResponse("Invalid ID Token.", status=403) # Forbidden
            
            # Extract user info from *verified* token
            kinde_user_id = verified_payload.get('sub') # Subject (unique Kinde ID)
            email = verified_payload.get('email')
            given_name = verified_payload.get('given_name', '')
            family_name = verified_payload.get('family_name', '')

            if not kinde_user_id or not email:
                print("Essential claims (sub, email) missing from token.")
                return HttpResponse("Incomplete user information from Kinde.", status=500)
                
            print(f"Token verified for email: {email}, Kinde ID: {kinde_user_id}")

            # --- Step 4: Find KindeUser, associated Tenant(s), and Update ID --- 
            print(f"Looking up KindeUser for email: {email} in public schema...")
            try:
                # Query public schema explicitly
                kinde_user_link = KindeUser.objects.using('default').prefetch_related('tenants', 'tenants__domains').get(email__iexact=email)
                
                # Get associated tenants
                associated_tenants = list(kinde_user_link.tenants.all())
                
                if len(associated_tenants) == 1:
                    tenant = associated_tenants[0]
                    print(f"Found KindeUser link. User belongs to single tenant: {tenant.name} ({tenant.schema_name})")
                elif len(associated_tenants) == 0:
                    print(f"Error: KindeUser {email} found but not associated with any tenant.")
                    return HttpResponse("Authentication failed: User has no assigned tenant.", status=403)
                else: # More than one tenant associated
                    # TODO: Implement tenant selection logic here if needed in the future
                    # For now, treat as an error or pick the first one?
                    # Picking the first one for now, but this might be ambiguous.
                    tenant = associated_tenants[0] 
                    tenant_names = ", ".join([t.name for t in associated_tenants])
                    print(f"Warning: KindeUser {email} associated with multiple tenants ({tenant_names}). Proceeding with first tenant: {tenant.name}")
                    # return HttpResponse(f"Ambiguous login: User belongs to multiple tenants ({tenant_names}).", status=400)
                
                # Update kinde_user_id if it's missing or changed
                if kinde_user_link.kinde_user_id is None or kinde_user_link.kinde_user_id != kinde_user_id:
                    kinde_user_link.kinde_user_id = kinde_user_id
                    kinde_user_link.save(using='default')
                    print(f"Updated KindeUser record with kinde_user_id: {kinde_user_id}")
                    
            except KindeUser.DoesNotExist:
                print(f"Error: No KindeUser found for email {email}. User must be pre-registered.")
                # Redirect to an error page or show a message
                return HttpResponse("Authentication failed: User not registered in this system.", status=403)
            except Exception as e:
                print(f"Error finding/updating KindeUser: {e}")
                return HttpResponse("An internal error occurred during user lookup.", status=500)
            
            # --- Step 5: Switch Schema and Log In --- 
            print(f"Switching to tenant schema: {tenant.schema_name}")
            try:
                connection.set_tenant(tenant)
                
                # Find the corresponding User within the tenant schema
                # *** This requires 'account' app to be in TENANT_APPS ***
                user = User.objects.get(email__iexact=email)
                print(f"Found tenant user: {user.email}")
                
                # Ensure user is active before login
                if not user.is_active:
                    print(f"Login failed: User {email} is inactive.")
                    connection.set_schema_to_public() # Switch back
                    return HttpResponse("Authentication failed: Account is inactive.", status=403)
                
                # Log the user into the Django session
                login(request, user) 
                print(f"User {user.email} logged in successfully.")
                
                # Store tokens in session if needed for backend API calls
                # request.session['access_token'] = access_token
                # request.session['refresh_token'] = refresh_token
                # request.session['id_token'] = id_token # May not need to store full ID token
                
            except User.DoesNotExist:
                # This *shouldn't* happen if KindeUser existed, but handle defensively
                print(f"CRITICAL Error: KindeUser found for {email}, but no corresponding User in tenant schema '{tenant.schema_name}'.")
                connection.set_schema_to_public() # Switch back
                return HttpResponse("Authentication failed: User record mismatch.", status=500)
            except Exception as e:
                print(f"Error switching schema or finding tenant user: {e}")
                connection.set_schema_to_public() # Switch back
                return HttpResponse("An internal error occurred during login.", status=500)
            finally:
                # Always switch back to public schema after request processing within tenant context
                # Note: Django-tenants middleware might handle this automatically depending on setup,
                # but being explicit here can be safer within the view.
                connection.set_schema_to_public()
            
            # --- Step 6: Redirect --- 
            print("Redirecting to tenant dashboard...")
            # Find the primary domain for the selected tenant
            primary_domain = None
            for domain in tenant.domains.all(): # Use cached domains from prefetch
                if domain.is_primary:
                    primary_domain = domain
                    break
                    
            if primary_domain:
                # Construct URL using tenant's primary domain
                # Determine scheme based on request or settings
                scheme = 'https' if request.is_secure() or not settings.DEBUG else 'http' 
                # Construct dashboard path (adjust if needed)
                dashboard_path = "/dashboard"
                # Assume frontend runs on a different port in development (e.g., 5173)
                # In production, the domain might handle routing without port needed?
                # You might need a more robust way to determine the frontend port/URL base.
                port_suffix = ":5173" if settings.DEBUG and ':' not in primary_domain.domain else ""
                dashboard_url = f"{scheme}://{primary_domain.domain}{port_suffix}{dashboard_path}"
                print(f"Redirecting to: {dashboard_url}")
            else:
                print(f"Error: No primary domain found for tenant {tenant.name}. Cannot redirect.")
                # Fallback redirect or error page
                # For now, redirecting to root, but this should be handled better.
                dashboard_url = '/' 
            
            return redirect(dashboard_url)

        except requests.exceptions.RequestException as e:
            print(f"Token Exchange Error: {e}")
            # Check if response object exists and has content
            error_details = "No details available."
            if e.response is not None:
                try:
                    error_details = e.response.json() 
                except ValueError:
                    error_details = e.response.text
            print(f"Error details: {error_details}")
            return HttpResponse(f"Authentication failed during token exchange: {error_details}", status=500)
        except Exception as e:
            print(f"Callback Processing Error: {e}")
            return HttpResponse("An internal error occurred during authentication.", status=500)

# TODO: Add KindeLogoutView
