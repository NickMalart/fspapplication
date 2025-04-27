import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-$ubqr)l_jiei9@h!jd!h&9v+bj1orr*735i7bqpjhq4m7y4d(7)')

DEBUG = True

IS_PRODUCTION = os.environ.get('DJANGO_ENV') == 'production'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,.localhost,127.0.0.1,.127.0.0.1,.fly.dev').split(',')

if IS_PRODUCTION:
    DEBUG = False
    pass

ROOT_URLCONF = 'fspapplication_backend.urls'
WSGI_APPLICATION = 'fspapplication_backend.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# Applications & Middleware
# ==============================================================================

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
    'rest_framework',
    'rest_framework_simplejwt',
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

# ==============================================================================
# Django Tenants Configuration
# ==============================================================================
TENANT_MODEL = "tenant.Client"
TENANT_DOMAIN_MODEL = "tenant.Domain"
PUBLIC_SCHEMA_NAME = 'public'
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# ==============================================================================
# Database Configuration
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.environ.get('DB_NAME', 'neondb'),
        'USER': os.environ.get('DB_USER', 'neondb_owner'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'npg_oZKwX9T3VIsy'),
        'HOST': os.environ.get('DB_HOST', 'ep-broad-sun-a7w4swm3-pooler.ap-southeast-2.aws.neon.tech'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# ==============================================================================
# Authentication & Authorization
# ==============================================================================
AUTH_USER_MODEL = 'account.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

KINDE_DOMAIN = os.environ.get('KINDE_DOMAIN', 'https://fspapplicationdev.kinde.com')
KINDE_CLIENT_ID = os.environ.get('KINDE_CLIENT_ID', 'f999f9947f6a4b39ab27ea5437b59346')
KINDE_CLIENT_SECRET = os.environ.get('KINDE_CLIENT_SECRET', 'h67zve1HENCduEAFtPoePFzbokdaM7QjMXDNs1JfKjHxlBhIi')

DEFAULT_BACKEND_BASE_URL = os.environ.get('BACKEND_BASE_URL', 'http://localhost:8000')
KINDE_CALLBACK_URL = os.environ.get(
    'KINDE_CALLBACK_URL',
    f"{DEFAULT_BACKEND_BASE_URL}/auth/callback/"
)

KINDE_ISSUER = KINDE_DOMAIN
KINDE_JWKS_URL = f"{KINDE_DOMAIN}/.well-known/jwks.json"
KINDE_AUDIENCE = None

KINDE_MGMNT_CLIENT_ID = os.environ.get('KINDE_MGMNT_CLIENT_ID', 'e82153b23544405e8ef91a2d63429b12')
KINDE_MGMNT_CLIENT_SECRET = os.environ.get('KINDE_MGMNT_CLIENT_SECRET', 'BBtyc0U3IsUA8C7gK0jYpQkMhgOVaDNfwxfn9wjHkVshAq9QDdhi')
KINDE_MGMNT_AUDIENCE = os.environ.get('KINDE_MGMNT_AUDIENCE', f"{KINDE_DOMAIN}/api")


# ==============================================================================
# API Settings (Django REST Framework & Simple JWT)
# ==============================================================================
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
        'user': os.environ.get('DRF_USER_THROTTLE_RATE', '1000/day'),
        'anon': os.environ.get('DRF_ANON_THROTTLE_RATE', '100/day'),
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 60))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME_DAYS', 7))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}


# ==============================================================================
# Frontend Integration & URLs
# ==============================================================================
FRONTEND_BASE_URL = os.environ.get('FRONTEND_BASE_URL', 'http://dev.localhost:5173')
FRONTEND_CALLBACK_URL = os.environ.get('FRONTEND_CALLBACK_URL', 'http://dev.localhost:5173/auth/callback/')

# ==============================================================================
# CORS & CSRF Settings
# ==============================================================================
CORS_ALLOWED_ORIGINS_STR = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://127.0.0.1:5173,http://dev.127.0.0.1:5173,http://dev.localhost:5173,http://dev.localhost:8000,http://dev2.127.0.0.1:5173,http://dev2.localhost:5173,http://dev2.localhost:8000,https://fspapplication-dev.fly.dev,https://dev.fspapplication-dev.fly.dev'
)
CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS_STR.split(',') if CORS_ALLOWED_ORIGINS_STR else []

