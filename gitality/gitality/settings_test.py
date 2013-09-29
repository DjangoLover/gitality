from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'gitality.db'
    }
}

SOUTH_DATABASE_ADAPTERS = {}

INSTALLED_APPS = INSTALLED_APPS + ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--verbosity', '1',
    '--failed',
    '--nologcapture',

    # Specs
    '--with-spec', '--spec-color',

    # Coverage
    '--with-coverage',
    '--cover-erase',
    # Packages to cover
    '--cover-package', 'projects, progresses, commits, core',

    # Packages to test
    'projects', 'progresses', 'commits', 'core',

    '--exclude=functional'
]

CELERY_ALWAYS_EAGER = True
