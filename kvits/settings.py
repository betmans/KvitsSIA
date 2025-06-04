import os
from pathlib import Path
import dj_database_url
# For Google Cloud Storage for static and media files
# You'll need to add 'django-storages' to your requirements.txt
# pip install django-storages[google]
# from storages.backends.gcloud import GoogleCloudStorage # Uncomment when using GCS for media/static

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Secrets Management ---
# SECRET_KEY should be loaded from an environment variable.
# In Cloud Run, set this environment variable, ideally populated from Google Secret Manager.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY and os.environ.get('DJANGO_DEBUG', 'True') == 'True':
    # Fallback for local development if DJANGO_SECRET_KEY is not set and DEBUG is True
    SECRET_KEY = 'your-fallback-local-secret-key-for-dev-only' # Make sure this is not used in prod

# --- Debugging ---
# DEBUG should be False in production. Load from environment variable.
# Set DJANGO_DEBUG="False" in Cloud Run environment variables for production.
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# --- Allowed Hosts ---
# ALLOWED_HOSTS will be your Cloud Run service URL(s) and any custom domains.
# Load from a space-separated environment variable.
# Example in Cloud Run env var: DJANGO_ALLOWED_HOSTS="your-service-name.a.run.app yourcustomdomain.com"
ALLOWED_HOSTS_STRING = os.environ.get('DJANGO_ALLOWED_HOSTS')
if ALLOWED_HOSTS_STRING:
    ALLOWED_HOSTS = ALLOWED_HOSTS_STRING.split(' ')
elif DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0'] # For local dev
else:
    ALLOWED_HOSTS = [] # Should not be empty in production if not DEBUG

# --- Application Definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # For collectstatic
    # 'whitenoise.runserver_nostatic', # Only if using WhiteNoise with runserver during DEBUG=True
    'kvitsapp', # Your app
    'crispy_forms',
    'crispy_bootstrap5',
    # 'storages', # Uncomment if using django-storages for GCS
    # Add other apps here
]

# Conditionally add development-specific apps
if DEBUG:
    INSTALLED_APPS.append('django_browser_reload') # If you use it

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise middleware - place high, after SecurityMiddleware
    # Useful if you collect static files into the container and serve them with WhiteNoise
    # If serving ALL static/media from GCS, you might not need it as extensively.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.append('django_browser_reload.middleware.BrowserReloadMiddleware') # If you use it

ROOT_URLCONF = 'kvits.urls' # Make sure 'kvits' is your project directory name containing urls.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Add a project-level templates directory if you have one
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'kvitsapp.context_processors.year',
                'kvitsapp.context_processors.categories_processor',
                'kvitsapp.context_processors.cart_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'kvits.wsgi.application' # Make sure 'kvits' is your project directory name containing wsgi.py

# --- Database ---
# For Cloud Run with Cloud SQL:
# 1. Enable the Cloud SQL Admin API in your Google Cloud project.
# 2. Create a Cloud SQL instance (PostgreSQL).
# 3. In Cloud Run service settings, under "Connections", add a connection to your Cloud SQL instance.
#    This will make the database available via a Unix socket and usually sets DATABASE_URL.
#    The socket path typically looks like: /cloudsql/YOUR_PROJECT_ID:YOUR_REGION:YOUR_INSTANCE_NAME
# DATABASE_URL format for Cloud SQL socket:
# postgresql://USER:PASSWORD@/DATABASE_NAME?host=/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME
# Or Cloud Run might set it up for you if you use the console to link the SQL instance.

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL: # Provided by Cloud Run (often when connected to Cloud SQL) or set manually
    DATABASES = {'default': dj_database_url.config(conn_max_age=600, ssl_require=os.environ.get('DB_SSL_REQUIRE', 'False') == 'True')}
elif DEBUG: # Fallback for local Docker development if DATABASE_URL is not set
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DATABASE_NAME_LOCAL', 'postgres'),
            'USER': os.environ.get('DATABASE_USER_LOCAL', 'postgres'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD_LOCAL', 'postgres'),
            'HOST': os.environ.get('DATABASE_HOST_LOCAL', 'db'), # Your Docker Compose service name
            'PORT': os.environ.get('DATABASE_PORT_LOCAL', '5432'),
        }
    }
else: # Production environment but DATABASE_URL is not set - this is an error condition
    raise EnvironmentError("DATABASE_URL environment variable not set for production.")


# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = os.environ.get('DJANGO_LANGUAGE_CODE', 'lv') # Default to Latvian
TIME_ZONE = os.environ.get('DJANGO_TIME_ZONE', 'Europe/Riga') # Default to Riga Timezone
USE_I18N = True
USE_TZ = True

# --- Static Files (CSS, JavaScript, Images) ---
# Option 1: Using WhiteNoise (files collected into the container)
#   - Your Dockerfile should run `python manage.py collectstatic`
#   - WhiteNoise middleware is already added.
#   - Set STATIC_ROOT.
# Option 2: Using Google Cloud Storage (recommended for offloading and CDN capabilities)
#   - Add `django-storages[google]` to requirements.txt
#   - Create a GCS bucket.
#   - Configure IAM permissions for the Cloud Run service account to write to the bucket (for collectstatic)
#     and make objects public if they need to be served directly.

STATIC_URL = '/static/' # Standard URL prefix
STATIC_ROOT = BASE_DIR / 'staticfiles' # Directory where collectstatic will gather them

