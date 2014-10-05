import os
import sys
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# add dir to path for use import
path = join(BASE_DIR, 'sevboats')
if path not in sys.path:
    sys.path.insert(0, path)

MESSAGES_DIR = join(BASE_DIR, 'sevboats', 'messages')

# Twitter authentication information
# must be redefined in settings local
TWITTER_OAUTH_INFO = dict(
    app_key='Consumer Key (API Key)',
    app_secret='Consumer Secret (API Secret)',
    oauth_token='Access Token',
    oauth_token_secret='Access Token Secret', )

try:
    from settings_local import *  # noqa
except ImportError:
    pass
if os.environ['travis']:
    try:
        from settings_travis import *  # noqa
    except ImportError:
        pass
