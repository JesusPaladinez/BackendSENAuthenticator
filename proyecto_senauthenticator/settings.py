"""
Django settings for proyecto_senauthenticator project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*dhg)w2)u_k6d)(5n)ihfqen*wp#jy6f=e8%2(z!=nipbwrr)^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Permite alojar el proyecto en todos los dominios
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'coreapi', # módulo para documentar el código    
    'whitenoise.runserver_nostatic', # Módulo para subir archivos estaticos 
    'app_senauthenticator', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #  Este middleware extrae el token jwt-access de las cookies en cada solicitud y lo coloca en la cabecera de autorización para que Django
    'app_senauthenticator.middleware.JWTAuthFromCookieMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'proyecto_senauthenticator.urls'

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

WSGI_APPLICATION = 'proyecto_senauthenticator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}
    
# DATABASES ["default"] = dj_database_url.parse('postgresql://senauthenticator_db_9c5c_user:aGE65xoUeYsYciQ8Qrw9nfAN08Ybhyip@dpg-crovmqdds78s73d2h69g-a.oregon-postgres.render.com/senauthenticator_db_9c5c')


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

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# usuario del app
AUTH_USER_MODEL = 'app_senauthenticator.Usuario'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Permite todas las solicitudes de todos los dominios(esto puede ser inseguro para producción)
CORS_ALLOW_ALL_ORIGINS = True


# autoriza rutas para poderse ejecutar (en este caso la de Next.js y la de Flutter)

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # URL del frontend en desarrollo
    'http://localhost:5173',
    
    'https://backendsenauthenticator.onrender.com',  # URL de producción
    'https://backprojecto.onrender.com',
    'https://senauthenticator.onrender.com',
]

# Configuración de esquema para que django rest framework y coreapi puedan documentar el código
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
} 

# Configurar las cookies de JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  #timedelta(minutes=5) Ajusta el tiempo según tu necesidad
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_COOKIE': 'jwt-access',  # Nombre de la cookie del token de acceso
    'AUTH_COOKIE_REFRESH': 'jwt-refresh',  # Nombre de la cookie del token de refresh
    'AUTH_COOKIE_SECURE': True,  # Cambiar a True en producción para HTTPS
    'AUTH_COOKIE_HTTP_ONLY': True, # Cuando httponly está configurado como true, significa que la cookie solo puede ser accedida por el navegador y no por scripts del lado del cliente (como JavaScript).
    'AUTH_COOKIE_SAMESITE': 'None', # para usar AUTH_COOKIE_SAMESITE:'none', AUTH_COOKIE_SECURE debe estar en True en producción
   
}


CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:5173/',  # URL del frontend
]


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER ='moto.emacasta12@gmail.com'
EMAIL_HOST_PASSWORD ='aytyfmpcczisphrd'