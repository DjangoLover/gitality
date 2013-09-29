DEBUG = False

ADMINS = (
    ('Artem Kostiuk', 'postatum@gmail.com'),
    ('Dima Moroz', 'me@dimamoroz.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django_postgrespool',
        'NAME': 'gitality',
        'USER': 'production',
        'PASSWORD': 'production',
        'HOST': 'localhost'
    }
}

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2'
}

ALLOWED_HOSTS = ['www.gitality.com', 'gitality.com']

SECRET_KEY = 'topsecret'

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CACHE_MIDDLEWARE_SECONDS = 60 * 5  # 5 minutes
