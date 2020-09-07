from .settings import *

DEBUG = True


DATABASES['default']['NAME'] = 'tekit'
DATABASES['default']['USER'] = 'postgres'
DATABASES['default']['PASSWORD'] = 'paulbit10'
DATABASES['default']['HOST'] = 'localhost'
DATABASES['default']['PORT'] = 5432


# DATABASES = {
#     'default': {
#         'NAME': 'tekit',
#         'USER': 'postgres',
#         'PASSWORD': 'paulbit10',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
