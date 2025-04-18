from .base import *
from .prod import *


DEBUG = True


ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INTERNAL_IPS = ["127.0.0.1"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


