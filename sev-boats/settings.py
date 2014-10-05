# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join

BASE_DIR = os.path.dirname(__file__)

MESSAGES_DIR = join(BASE_DIR, 'messages')

try:
    from settings_local import *  # noqa
except ImportError:
    pass
