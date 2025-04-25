from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.conf import settings
from django.contrib.auth import login, logout
from django.db import connection
from django.urls import reverse
import requests
import uuid
from urllib.parse import urljoin, urlencode
import os
import logging # Add logging
import time # Import time for token expiry
import json

# JWT verification
from jose import jwt, jwk
from jose.exceptions import JOSEError, JWTError

# Simple JWT Token Generation
from rest_framework_simplejwt.tokens import RefreshToken
# Import AuthenticationFailed for explicit error handling if needed
from rest_framework_simplejwt.exceptions import AuthenticationFailed
# Import Django signing tools
from django.core.signing import Signer, BadSignature, SignatureExpired

# Models
from tenant.models import Client
from .models import KindeUser
from django.contrib.auth import get_user_model
User = get_user_model()

# Get logger instance
logger = logging.getLogger(__name__)

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
    # Set a duration for the temporary token (e.g., 5 minutes)
    TEMP_TOKEN_MAX_AGE_SECONDS = 300 

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        logger.debug("--- Kinde Callback Received ---")
        error = request.GET.get('error')
        if error:
            error_desc = request.GET.get('error_description', 'No description provided.')
            logger.error(f"Kinde Error: {error} - {error_desc}")
            # Return JSON error for frontend to handle potentially
            return JsonResponse({'error': 'kinde_authentication_error', 'detail': error_desc}, status=400)

        code = request.GET.get('code')
        state = request.GET.get('state')

        if not code:
            logger.error("Callback Error: 'code' parameter missing.")
            return JsonResponse({'error': 'missing_code'}, status=400)
        
        logger.debug(f"Received code: {code[:10]}... (truncated)")
        logger.debug(f"Received state: {state}")
        
        # --- Step 1: Validate state parameter --- 
        session_state = request.session.pop('oauth_state', None)
        if not state or state != session_state:
            logger.warning("State mismatch error. Potential CSRF attack.")
            return JsonResponse({'error': 'invalid_state'}, status=400)
        logger.debug("State validation successful.")

        # --- Step 2: Exchange code for tokens --- 
        logger.debug("Attempting to exchange code for tokens...")
        token_url = f"{settings.KINDE_ISSUER}/oauth2/token"
        redirect_uri = settings.KINDE_CALLBACK_URL 
        
        payload = {
            'grant_type': 'authorization_code',
            'client_id': settings.KINDE_CLIENT_ID,
            'client_secret': settings.KINDE_CLIENT_SECRET,
            'code': code,
            'redirect_uri': redirect_uri,
        }
        
        try:
            token_response = requests.post(token_url, data=payload, timeout=15)
            token_response.raise_for_status() 
            token_data = token_response.json()
            logger.debug("Successfully exchanged code for tokens.")
            
            id_token = token_data.get('id_token')
            access_token_kinde = token_data.get('access_token') # Kinde's access token (might differ from our app's)
            refresh_token_kinde = token_data.get('refresh_token') # Kinde's refresh token

            if not id_token:
                 logger.error("Token Error: ID token missing in response.")
                 return JsonResponse({'error': 'id_token_missing'}, status=500)

            # --- Step 3: Verify ID Token --- 
            logger.debug("Fetching JWKS...")
            jwks = fetch_jwks(settings.KINDE_JWKS_URL)
            if not jwks:
                logger.error("Failed to fetch JWKS for token verification.")
                return JsonResponse({'error': 'jwks_fetch_failed'}, status=500)
                
            logger.debug("Verifying ID Token...")
            verified_payload = verify_id_token(
                id_token,
                jwks,
                settings.KINDE_AUDIENCE, 
                settings.KINDE_ISSUER,
                access_token_kinde # Pass the received Kinde access token here
            )
            
            if not verified_payload:
                logger.warning("ID Token verification failed.")
                return JsonResponse({'error': 'invalid_id_token'}, status=403) # Forbidden
            
            # Extract user info from *verified* token
            kinde_user_id = verified_payload.get('sub') 
            email = verified_payload.get('email')
            given_name = verified_payload.get('given_name', '')
            family_name = verified_payload.get('family_name', '')

            if not kinde_user_id or not email:
                logger.error("Essential claims (sub, email) missing from token.")
                return JsonResponse({'error': 'incomplete_kinde_claims'}, status=500)
                
            logger.info(f"Token verified for email: {email}, Kinde ID: {kinde_user_id}")

            # --- Step 4: Find KindeUser, associated Tenant(s), and Update ID --- 
            logger.debug(f"Looking up KindeUser for email: {email} in public schema...")
            try:
                # Query public schema explicitly, prefetch related tenants and their domains
                kinde_user_link = KindeUser.objects.using('default').prefetch_related('tenants__domains').get(email__iexact=email)
                
                # Get associated tenants
                associated_tenants = list(kinde_user_link.tenants.all())
                
                # Update kinde_user_id if it's missing or changed (do this regardless of tenant count)
                if kinde_user_link.kinde_user_id is None or kinde_user_link.kinde_user_id != kinde_user_id:
                    kinde_user_link.kinde_user_id = kinde_user_id
                    # Also update names if they are blank in our record but present in Kinde's token
                    if not kinde_user_link.first_name and given_name:
                         kinde_user_link.first_name = given_name
                    if not kinde_user_link.last_name and family_name:
                         kinde_user_link.last_name = family_name
                    kinde_user_link.save(using='default')
                    logger.info(f"Updated KindeUser record for {email} with kinde_user_id and potentially names.")
                    
            except KindeUser.DoesNotExist:
                logger.warning(f"Error: No KindeUser found for email {email}. User must be pre-registered.")
                # Redirect to an error page or show a message
                return JsonResponse({'error': 'user_not_registered'}, status=403)
            except Exception as e:
                logger.exception(f"Error finding/updating KindeUser for {email}: {e}")
                return JsonResponse({'error': 'user_lookup_failed', 'detail': str(e)}, status=500)

            # --- Step 5: Handle Tenant Scenarios ---
            
            num_tenants = len(associated_tenants)
            logger.info(f"User {email} is associated with {num_tenants} tenant(s).")

            # Always require tenant selection if user has *any* assigned tenants
            if num_tenants == 0:
                logger.warning(f"Authentication failed for {email}: User has no assigned tenant.")
                # Option: Redirect to a frontend error page?
                # frontend_error_url = f"{settings.FRONTEND_BASE_URL}/auth-error?error=no_tenant_assigned"
                # return redirect(frontend_error_url)
                return JsonResponse({'error': 'no_tenant_assigned'}, status=403) # Keep JSON for now, frontend can handle

            # Now, if num_tenants >= 1, proceed to tenant selection flow
            else:
                # --- Redirect to Frontend with Temp Token for selection ---
                tenant_names = ", ".join([t.name for t in associated_tenants])
                logger.info(f"User {email} associated with {num_tenants} tenant(s) ({tenant_names}). Redirecting to frontend for selection.")

                # Prepare tenant data for frontend
                tenants_data = []
                for t in associated_tenants:
                    domain_obj = t.domains.filter(is_primary=True).first() or t.domains.first()
                    tenants_data.append({
                        'name': t.name,
                        'schema_name': t.schema_name,
                        'domain': domain_obj.domain if domain_obj else None
                    })

                try:
                    # Generate a short-lived signed token containing essential verified info
                    signer = Signer()
                    payload_to_sign = {
                        'email': email,
                        'sub': kinde_user_id, # Kinde subject ID
                        'exp': int(time.time()) + self.TEMP_TOKEN_MAX_AGE_SECONDS
                    }
                    temp_token = signer.sign_object(payload_to_sign)
                    logger.debug(f"Generated temporary token for {email}")

                    # ---> NEW CODE: Redirect to Frontend <---
                    frontend_callback_url = settings.FRONTEND_CALLBACK_URL # Ensure this is defined in settings.py

                    # Encode tenants_data as JSON string to pass in URL
                    tenants_json = json.dumps(tenants_data)

                    query_params = urlencode({
                        'status': 'select_tenant',
                        'temp_token': temp_token,
                        'tenants': tenants_json # Pass JSON string
                    })

                    redirect_url = f"{frontend_callback_url}?{query_params}"
                    logger.debug(f"Redirecting browser to frontend callback: {redirect_url}")
                    return redirect(redirect_url) # Use Django's redirect shortcut

                except Exception as e:
                     logger.exception(f"Error during temporary token generation or redirect prep for {email}: {e}")
                     # Redirect to a frontend error page if possible
                     # frontend_error_url = f"{settings.FRONTEND_BASE_URL}/auth-error?error=token_error"
                     # return redirect(frontend_error_url)
                     return JsonResponse({'error': 'multi_tenant_token_error', 'detail': str(e)}, status=500)


        except requests.exceptions.RequestException as e:
            logger.exception(f"Token Exchange Error: {e}")
            error_details = "No details available."
            if e.response is not None:
                try:
                    error_details = e.response.json() 
                except ValueError: # If response is not JSON
                    error_details = e.response.text
            logger.error(f"Token exchange failed. Details: {error_details}")
            return JsonResponse({'error': 'token_exchange_failed', 'detail': str(error_details)}, status=500)
        except Exception as e:
            logger.exception(f"General Callback Processing Error: {e}")
            # Ensure schema is switched back if error happened before finally block
            if connection.schema_name != settings.PUBLIC_SCHEMA_NAME:
                 logger.warning(f"Exception handler: Current schema is {connection.schema_name}, switching back.")
                 connection.set_schema_to_public()
            return JsonResponse({'error': 'internal_server_error', 'detail': str(e)}, status=500)

