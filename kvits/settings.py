import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Using the default insecure key is acceptable ONLY for local development.
# DO NOT use this key in production (Render).
SECRET_KEY = 'django-insecure-beso@#zvg(2szht%&80yddpqe^(7n(&d2b)6zmkrtrro1=n60b'

# SECURITY WARNING: don't run with debug turned on in production!
# Hardcoding DEBUG = True for local development.
DEBUG = True

# Allow hosts commonly used for local Docker development
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'whitenoise.runserver_nostatic', # Optional: include if you use runserver --nostatic
    'django.contrib.staticfiles',
    'kvitsapp',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_browser_reload', # Okay for local development
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Keep WhiteNoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware', # Okay for local development
]

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


# Database
# Reads individual connection details directly from environment variables
# set in docker-compose.yml for the 'web' service.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'postgres'), # Default 'postgres' if not set
        'USER': os.environ.get('DATABASE_USER', 'postgres'), # Default 'postgres' if not set
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'postgres'), # Default 'postgres' if not set
        'HOST': os.environ.get('DATABASE_HOST', 'db'), # Default 'db' (service name) if not set
        'PORT': os.environ.get('DATABASE_PORT', '5432'), # Default '5432' if not set
    }
    # Removed the specific TEST database config for simplicity
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# STATIC_ROOT is where collectstatic gathers files (needed for WhiteNoise in production)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS is where Django looks for static files in development
STATICFILES_DIRS = [
    BASE_DIR / "kvitsapp/static",
]

# STORAGES setting for WhiteNoise is removed as it's primarily for production optimization
# and DEBUG=True handles static files differently.

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'kvitsapp:profile'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email backend for local development (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
COMPANY_ORDER_EMAIL = 'local-dev-email@example.com' # Use a placeholder for local

# Production security settings are removed or implicitly False due to DEBUG=True
# CSRF_TRUSTED_ORIGINS = []
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False

# Basic logging for development
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
        'level': 'INFO', # Or DEBUG for more verbosity
    },
}

