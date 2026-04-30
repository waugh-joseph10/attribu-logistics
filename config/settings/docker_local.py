from .base import *

DEBUG = True

DATABASES['default']['NAME'] = 'attribu_local'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
