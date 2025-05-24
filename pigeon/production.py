import os

from pigeon.settings import *

print("Using production settings")

ALLOWED_HOSTS = [
    "*",
]

# DATABASES = {"default": dj_database_url.config()}

DATABASES = {
    # 'default': {
    # 	'ENGINE': 'django.db.backends.sqlite3',
    # 	'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
    }
}
print(DATABASES)

STATIC_ROOT = os.getenv("STATIC_ROOT", "/data/static")