# If using WhiteNoise, its storage backend is good.
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # For Django < 4.2
# For Django 4.2+ STORAGES setting is preferred:
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    # If NOT using GCS for default file storage (media), set a default:
    # "default": {
    #     "BACKEND": "django.core.files.storage.FileSystemStorage", # Or your preferred default
    # },
}

# --- Google Cloud Storage for Static and Media Files (using django-storages) ---
# Ensure 'django-storages[google]' is in your requirements.txt
# This section is an alternative/enhancement to just WhiteNoise for static files
# and essential for user-uploaded media files in a stateless environment like Cloud Run.

# Only configure GCS if the bucket name is set via environment variable
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')
if GCS_BUCKET_NAME:
    # INSTALLED_APPS.append('storages') # Ensure 'storages' is in INSTALLED_APPS if uncommented above

    # Default File Storage (for Media Files)
    # STORAGES['default'] = {'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage'} # Django 4.2+
    # DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage' # Django < 4.2
    # GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID') # Your Google Cloud Project ID
    # GS_BUCKET_NAME = GCS_BUCKET_NAME
    # GS_DEFAULT_ACL = 'publicRead' # Or 'private' then use signed URLs or Cloud CDN
    # MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'
    # MEDIA_ROOT = '' # Media files are not stored locally with GCS

    # Static Files Storage (alternative to WhiteNoise for serving)
    # STORAGES['staticfiles']['BACKEND'] = 'storages.backends.gcloud.GoogleCloudStorage' # Django 4.2+
    # STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage' # Django < 4.2
    # GS_STATIC_BUCKET_NAME = GCS_BUCKET_NAME # Can be the same or a different bucket
    # STATIC_URL = f'https://storage.googleapis.com/{GS_STATIC_BUCKET_NAME}/static/'
    # Note: If using this for static files, your `collectstatic` command during build
    # (e.g., in cloudbuild.yaml) will upload files to GCS.

    pass # Placeholder - uncomment and configure the GCS parts as needed.
         # For a simpler start, you might rely on WhiteNoise for static files first,
         # and then implement GCS for media, then optionally for static.


# --- Media Files (User Uploads) ---
# If not using GCS for media files (DEFAULT_FILE_STORAGE), you'll need a different strategy
# for Cloud Run as its filesystem is ephemeral. GCS is highly recommended.
# If using GCS, MEDIA_URL and MEDIA_ROOT are set in the GCS section above.
# If you *must* use local storage temporarily (e.g., very small, non-critical media, or testing):
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'mediafiles' # This will be ephemeral on Cloud Run

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Authentication ---
LOGIN_REDIRECT_URL = 'kvitsapp:profile' #
LOGIN_URL = 'kvitsapp:login' #
# Consider settings like:
# LOGOUT_REDIRECT_URL = '/'

# --- Crispy Forms ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5" #
CRISPY_TEMPLATE_PACK = "bootstrap5" #

# --- Email Backend ---
# For production, use a transactional email service like SendGrid, Mailgun, etc.
# Configure using environment variables.
# For Cloud Run, avoid using django.core.mail.backends.smtp.EmailBackend directly
# if your provider requires IP whitelisting, as Cloud Run IPs are dynamic.
# Use their official client libraries or an HTTP API if possible, or an SMTP
# service designed for cloud environments.
EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend') #
if EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER') # Your email username
    EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD') # Your email password (use Secret Manager!)
    DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', 'webmaster@yourdomain.com')

COMPANY_ORDER_EMAIL = os.environ.get('COMPANY_ORDER_EMAIL', 'company-orders@example.com') #


# --- Security Settings (Important for Production!) ---
# Most of these should be True or set in production (when DEBUG=False).
# Cloud Run typically runs behind a Google managed SSL endpoint.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # Essential if Cloud Run is behind a load balancer/proxy handling HTTPS
SECURE_SSL_REDIRECT = not DEBUG and os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = not DEBUG and os.environ.get('DJANGO_SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = not DEBUG and os.environ.get('DJANGO_CSRF_COOKIE_SECURE', 'True') == 'True'

# CSRF_TRUSTED_ORIGINS should include your Cloud Run service URL and custom domain.
# e.g., https://your-service-name.a.run.app, https://www.yourcustomdomain.com
CSRF_TRUSTED_ORIGINS_STRING = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS')
if CSRF_TRUSTED_ORIGINS_STRING:
    CSRF_TRUSTED_ORIGINS = [url.strip() for url in CSRF_TRUSTED_ORIGINS_STRING.split(',')]
else:
    CSRF_TRUSTED_ORIGINS = []

# HSTS Settings (consider your needs and test carefully)
# SECURE_HSTS_SECONDS = not DEBUG and int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', 0)) # e.g., 2592000 (30 days)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG and os.environ.get('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
# SECURE_HSTS_PRELOAD = not DEBUG and os.environ.get('DJANGO_SECURE_HSTS_PRELOAD', 'True') == 'True'

# --- Logging ---
# Logs to stdout/stderr are automatically collected by Cloud Logging on Cloud Run.
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
            'formatter': 'simple', # Or 'verbose'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('DJANGO_LOG_LEVEL_ROOT', 'INFO'), # Default to INFO
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL_DJANGO', 'INFO'), # Default to INFO
            'propagate': False,
        },
        # Add other loggers as needed
        # 'yourapp': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG', # Example
        #     'propagate': False,
        # },
    },
}

# --- Django App Specific Settings ---
# (Add any other custom settings your app 'kvitsapp' might need)