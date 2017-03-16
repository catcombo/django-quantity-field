# coding: utf-8

SECRET_KEY = 'test'

INSTALLED_APPS = [
    'tests',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb',
    }
}
