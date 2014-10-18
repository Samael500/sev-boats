import os
import sys
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# add dir to path for use import
path = join(BASE_DIR, 'sevboats')
if path not in sys.path:
    sys.path.insert(0, path)

MESSAGES_DIR = join(BASE_DIR, 'sevboats', 'messages')
DATA_DIR = join(BASE_DIR, 'sevboats', 'data')

# Twitter authentication information
# must be redefined in settings local
TWITTER_OAUTH_INFO = dict(
    app_key='Consumer Key (API Key)',
    app_secret='Consumer Secret (API Secret)',
    oauth_token='Access Token',
    oauth_token_secret='Access Token Secret', )

# if is debug
DEBUG = False

# peryodical get ship data in hours
PERIOD = 1

# time delta of UTC
UTC_OFFSET = 4

try:
    from settings_local import *  # noqa
except ImportError:
    pass

if 'travis' in os.environ:
    try:
        from settings_travis import *  # noqa
    except ImportError:
        pass
