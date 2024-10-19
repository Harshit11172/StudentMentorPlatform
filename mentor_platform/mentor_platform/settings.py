"""
Django settings for mentor_platform project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m95y7l1pezvlo0ia8+j=)r1a!w7@8a0j5xv5yjr$*gogw%$8st'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'daphne' , 

    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'users', # apps installed from now below
    'mentorship',
    'chat',
    'voice_video',
    'payments',
    'education',

    'channels', #real-time chat
    'channels_redis',

    #email verification
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'corsheaders',
]

AUTH_USER_MODEL = 'users.CustomUser'

ASGI_APPLICATION = 'mentor_platform.asgi.application'


AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
)


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'allauth.account.middleware.AccountMiddleware',  # Add this line
]


ROOT_URLCONF = 'mentor_platform.urls'

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

WSGI_APPLICATION = 'mentor_platform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


########################## AUTH FROM CHATGPT

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ],
    
}


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # Adjust if your Redis is hosted differently
        },
    },
}

#email-verification

SITE_ID = 1

# Email backend settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Use Gmail's SMTP server
EMAIL_PORT = 587  # Standard port for TLS
EMAIL_USE_TLS = True  # Enable TLS
EMAIL_HOST_USER = 'harshitkh9@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'jngauxbvndxcgcyi'  # Your email password
DEFAULT_FROM_EMAIL = 'harshitkh9@gmail.com'  # Email address used in "From" field


ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # To require email verification
ACCOUNT_EMAIL_REQUIRED = True  # Require email for signup
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Allow login via username or email
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'  # If you have a custom user model
ACCOUNT_USERNAME_REQUIRED = True  # Require username



AGORA_APP_ID = '2128c59cf62641a5b09b7bff062ed10c'
AGORA_APP_CERTIFICATE = 'aeb6d3c85fa64265bd736659606530b2'  # If using token-based authentication


# settings.py
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Optional: Ensures sessions expire when the browser is closed
SESSION_COOKIE_AGE = 1209600  # Set session duration (2 weeks)


CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
]