class KindeLogoutView(View):
    """Logs the user out of the Django session and initiates Kinde SLO."""
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        print("--- Kinde Logout Initiated ---")

        # Log the user out of the Django session first
        logout(request)
        print("Django session cleared.")

        # Construct the Kinde end session endpoint URL
        # Ensure your KINDE_POST_LOGOUT_REDIRECT_URL is configured in Kinde settings
        # and matches where you want users to land after logout (e.g., your base frontend URL)
        # If KINDE_POST_LOGOUT_REDIRECT_URL is not set, Kinde might redirect to a default.
        kinde_logout_url = f"{settings.KINDE_ISSUER}/logout"
        
        # The post_logout_redirect_uri tells Kinde where to send the user back *after* Kinde logout
        post_logout_redirect_uri = os.environ.get('KINDE_POST_LOGOUT_REDIRECT_URL', settings.FRONTEND_BASE_URL + '/') # Default to frontend base

        params = {
            'post_logout_redirect_uri': post_logout_redirect_uri
            # Kinde might support id_token_hint but it's often not strictly necessary for basic logout
        }
        
        # Build the full URL with parameters
        logout_redirect_url = f"{kinde_logout_url}?{urlencode(params)}"
        
        print(f"Redirecting to Kinde end session endpoint: {logout_redirect_url}")
        
        # Redirect the browser to Kinde's logout endpoint
        # Use HttpResponseTemporaryRedirect (307) or PermanentRedirect (308)
        # A simple redirect (302) is often sufficient here.
        return redirect(logout_redirect_url)

