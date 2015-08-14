from environ import Env, Path

root = Path(__file__) - 2 # two folders up
BASE_DIR = root()

# set default values and casting
env = Env(
    DEBUG=(bool, False),
    LOCAL=(bool, False)
)
Env.read_env(
    env_file='.env.local' if env('LOCAL') else '.env'
)

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = [
    '.nova.jobs'
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    #'core',
    #'signup',
    #'scheduler',
    #'review',
    'homepage',
)
if env('LOCAL'):
    INSTALLED_APPS += (
        'django.contrib.admin',
        'django_extensions',
        'rosetta',
    )

MIDDLEWARE_CLASSES = (
    # before any that modify the Vary header
    'django.middleware.cache.UpdateCacheMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'donottrack.middleware.DoNotTrackMiddleware',
    'django.middleware.common.CommonMiddleware',

    # after any that modify the Vary header
    'django.middleware.cache.FetchFromCacheMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'nova.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # TODO cached template loader
            #'loaders': [
            #    ('django.template.loaders.cached.Loader', [
            #        'django.template.loaders.filesystem.Loader',
            #        'django.template.loaders.app_directories.Loader',
            #    ]),
            #]
        },
    },
]

WSGI_APPLICATION = 'nova.wsgi.application'


DATABASES = {
    'default': env.db()
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    root('locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# absolute path to the directory where collectstatic
# will collect static files for deployment
STATIC_ROOT = root('public', 'static')

# URL to use when referring to static files located in STATIC_ROOT
STATIC_URL = '/static/'

# additional absolute paths the staticfiles app will traverse if the
# FileSystemFinder finder is enabled, e.g. if you use the collectstatic or
# findstatic management command or use the static file serving view
STATICFILES_DIRS = (
    root('static'),
)

# Fingerprint static resources (cache busting) so that we can serve them
# with far-future expires headers and not run into stale cache problems.
# This makes the static template tag insert content hashes into filenames.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# make Django Compressor work with `./manage.py collectstatic`
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# will be using `./manage.py compress` to pre-build compress-tagged assets
COMPRESS_OFFLINE = True

# any template variables inside compress blocks have to be declared here
#COMPRESS_OFFLINE_CONTEXT = {
#}

# minify CSS
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

# don't append query strings to url() assets in CSS
COMPRESS_CSS_HASHING_METHOD = None


# Django Cache Framework
def _get_caches():
    if env('LOCAL'):
        return {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        }

    # Memcached in prod
    return {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': '/tmp/memcached.sock',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': {}
    }

CACHES = {
    'default': _get_caches()
}
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = 'nova'
