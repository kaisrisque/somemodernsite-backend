from .settings import *

DEBUG = False

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static") 

WEBPACK_LOADER = {
    'DEFAULT': {
            'BUNDLE_DIR_NAME': 'bundles/',
            'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.prod.json'),
        }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis-backend.nt9c3i.0001.cac1.cache.amazonaws.com:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis-backend.nt9c3i.0001.cac1.cache.amazonaws.com', 6379)],
        },
    },
}

SECURE_CONTENT_TYPE_NOSNIFF=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS='DENY'

