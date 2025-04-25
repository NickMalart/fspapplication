from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-$ubqr)l_jiei9@h!jd!h&9v+bj1orr*735i7bqpjhq4m7y4d(7)')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False # IMPORTANT: Set to False in production
DEBUG = True  # WARNING: Running with debug enabled in production is a security risk
# DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,.localhost,127.0.0.1,.127.0.0.1,.fly.dev').split(',')

# Add a check for production environment to enforce stricter settings
IS_PRODUCTION = os.environ.get('DJANGO_ENV') == 'production'

if IS_PRODUCTION:
    DEBUG = False
    # Ensure ALLOWED_HOSTS is properly configured via environment variable for production
    # Example: os.environ.get('ALLOWED_HOSTS', 'yourdomain.com,.yourdomain.com').split(',')
    # Ensure CORS/CSRF origins are properly configured for production
    # Example: CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'https://yourfrontend.com').split(',')
    # Example: CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://yourfrontend.com').split(',')
    pass # Add production-specific overrides here if needed

# --- Kinde Authentication Settings --- 
# Ensure these are set as environment variables in production!
KINDE_DOMAIN = os.environ.get('KINDE_DOMAIN', 'https://fspapplicationdev.kinde.com')
KINDE_CLIENT_ID = os.environ.get('KINDE_CLIENT_ID', 'f999f9947f6a4b39ab27ea5437b59346')
KINDE_CLIENT_SECRET = 'h67zve1HENCduEAFtPoePFzbokdaM7QjMXDNs1JfKjHxlBhIi' # Hardcoded for local testing ONLY!

# Default callback URL - adjust if needed for production/staging
DEFAULT_BACKEND_BASE_URL = os.environ.get('BACKEND_BASE_URL', 'http://localhost:8000')
KINDE_CALLBACK_URL = os.environ.get(
    'KINDE_CALLBACK_URL',
    f"{DEFAULT_BACKEND_BASE_URL}/auth/callback/" 
)

# Derived Kinde URLs
KINDE_ISSUER = KINDE_DOMAIN
KINDE_JWKS_URL = f"{KINDE_DOMAIN}/.well-known/jwks.json"
# KINDE_AUDIENCE = KINDE_CLIENT_ID # Often the Client ID can serve as the Audience for ID tokens
KINDE_AUDIENCE = None # Disable audience check for ID token verification first
# --- End Kinde Settings ---

# --- Frontend Base URL --- 
# Used for redirects after Kinde callback
FRONTEND_BASE_URL = os.environ.get('FRONTEND_BASE_URL', 'http://dev.localhost:5173')
# --- End Frontend Base URL ---

# --- Kinde Management API (M2M) Settings ---
# For backend operations like creating users via API
# MUST be set via environment variables
# KINDE_MGMNT_CLIENT_ID = os.environ.get('KINDE_MGMNT_CLIENT_ID') 
KINDE_MGMNT_CLIENT_ID = 'e82153b23544405e8ef91a2d63429b12' # Hardcoded for local testing ONLY!
# KINDE_MGMNT_CLIENT_SECRET = os.environ.get('KINDE_MGMNT_CLIENT_SECRET')
KINDE_MGMNT_CLIENT_SECRET = 'BBtyc0U3IsUA8C7gK0jYpQkMhgOVaDNfwxfn9wjHkVshAq9QDdhi' # Hardcoded for local testing ONLY!
# The audience for the Kinde Management API (e.g., https://yourdomain.kinde.com/api)
KINDE_MGMNT_AUDIENCE = os.environ.get('KINDE_MGMNT_AUDIENCE', f"{KINDE_DOMAIN}/api")
# --- End Kinde Management API Settings ---

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',  # Adjust rates as needed
        'anon': '100/day',   # Adjust rates as needed
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://dev.127.0.0.1:5173",
    "http://dev.localhost:5173",
    "http://dev.localhost:8000", 
    "http://dev2.127.0.0.1:5173",
    "http://dev2.localhost:5173",
    "http://dev2.localhost:8000",
    "https://fspapplication-dev.fly.dev",
    "https://dev.fspapplication-dev.fly.dev",
]

