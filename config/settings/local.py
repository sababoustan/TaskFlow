from .base import *

DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
