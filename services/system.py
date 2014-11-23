from os import environ
import mongoengine
import settings


def connect_mongo():
    try:
        mongoengine.connection.get_connection()
    except mongoengine.ConnectionError:
        mongoengine.connect(get_mongo_settings().get('database'))

def get_mongo_settings():
    if environ.get('APP_ENVIRONMENT', 'production') == 'testing':
        print "Connected to test"
        return settings.mongo_test
    return settings.mongo

def get_env():
    return environ.get('APP_ENVIRONMENT', 'production')
