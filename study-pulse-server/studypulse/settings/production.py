import os
from .base import *
import dj_database_url


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         "USER": os.environ.get("SQL_USER"),
#         "PASSWORD": os.environ.get("SQL_PASSWORD"),
#         'NAME': os.environ.get('DATABASE_NAME'),
#         'HOST': os.environ.get('DATABASE_HOST'),
#         'PORT': int(os.environ.get('DATABASE_PORT')),
#     }
# }
DATABASES = {}
# postgresql://root:uWB0oEy90tzTqPyt36CapiLp5TaTNkDG@dpg-cptveo08fa8c738rlh90-a.oregon-postgres.render.com/studypulse
DATABASES["default"] = dj_database_url.parse(os.environ.get('DATABASE_URL'))

ROOT_URLCONF = 'studypulse.urls'

STATIC_URL = "static/"


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
