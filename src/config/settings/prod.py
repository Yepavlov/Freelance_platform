import os

from config.settings.base import *  # NOQA

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}

STATIC_ROOT = BASE_DIR / "static/"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media/"
MEDIA_URL = "/media/"
print(MEDIA_ROOT)
print(STATIC_ROOT)
