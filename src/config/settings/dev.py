import os

from dotenv import load_dotenv

from config.settings.base import *  # NOQA

load_dotenv()


SECRET_KEY = "django-insecure-m2@0y4r0z6mz!sh=9f=-j*k5v_swbo*z^l3g9efhn9pv$9sv(j"

DEBUG = True

ALLOWED_HOSTS = []  # NOQA
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

INSTALLED_APPS += [
    "django_extensions",  # NOQA
    "debug_toolbar",  # NOQA
]

if os.getenv("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "0.0.0.0",
            "PORT": 5432,
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "Pavlov_fp_db",
            "USER": "fp_user",
            "PASSWORD": "admin",
            "HOST": "localhost",
            "PORT": "5432",
        },
        # "default": {
        #     "ENGINE": "django.db.backends.postgresql",
        #     "NAME": os.getenv("POSTGRES_DB"),
        #     "USER": os.getenv("POSTGRES_USER"),
        #     "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        #     "HOST": os.getenv("POSTGRES_HOST"),
        #     "PORT": os.getenv("POSTGRES_PORT"),
        # },
        # "default": {
        #     "ENGINE": "djongo",
        #     "NAME": os.getenv("MONGO_DB_NAME"),
        #     "ENFORCE_SCHEMA": False,
        #     "CLIENT": {
        #         "host": os.getenv("MONGO_HOST"),
        #         "port": int(os.getenv("MONGO_PORT", 27017)),
        #         "username": os.getenv("MONGO_INITDB_ROOT_USERNAME"),
        #         "password": os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
        #         "authSource": "admin",
        #     },
        # },
        # "default": {
        #     "ENGINE": "django.db.backends.sqlite3",
        #     "NAME": BASE_DIR / "db.sqlite3",  # NOQA
        # },
    }

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # NOQA
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