# Allow cookies to be sent from these origins
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-dts-tenant', 
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://dev.127.0.0.1:5173",
    "http://dev.localhost:5173",
    "http://dev.localhost:8000", 
    "http://dev2.127.0.0.1:5173",
    "http://dev2.localhost:5173",
    "http://dev2.localhost:8000",
    "https://fspapplication-dev.fly.dev",
    "https://dev.fspapplication-dev.fly.dev",
]


# Application definition

SHARED_APPS = (
    'django_tenants',
    'tenant',
    'kinde_auth',
    'company',
    'dashboard',
    'client',
    'agent',
    'common_utils',
    'files',
    'corsheaders',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'rest_framework',
    'rest_framework_simplejwt',
    
)

TENANT_APPS = (
    'account',
    'company',
    'dashboard',
    'client',
    'agent',
    'common_utils',
    'files',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# --- Django Tenants Configuration ---
TENANT_MODEL = "tenant.Client" # app.Model
TENANT_DOMAIN_MODEL = "tenant.Domain" # app.Model
# --- End Django Tenants Configuration ---

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'fspapplication_backend.security_headers_middleware.SecurityHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'fspapplication_backend.custommiddleware.CustomTenantMiddleware',
    'fspapplication_backend.custommiddleware.TenantUserAccessMiddleware',
    'account.middleware.TenantUserLimitMiddleware',
]

ROOT_URLCONF = 'fspapplication_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fspapplication_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',  # ✅ Use Django-Tenants backend
        # Recommendation: Load sensitive DB details from environment variables
        'NAME': os.environ.get('DB_NAME', 'neondb'),
        'USER': os.environ.get('DB_USER', 'neondb_owner'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'npg_oZKwX9T3VIsy'), # Replace default if needed
        'HOST': os.environ.get('DB_HOST', 'ep-broad-sun-a7w4swm3-pooler.ap-southeast-2.aws.neon.tech'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',  # ✅ Enforce SSL for security
        }
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django_tenants': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'fspapplication_backend': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Add configuration to use local static files in production
# This is needed for the Vue.js frontend in Fly.io deployment
USE_LOCAL_STATIC_STORAGE = os.environ.get('USE_LOCAL_STATIC_STORAGE', 'True') == 'True'

if USE_LOCAL_STATIC_STORAGE:
    # Use local storage for static files
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
else:
    # Use S3 for static files
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# Tigris S3 compatible storage configuration using environment variables
TIGRIS_ACCESS_KEY_ID = os.environ.get('TIGRIS_ACCESS_KEY_ID')
TIGRIS_SECRET_ACCESS_KEY = os.environ.get('TIGRIS_SECRET_ACCESS_KEY')
TIGRIS_STORAGE_BUCKET_NAME = os.environ.get('TIGRIS_STORAGE_BUCKET_NAME')
TIGRIS_REGION_NAME = os.environ.get('TIGRIS_REGION_NAME')
TIGRIS_ENDPOINT_URL = os.environ.get('TIGRIS_ENDPOINT_URL') 
TIGRIS_ENDPOINT_URL_CUSTOM_DOMAIN = os.environ.get('TIGRIS_ENDPOINT_URL_CUSTOM_DOMAIN')
TIGRIS_DEFAULT_ACL = os.environ.get('TIGRIS_DEFAULT_ACL', 'private') # Using TIGRIS_ prefix
TIGRIS_S3_OBJECT_PARAMETERS = { # Using TIGRIS_ prefix
    'CacheControl': 'max-age=86400',
}

# CloudFront settings removed as per user request (using Tigris directly)
# CLOUDFRONT_DOMAIN = os.environ.get('CLOUDFRONT_DOMAIN', 'd1elaz1f509qmb.cloudfront.net')
# CLOUDFRONT_OAI_ID = os.environ.get('CLOUDFRONT_OAI_ID', '')
# AWS_S3_USE_OAI = os.environ.get('AWS_S3_USE_OAI', 'False') == 'True'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', 'AIzaSyDvfOM0JZd18BTt8kijxWo1gAOw6y0qy7U')

# Security Middleware Settings (Enable/Configure for Production)
# Ensure 'django.middleware.security.SecurityMiddleware' is high in your MIDDLEWARE list

SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True' if IS_PRODUCTION else False
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True' if IS_PRODUCTION else False
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True') == 'True' if IS_PRODUCTION else False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# HTTP Strict Transport Security (HSTS) - Enable carefully after testing HTTPS
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True