import os
from pathlib import Path
from .settings import *

DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'), #修正
    }
}
