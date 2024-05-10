from config.settings.base import *  # NOQA

SECRET_KEY = "django-insecure-m2@0y4r0z6mz!sh=9f=-j*k5v_swbo*z^l3g9efhn9pv$9sv(j"

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "static/"
