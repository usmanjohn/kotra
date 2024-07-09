import os
from pathlib import Path
import django_heroku
import dj_database_url
import environ
from storages.backends.s3boto3 import S3Boto3Storage

from kotrain.storage_backends import StaticStorage, MediaStorage


# Initialize environment variables
env = environ.Env()
# Read .env file
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'topics',
    'users',
    'book',
    'podcasts',
    'tutor',
    'job',
    'exam',

    'storages',
    'crispy_forms',
    'crispy_bootstrap4',
    'taggit',
    'django_ckeditor_5',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kotrain.urls'

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
                'topics.context_processors.logo_url',
            ],
        },
    },
]

WSGI_APPLICATION = 'kotrain.wsgi.application'

# Database configuration
DATABASES = {
    'default': dj_database_url.config(conn_max_age=0, ssl_require=False)
}
DATABASES['default'] = DATABASES['default']


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Ensure emails are sent from your actual email
SERVER_EMAIL = EMAIL_HOST_USER 

# Static files (CSS, JavaScript, Images)
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
AWS_LOCATION = env('AWS_LOCATION')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'



STATICFILES_STORAGE = 'kotrain.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'kotrain.storage_backends.MediaStorage'

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Activate Django-Heroku without database settings
django_heroku.settings(locals(), databases=False, staticfiles=False)

# Date input formats
DATE_INPUT_FORMATS = ['%d/%m/%Y']

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# Miscellaneous settings
DATA_UPLOAD_MAX_NUMBER_FIELDS = 11240
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# CKEditor settings
CKEDITOR_BASEPATH = "/topics/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "media/"

customColorPalette = [
    {'color': 'hsl(4, 90%, 58%)', 'label': 'Red'},
    {'color': 'hsl(340, 82%, 52%)', 'label': 'Pink'},
    {'color': 'hsl(291, 64%, 42%)', 'label': 'Purple'},
    {'color': 'hsl(262, 52%, 47%)', 'label': 'Deep Purple'},
    {'color': 'hsl(231, 48%, 48%)', 'label': 'Indigo'},
    {'color': 'hsl(207, 90%, 54%)', 'label': 'Blue'},
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', 'imageUpload'],
        'width': '100%',
    },
    'extends': {
        'width': '100%',
        'blockToolbar': ['paragraph', 'heading1', 'heading2', 'heading3', '|', 'bulletedList', 'numberedList', '|', 'blockQuote'],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough', 'code', 'subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage', 'bulletedList', 'numberedList', 'todoList', '|', 'blockQuote', 'imageUpload', '|', 'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat', 'insertTable'],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft', 'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side'],
            'styles': ['full', 'side', 'alignLeft', 'alignRight', 'alignCenter'],
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties'],
            'tableProperties': {'borderColors': customColorPalette, 'backgroundColors': customColorPalette},
            'tableCellProperties': {'borderColors': customColorPalette, 'backgroundColors': customColorPalette},
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'},
            ],
        },
        'width': 'auto',
    },
    'list': {
        'properties': {'styles': 'true', 'startIndex': 'true', 'reversed': 'true'},
        'width': 'auto',
    },
}

# Auth password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# Debugging prints
#print("EMAIL_HOST:", env('EMAIL_HOST'))
#print("EMAIL_PORT:", env('EMAIL_PORT'))
#print("EMAIL_USE_TLS:", env('EMAIL_USE_TLS'))
#print("EMAIL_HOST_USER:", env('EMAIL_HOST_USER'))
#print("EMAIL_HOST_PASSWORD:", env('EMAIL_HOST_PASSWORD'))
#print("DATABASE_URL:", env('DATABASE_URL'))
#print("SECRET_KEY:", env('SECRET_KEY'))
#print("DEBUG:", env('DEBUG'))
# 