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
        'PASSWORD': 'production'
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
