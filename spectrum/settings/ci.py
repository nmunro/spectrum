from .base import *

DATABASES = {
    "default":  {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres_test",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,  # default postgres port
    }
}
