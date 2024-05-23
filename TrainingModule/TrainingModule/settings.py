"""
Django settings for TrainingModule project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import _osx_support
import os
import json
from django.core.exceptions import ImproperlyConfigured


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yfv2si1i$+%v)u$vo7gv$3^@ap1#z!hm5+jhq$i9x^ro5%_zvd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
env = os.environ['ENV']
conf_name = 'config-'+ env+'.json'
config_path = os.path.join (os.path.dirname(__file__),conf_name  )
config = open(config_path)
data = json.load(config)

DIRECTORY_TO_SCAN = data ["DIRECTORY_TO_SCAN"]
PROCESSED_FILES = data ["PROCESSED_FILES"]
ERROR_FILES = data ["ERROR_FILES"]
PINECONE_API_KEY = data ["PINECONE_API_KEY"]
PINECONE_INDEX = data ["PINECONE_INDEX"]
OPENAI_API_KEY = data ["OPENAI_API_KEY"]
PDF_MODEL = data ["PDF_MODEL"]
TXT_MODEL = data ["TXT_MODEL"]
OPEN_AI_PDF_EMBEDDING_MODEL = data ["OPEN_AI_PDF_EMBEDDING_MODEL"]
OPEN_AI_PDF_EMBEDDING_CTX_LENGTH = data ["OPEN_AI_PDF_EMBEDDING_CTX_LENGTH"]
OPEN_AI_PDF_EMBEDDING_ENCODING = data ["OPEN_AI_PDF_EMBEDDING_ENCODING"]
EMBEDDING_CHUNK_SIZE = data ["EMBEDDING_CHUNK_SIZE"]
NUM_RELATED_QUESTIONS= data ["NUM_RELATED_QUESTIONS"]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Training',
    'rest_framework'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '127.0.0.1:11211',  # Adjust as necessary
    }
}

ROOT_URLCONF = 'TrainingModule.urls'

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

WSGI_APPLICATION = 'TrainingModule.wsgi.application'

#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(funcName)s: %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django_info.log',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {  # This is the root logger, which catches logs from any logger.
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}














