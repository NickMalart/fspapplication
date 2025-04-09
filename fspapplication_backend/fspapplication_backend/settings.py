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
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = []

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=180),
    'ROTATE_REFRESH_TOKENS': False,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://dev.127.0.0.1:5173",
    "http://dev.localhost:5173",
    "http://dev.localhost:8000", 
    "http://dev2.127.0.0.1:5173",
    "http://dev2.localhost:5173",
    "http://dev2.localhost:8000", 
]

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
]


# Application definition

SHARED_APPS = (
    'django_tenants',
    'tenant',    
    'account',
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

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'fspapplication_backend.custommiddleware.CustomTenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
        'NAME': 'neondb',  # ✅ Database name from your NeonDB URL
        'USER': 'neondb_owner',  # ✅ Username from your NeonDB URL
        'PASSWORD': 'npg_oZKwX9T3VIsy',  # ✅ Password from your NeonDB URL
        'HOST': 'ep-broad-sun-a7w4swm3-pooler.ap-southeast-2.aws.neon.tech',  # ✅ Host from your NeonDB URL
        'PORT': '5432',  # ✅ PostgreSQL default port
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

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# AWS S3 configuration using environment variables
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = os.environ.get('AWS_DEFAULT_ACL', 'private')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# CloudFront settings
CLOUDFRONT_DOMAIN = os.environ.get('CLOUDFRONT_DOMAIN', 'd1elaz1f509qmb.cloudfront.net')
CLOUDFRONT_OAI_ID = os.environ.get('CLOUDFRONT_OAI_ID', '')
AWS_S3_USE_OAI = os.environ.get('AWS_S3_USE_OAI', 'False') == 'True'

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

TENANT_MODEL = "tenant.Client" 

TENANT_DOMAIN_MODEL = "tenant.Domain"

AUTH_USER_MODEL = 'account.User'

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', 'AIzaSyDvfOM0JZd18BTt8kijxWo1gAOw6y0qy7U')