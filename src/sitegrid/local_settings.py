STATIC_URL = '/static/'
ALLOWED_HOSTS = {
    '192.168.99.100'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sitegrid',
        'PASSWORD': 'docker',
        'USER': 'docker',
        'HOST': 'db',
    }
}

SITE_ID = 1

AUTH_USER_MODEL = 'accounts.User'