CSRF_TRUSTED_ORIGINS_STR = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'http://127.0.0.1:5173,http://dev.127.0.0.1:5173,http://dev.localhost:5173,http://dev.localhost:8000,http://dev2.127.0.0.1:5173,http://dev2.localhost:5173,http://dev2.localhost:8000,https://fspapplication-dev.fly.dev,https://dev.fspapplication-dev.fly.dev'
)
CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS_STR.split(',') if CSRF_TRUSTED_ORIGINS_STR else []

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

# ==============================================================================
# Security Settings
# ==============================================================================
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True' if IS_PRODUCTION else False
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True' if IS_PRODUCTION else False
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True') == 'True' if IS_PRODUCTION else False

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# ==============================================================================
# Static & Media Files (Storage)
# ==============================================================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

USE_LOCAL_STORAGE = os.environ.get('USE_LOCAL_STORAGE', 'True') == 'True'

if USE_LOCAL_STORAGE:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    STATICFILES_DIRS = []
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
else:
    TIGRIS_ACCESS_KEY_ID = os.environ.get('TIGRIS_ACCESS_KEY_ID')
    TIGRIS_SECRET_ACCESS_KEY = os.environ.get('TIGRIS_SECRET_ACCESS_KEY')
    TIGRIS_STORAGE_BUCKET_NAME = os.environ.get('TIGRIS_STORAGE_BUCKET_NAME')
    TIGRIS_REGION_NAME = os.environ.get('TIGRIS_REGION_NAME')
    TIGRIS_ENDPOINT_URL = os.environ.get('TIGRIS_ENDPOINT_URL')
    TIGRIS_ENDPOINT_URL_CUSTOM_DOMAIN = os.environ.get('TIGRIS_ENDPOINT_URL_CUSTOM_DOMAIN')

    if not all([TIGRIS_ACCESS_KEY_ID, TIGRIS_SECRET_ACCESS_KEY, TIGRIS_STORAGE_BUCKET_NAME, TIGRIS_REGION_NAME, TIGRIS_ENDPOINT_URL]):
        print("WARNING: S3/Tigris storage configured but essential environment variables are missing!")

    AWS_ACCESS_KEY_ID = TIGRIS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = TIGRIS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = TIGRIS_STORAGE_BUCKET_NAME
    AWS_S3_REGION_NAME = TIGRIS_REGION_NAME
    AWS_S3_ENDPOINT_URL = TIGRIS_ENDPOINT_URL
    AWS_S3_CUSTOM_DOMAIN = TIGRIS_ENDPOINT_URL_CUSTOM_DOMAIN

    AWS_S3_SECURE_URLS = True
    AWS_QUERYSTRING_AUTH = False

    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    STATIC_LOCATION = 'static'
    STATIC_URL = f'{AWS_S3_CUSTOM_DOMAIN or AWS_S3_ENDPOINT_URL}/{STATIC_LOCATION}/'

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_LOCATION = 'media'
    MEDIA_URL = f'{AWS_S3_CUSTOM_DOMAIN or AWS_S3_ENDPOINT_URL}/{MEDIA_LOCATION}/'

    AWS_DEFAULT_ACL = os.environ.get('AWS_DEFAULT_ACL', 'private')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

# ==============================================================================
# Templates Configuration
# ==============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


# ==============================================================================
# Logging Configuration
# ==============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
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
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_DB_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django_tenants': {
            'handlers': ['console'],
            'level': os.environ.get('TENANTS_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'kinde_auth': {
            'handlers': ['console'],
            'level': os.environ.get('KINDE_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        'fspapplication_backend': {
            'handlers': ['console'],
            'level': os.environ.get('APP_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        'account': {
            'handlers': ['console'],
            'level': os.environ.get('APP_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('ROOT_LOG_LEVEL', 'WARNING'),
    },
}

# ==============================================================================
# Third-Party Service Keys
# ==============================================================================
GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', 'AIzaSyDvfOM0JZd18BTt8kijxWo1gAOw6y0qy7U')

# ==============================================================================
# Miscellaneous Settings
# ==============================================================================
SITE_ID = 1
