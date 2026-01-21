from pathlib import Path
import os
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

# ---------------------------------------
# BASE_DIR et .env
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

if os.path.exists(BASE_DIR / ".env"):
    load_dotenv(BASE_DIR / ".env")

# ---------------------------------------
# Sécurité
# ---------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key")
DEBUG = False  # Toujours False en prod

# Remplace par ton domaine Render
ALLOWED_HOSTS = ["midai.onrender.com", "127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = ["https://midai.onrender.com"]

# ---------------------------------------
# Applications installées
# ---------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

# ---------------------------------------
# Middleware
# ---------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise pour servir les statics
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MidAI.urls'

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

WSGI_APPLICATION = 'MidAI.wsgi.application'

# ---------------------------------------
# Base de données
# ---------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------
# Password validation
# ---------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------
# Internationalisation
# ---------------------------------------
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ("fr", _("French")),
    ("en", _("English")),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

# ---------------------------------------
# Static files
# ---------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'app/static']  # dossiers sources
STATIC_ROOT = BASE_DIR / "staticfiles"        # dossier collecté pour la prod

# WhiteNoise : compression et hash pour prod
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ---------------------------------------
# Autres settings
# ---------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
CONTACT_EMAIL = "michaellapeyrere.ml@gmail.com"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"contact": {"handlers": ["console"], "level": "WARNING"}},
}