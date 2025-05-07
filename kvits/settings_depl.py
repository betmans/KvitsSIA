import os
from pathlib import Path
import dj_database_url # Add this

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY') # Load from environment

# DEBUG should be False in production.
# Set DJANGO_DEBUG=True in your .env for local dev if you use this.
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Load allowed hosts from environment variable, space separated
# e.g., your-app.onrender.com www.yourdomain.com
ALLOWED_HOSTS_STRING = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1')
ALLOWED_HOSTS = ALLOWED_HOSTS_STRING.split(' ') if ALLOWED_HOSTS_STRING else []
if DEBUG and not ALLOWED_HOSTS: # Add default allowed hosts for local dev if DEBUG is True and no hosts are set
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '[::1]'])


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # If using whitenoise for dev too (runserver --nostatic)
    'django.contrib.staticfiles',
    'kvitsapp',
    'crispy_forms',
    'crispy_bootstrap5',
    # 'django_browser_reload', # Consider removing for production or wrap in if DEBUG
]
# Conditionally add development apps
if DEBUG:
    INSTALLED_APPS.append('django_browser_reload')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    MIDDLEWARE.append('django_browser_reload.middleware.BrowserReloadMiddleware')


ROOT_URLCONF = 'kvits.urls'

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
                'kvitsapp.context_processors.year',
                'kvitsapp.context_processors.categories_processor',
                'kvitsapp.context_processors.cart_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'kvits.wsgi.application'

# Database configuration using dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}"), # Fallback to SQLite for local dev if DATABASE_URL not set
        conn_max_age=600,
        # For Render PostgreSQL, SSL might be required.
        # dj_database_url usually handles the ?sslmode=require in the URL.
        # If explicit control is needed:
        # ssl_require=os.environ.get('DB_SSL_REQUIRE', 'False') == 'True'
    )
}

# If you need a separate test database configuration:
import sys
if 'test' in sys.argv or os.environ.get('CI'): # Also check for CI environment variable if you run tests in CI
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_TEST_NAME', 'test_kvits_postgres'),
        'USER': os.environ.get('DATABASE_TEST_USER', 'postgres'),
        'PASSWORD': os.environ.get('DATABASE_TEST_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DATABASE_TEST_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_TEST_PORT', '5432'),
    }
    # Or use an environment variable for the test database URL
    # TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')
    # if TEST_DATABASE_URL:
    #    DATABASES['default'] = dj_database_url.parse(TEST_DATABASE_URL)


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "kvitsapp/static",
]

# For Django 4.2+
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": { # Keep or set your default file storage if needed for media files etc.
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}
# For Django < 4.2, use this instead of the STORAGES dict for staticfiles:
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'kvitsapp:profile'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email backend: For production, you'll want a real email service (SendGrid, Mailgun, etc.)
# For now, console is fine, or set up SMTP via environment variables.
EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
# Add other email settings (EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
# if you switch to an SMTP backend, and load them from environment variables.

COMPANY_ORDER_EMAIL = os.environ.get('COMPANY_ORDER_EMAIL', 'oskarsplotnieks@gmail.com')

# CSRF_TRUSTED_ORIGINS: If your app is behind HTTPS, you'll need to set this
# to include your domain to allow POST requests.
CSRF_TRUSTED_ORIGINS_STRING = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS')
if CSRF_TRUSTED_ORIGINS_STRING:
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in CSRF_TRUSTED_ORIGINS_STRING.split(' ')]
else:
    CSRF_TRUSTED_ORIGINS = []

# Security settings for production:
# These should ideally be True in production, but require your site to be served over HTTPS.
# Render provides free TLS certificates and handles HTTPS termination.
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = os.environ.get('DJANGO_SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('DJANGO_CSRF_COOKIE_SECURE', 'True') == 'True'

# Optional but recommended security headers (if not handled by a reverse proxy)
# SECURE_HSTS_SECONDS = 31536000 # 1 year; set to 0 or a small value initially for testing
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_BROWSER_XSS_FILTER = True # X-XSS-Protection is deprecated in modern browsers
# SECURE_CONTENT_TYPE_NOSNIFF = True

# Logging: Configure logging for production to see errors.
# Example:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO', # Set to WARNING or ERROR for less verbosity in production
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'), # Configurable log level
            'propagate': False,
        },
    },
}