# --- Tenant Login Finalization View ---
class FinalizeLoginView(View):
    """Handles the final login step on the tenant domain using a temporary token."""
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        logger.debug(f"--- Finalize Login Request Received on schema: {connection.schema_name} ---")
        token = request.GET.get('token')
        if not token:
            logger.warning("Finalize login failed: Missing temporary token.")
            return JsonResponse({'error': 'missing_token'}, status=400)
        
        signer = Signer()
        try:
            # Note: unsign_object doesn't automatically check expiry
            payload = signer.unsign_object(token) 
            logger.debug(f"Successfully unsigned temporary token.")
            
            # Manual expiry check
            if time.time() > payload.get('exp', 0):
                logger.warning("Finalize login failed: Temporary token has expired.")
                raise SignatureExpired("Token has expired.")
                
            email = payload.get('email')
            kinde_sub = payload.get('sub') # Optional: Can verify against KindeUser if needed

            if not email:
                 logger.error("Finalize login failed: Email missing from temporary token payload.")
                 return JsonResponse({'error': 'invalid_token_payload'}, status=400)
            
            # We should be in the tenant context because this view is accessed via tenant domain
            logger.info(f"Finalizing login for {email} in schema {connection.schema_name} using temp token.")
            
            # Find the user within the *current* tenant schema
            user = User.objects.get(email__iexact=email)
            logger.debug(f"Found tenant user: {user.email} (ID: {user.id})")

            if not user.is_active:
                 logger.warning(f"Login finalization failed for {email}: User account is inactive in this tenant.")
                 return JsonResponse({'error': 'account_inactive'}, status=403)
                 
            # Log the user into the Django session for this tenant domain
            login(request, user) 
            logger.info(f"User {email} logged into Django session for tenant {connection.schema_name}.")
            
            # Generate final tenant-specific JWTs
            logger.debug("Generating final JWT tokens...")
            refresh = RefreshToken.for_user(user)
            app_access_token = str(refresh.access_token)
            app_refresh_token = str(refresh)
            logger.debug("Final JWT tokens generated.")
            
            # Return tokens in JSON 
            logger.info(f"Login finalization successful for {email}. Returning JWTs.")
            return JsonResponse({
                'access_token': app_access_token,
                'refresh_token': app_refresh_token,
                'user_email': user.email, 
                'tenant_schema_name': connection.schema_name 
            })

        except (BadSignature, SignatureExpired) as e:
            logger.warning(f"Invalid or expired temporary token received: {e}")
            return JsonResponse({'error': 'invalid_or_expired_token', 'detail': str(e)}, status=403)
        except User.DoesNotExist:
            logger.error(f"Login finalization failed: User {email} not found in current schema {connection.schema_name}.")
            # This shouldn't happen if KindeUser was linked correctly, but handle defensively
            return JsonResponse({'error': 'tenant_user_not_found'}, status=403) 
        except Exception as e:
            # Log the email if available, otherwise just the error
            log_email = email if 'email' in locals() else 'unknown'
            logger.exception(f"Error during login finalization for {log_email}: {e}")
            return JsonResponse({'error': 'finalize_login_error', 'detail': str(e)}, status=500)

# TODO: Add KindeLogoutView
