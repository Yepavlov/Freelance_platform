import os

from config.settings.base import *  # NOQA

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # NOQA
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
