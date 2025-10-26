import os
from pathlib import Path

# Base
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = "django-insecure-!#8wnj$w-yh_o=d8$y67-)w6z$pid*1fjbw=eg5b-*o&u^)$u+"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "[::1]"]

# Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "App",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "website.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # <project>/templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "App.context_processors.site_menus",
            ],
        },
    },
]

WSGI_APPLICATION = "website.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# I18N / TZ
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Bangkok"  # ปรับให้ตรงเวลาไทย (เปลี่ยนได้ตามต้องการ)
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # ไฟล์ static ที่แก้เองตอน dev
STATIC_ROOT = BASE_DIR / "staticfiles"  # โฟลเดอร์ปลายทาง collectstatic (prod)

# Media files (สำหรับอัปโหลดรูปจาก admin)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default PK
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
