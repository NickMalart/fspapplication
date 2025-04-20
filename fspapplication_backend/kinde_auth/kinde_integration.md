# Kinde Authentication Integration Guide

This document outlines the steps and configuration required to integrate Kinde for authentication in the FSP Application.

## OpenID Connect Configuration

Kinde utilizes OpenID Connect (OIDC) for authentication. The necessary endpoint information can be found in the OpenID configuration discovery document:

- **Discovery URL:** `https://fspapplicationdev.kinde.com/.well-known/openid-configuration`

This URL provides details about authorization endpoints, token endpoints, user profile endpoints, supported response types, and claims.

## Authentication Flow

### 1. Initiating Sign-up / Sign-in

Redirect users from the application frontend (Vue.js) to the Kinde authorization endpoint.

- **Authorization Endpoint:** `https://fspapplicationdev.kinde.com/oauth2/auth`

**Required Query Parameters:**

- `response_type=code`: Specifies that we expect an authorization code.
- `client_id=f999f9947f6a4b39ab27ea5437b59346`: Your Kinde application's Client ID.
- `redirect_uri=http://localhost:3000`: The URL within your application where Kinde should redirect the user after successful authentication. **Note:** This will need to be updated for different environments (staging, production).
- `scope=openid+profile+email`: Defines the requested user information (standard OIDC scopes).
- `state=abc`: A random, unique, and non-guessable value used to prevent CSRF attacks. This should be generated dynamically for each request and verified upon callback.

**Example Redirect URL:**

```
https://fspapplicationdev.kinde.com/oauth2/auth?response_type=code&client_id=f999f9947f6a4b39ab27ea5437b59346&redirect_uri=http://localhost:3000&scope=openid+profile+email&state=<RANDOM_STATE_VALUE>
```

**Important:** Never include the `client_secret` in this URL.

### 2. Handling the Callback

After the user authenticates with Kinde, they will be redirected back to the `redirect_uri` specified in the previous step (`http://localhost:3000` in the example). Kinde will append an authorization `code` and the original `state` value as query parameters.

**Example Callback URL:**

```
http://localhost:3000?code=<CALLBACK_AUTHORIZATION_CODE>&state=<ORIGINAL_STATE_VALUE>
```

**Backend Implementation (Django `auth` app):**

- Create a view (e.g., `KindeCallbackView`) mapped to the `redirect_uri` path (`/callback` or similar).
- This view must:
    - Verify the received `state` parameter against the value stored before the redirect to prevent CSRF.
    - Extract the `code` parameter from the query string.

### 3. Exchanging Authorization Code for Tokens

Make a secure, server-to-server POST request from the Django backend (`auth` app) to the Kinde token endpoint to exchange the `code` for an access token, refresh token, and ID token.

- **Token Endpoint:** `https://fspapplicationdev.kinde.com/oauth2/token`

**Required POST Request Parameters (typically sent in the request body as `application/x-www-form-urlencoded`):**

- `client_id=f999f9947f6a4b39ab27ea5437b59346`: Your Kinde application's Client ID.
- `client_secret=h67zve1HENCduEAFtPoePFzbokdaM7QjMXDNs1JfKjHxlBhIi`: Your Kinde application's Client Secret. **Keep this secret secure on the backend.**
- `grant_type=authorization_code`: Specifies the grant type being used.
- `redirect_uri=http://localhost:3000`: The *exact same* redirect URI used in the initial authorization request.
- `code=<CALLBACK_AUTHORIZATION_CODE>`: The authorization code received in the callback step.

**Note:** If using PKCE (Proof Key for Code Exchange), the `code_verifier` parameter is also required. This is generally recommended for enhanced security, especially for public clients like SPAs.

**Response:**

Kinde will respond with a JSON object containing:

- `access_token`: A JWT used to authenticate API requests to your backend.
- `id_token`: A JWT containing user profile information (claims).
- `refresh_token`: (Optional, if configured) Used to obtain new access tokens without requiring the user to log in again.
- `expires_in`: The lifetime of the access token in seconds.
- `token_type`: Typically "Bearer".

**Backend Implementation:**

- The `KindeCallbackView` should perform this POST request.
- Handle potential errors from the token endpoint.
- Securely store the tokens (e.g., in the user's session or a secure HTTP-only cookie).

### 4. Verifying Tokens and User Session

- **ID Token:** Verify the signature and claims (like `iss`, `aud`, `exp`) of the `id_token` to confirm the user's identity. The public keys for signature verification can be found at the JWKS endpoint.
    - **JWKS Endpoint:** `https://fspapplicationdev.kinde.com/.well-known/jwks`
- **Access Token:** Verify the signature and claims (like `iss`, `aud`, `exp`, `scp`) of the `access_token` before accepting it for protected API requests. Use the same JWKS endpoint for verification.
- **User Management:**
    - Use the verified information from the `id_token` (like email or a unique subject ID) to find or create a corresponding `User` record in the *public* schema database.
    - Determine the user's tenant based on their Kinde information or potentially prompt them if needed.
    - Establish the user's session in Django.

## Signing Out

Implement a logout mechanism in your application:

1.  **Clear Local Session:** Clear any user-related data stored in the frontend (local/session storage) and backend (Django session).
2.  **Redirect to Kinde Logout:** Redirect the user's browser to the Kinde logout endpoint.
    - **Logout Endpoint:** `https://fspapplicationdev.kinde.com/logout`
3.  **Configure Kinde Logout Redirect:** In your Kinde application settings (Details page), add the URL(s) where users should be redirected *after* logging out from Kinde in the "Allowed logout redirect URLs" field (e.g., your application's login page).

## Security Considerations

- **State Parameter:** Always use and validate the `state` parameter during the OAuth flow to prevent CSRF.
- **PKCE:** Implement PKCE for added security, especially for the Vue.js frontend acting as a public client.
- **Client Secret:** Never expose the `client_secret` in frontend code or URLs. It should only be used in backend-to-backend communication.
- **Token Storage:** Store tokens securely. Avoid storing sensitive tokens like refresh tokens in browser local storage. Use secure, HTTP-only cookies or backend sessions.
- **Token Verification:** Rigorously verify the signature and claims (`iss`, `aud`, `exp`, `nonce` if used) of both ID and access tokens on the backend using the JWKS endpoint.
- **HTTPS:** Ensure all communication happens over HTTPS.
- **Redirect URIs:** Strictly configure and validate allowed `redirect_uri` values in Kinde to prevent open redirector vulnerabilities.

## Next Steps

- Implement the frontend redirect logic in Vue.js.
- Create the Django callback view in the `auth` app.
- Implement the token exchange logic in the callback view.
- Add token verification using a Python JWT library (e.g., `PyJWT` along with `cryptography`).
- Implement user lookup/creation based on Kinde ID token claims.
- Integrate access token verification into API views.
- Implement the logout flow. 