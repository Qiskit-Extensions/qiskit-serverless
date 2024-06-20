"""
Django settings for gateway project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import os.path
import sys
from datetime import timedelta
from pathlib import Path
from utils import sanitize_file_path

RELEASE_VERSION = os.environ.get("VERSION", "UNKNOWN")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-&)i3b5aue*#-i6k9i-03qm(d!0h&662lbhj12on_*gimn3x8p7",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", 1))

# SECURITY WARNING: don't run with debug turned on in production!
LOG_LEVEL = "DEBUG" if int(os.environ.get("DEBUG", 1)) else "WARNING"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# allow connections from any kubernetes pod within the cluster
# k8s pods are given an IP on the private 10. network, and 10.0.0.0/8
# includes all 10. IPs.
ALLOWED_CIDR_NETS = ["10.0.0.0/8"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_prometheus",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "allauth",
    "allauth.socialaccount",
    "api",
    "psycopg2",
    "drf_yasg",
]

MIDDLEWARE = [
    "csp.middleware.CSPMiddleware",
    "allow_cidr.middleware.AllowCIDRMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", "/tmp/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(asctime)s %(filename)s:%(lineno)s : %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "commands": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "gateway": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "gateway.serializers": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "gateway.authentication": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME", "serverlessdb"),
        "USER": os.environ.get("DATABASE_USER", "serverlessuser"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "serverlesspassword"),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
    },
    "test": {
        "ENGINE": "django_prometheus.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

if "test" in sys.argv:
    DATABASES["default"] = DATABASES["test"]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(sanitize_file_path(str(BASE_DIR)), "static")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(sanitize_file_path(str(BASE_DIR)), "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============
# AUTH SETTINGS
# =============
SETTINGS_AUTH_MECHANISM = os.environ.get("SETTINGS_AUTH_MECHANISM", "default")
SETTINGS_DEFAULT_AUTH_CLASSES = [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
    "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
]
ALL_AUTH_CLASSES_CONFIGURATION = {
    "default": SETTINGS_DEFAULT_AUTH_CLASSES,
    "custom_token": [
        "api.authentication.CustomTokenBackend",
    ],
    "mock_token": [
        "api.authentication.MockAuthBackend",
    ],
}
DJR_DEFAULT_AUTHENTICATION_CLASSES = ALL_AUTH_CLASSES_CONFIGURATION.get(
    SETTINGS_AUTH_MECHANISM, SETTINGS_DEFAULT_AUTH_CLASSES
)
# mock token value
SETTINGS_AUTH_MOCK_TOKEN = os.environ.get("SETTINGS_AUTH_MOCK_TOKEN", "awesome_token")
# =============

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": DJR_DEFAULT_AUTHENTICATION_CLASSES,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

REST_AUTH = {
    "USE_JWT": True,
    # 'JWT_AUTH_COOKIE': 'gateway-app-auth',
    # 'JWT_AUTH_REFRESH_COOKIE': 'gateway-refresh-token',
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        },
    },
    "USE_SESSION_AUTH": False,
}

SITE_ID = 1
SITE_HOST = os.environ.get("SITE_HOST", "http://localhost:8000")

# Provider specific settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=20),
}

MEDIA_ROOT = os.path.join(sanitize_file_path(str(BASE_DIR)), "media")
MEDIA_URL = "/media/"

# custom token auth
SETTINGS_TOKEN_AUTH_URL = os.environ.get("SETTINGS_TOKEN_AUTH_URL", None)
SETTINGS_TOKEN_AUTH_USER_FIELD = os.environ.get(
    "SETTINGS_TOKEN_AUTH_USER_FIELD", "userId"
)
SETTINGS_TOKEN_AUTH_TOKEN_FIELD = os.environ.get(
    "SETTINGS_TOKEN_AUTH_TOKEN_FIELD", "apiToken"
)
SETTINGS_TOKEN_AUTH_VERIFICATION_URL = os.environ.get(
    "SETTINGS_TOKEN_AUTH_VERIFICATION_URL", None
)
# verification fields to check when returned from auth api
# Example of checking multiple fields:
#    For following verification data
#    {
#       "is_valid": true,
#       "some": {
#         "nested": {
#           "field": true
#         },
#         "other": "bla"
#       }
#    }
#   setting string will be:
#    "SETTINGS_TOKEN_AUTH_VERIFICATION_FIELD", "is_valid;some,nested,field"
SETTINGS_TOKEN_AUTH_VERIFICATION_FIELD = os.environ.get(
    "SETTINGS_TOKEN_AUTH_VERIFICATION_FIELD", None
)

# resources limitations
LIMITS_JOBS_PER_USER = int(os.environ.get("LIMITS_JOBS_PER_USER", "2"))
LIMITS_MAX_CLUSTERS = int(os.environ.get("LIMITS_MAX_CLUSTERS", "6"))

# ray cluster management
RAY_KUBERAY_NAMESPACE = os.environ.get("RAY_KUBERAY_NAMESPACE", "qiskit-serverless")
RAY_CLUSTER_MODE = {
    "local": int(os.environ.get("RAY_CLUSTER_MODE_LOCAL", 0)),
    "ray_local_host": os.environ.get(
        "RAY_CLUSTER_MODE_LOCAL_HOST", "http://localhost:8265"
    ),
}
RAY_NODE_IMAGE = os.environ.get(
    "RAY_NODE_IMAGE", "icr.io/quantum-public/qiskit-serverless/ray-node:0.12.0-py310"
)
RAY_NODE_IMAGES_MAP = {
    "default": RAY_NODE_IMAGE,
    "py39": os.environ.get("RAY_NODE_IMAGE_PY39", RAY_NODE_IMAGE),
    "py310": os.environ.get("RAY_NODE_IMAGE_PY310", RAY_NODE_IMAGE),
}
RAY_CLUSTER_WORKER_REPLICAS = int(os.environ.get("RAY_CLUSTER_WORKER_REPLICAS", "1"))
RAY_CLUSTER_WORKER_REPLICAS_MAX = int(
    os.environ.get("RAY_CLUSTER_WORKER_REPLICAS_MAX", "5")
)
RAY_CLUSTER_WORKER_MIN_REPLICAS = int(
    os.environ.get("RAY_CLUSTER_WORKER_MIN_REPLICAS", "1")
)
RAY_CLUSTER_WORKER_MIN_REPLICAS_MAX = int(
    os.environ.get("RAY_CLUSTER_WORKER_MIN_REPLICAS_MAX", "2")
)
RAY_CLUSTER_WORKER_MAX_REPLICAS = int(
    os.environ.get("RAY_CLUSTER_WORKER_MAX_REPLICAS", "4")
)
RAY_CLUSTER_WORKER_MAX_REPLICAS_MAX = int(
    os.environ.get("RAY_CLUSTER_WORKER_MAX_REPLICAS_MAX", "10")
)
RAY_CLUSTER_WORKER_AUTO_SCALING = bool(
    os.environ.get("RAY_CLUSTER_WORKER_AUTO_SCALING", False)
)
RAY_CLUSTER_MAX_READINESS_TIME = int(
    os.environ.get("RAY_CLUSTER_MAX_READINESS_TIME", "120")
)

RAY_SETUP_MAX_RETRIES = int(os.environ.get("RAY_SETUP_MAX_RETRIES", 30))

RAY_CLUSTER_NO_DELETE_ON_COMPLETE = bool(
    os.environ.get("RAY_CLUSTER_NO_DELETE_ON_COMPLETE", False)
)

PROGRAM_TIMEOUT = int(os.environ.get("PROGRAM_TIMEOUT", "14"))

# qiskit runtime
QISKIT_IBM_CHANNEL = os.environ.get("QISKIT_IBM_CHANNEL", "ibm_quantum")
QISKIT_IBM_URL = os.environ.get(
    "QISKIT_IBM_URL", "https://auth.quantum-computing.ibm.com/api"
)

# quantum api
IQP_QCON_API_BASE_URL = os.environ.get("IQP_QCON_API_BASE_URL", None)

# Content Security Policy
CSP_DEFAULT_SRC = "'none'"
CSP_SCRIPT_SRC = "'none'"
CSP_FRAME_ANCESTORS = "'self'"
CSP_OBJECT_SRC = "'self'"
CSP_IMG_SRC = ("'self'", "data:", "https://cdn.redoc.ly")
CSP_STYLE_SRC_ELEM = ("'self'", "'unsafe-inline'")
CSP_SCRIPT_SRC_ELEM = "'self'"
CSP_CONNECT_SRC = "'self'"
CSP_WORKER_SRC = ("'self'", "blob:")

# Custom image for programs settings
CUSTOM_IMAGE_PACKAGE_NAME = os.environ.get("CUSTOM_IMAGE_PACKAGE_NAME", "runner")
CUSTOM_IMAGE_PACKAGE_PATH = os.environ.get("CUSTOM_IMAGE_PACKAGE_PATH", "/runner")
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_AGE = 3600
