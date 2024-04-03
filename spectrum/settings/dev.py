from .base import *

DATABASES = {
    "default":  {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}

SENDGRID_SANDBOX_MODE_IN_DEBUG = config("SENDGRID_SANDBOX_MODE_IN_DEBUG", cast=bool)
