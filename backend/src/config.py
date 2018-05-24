from os import environ

class BaseConfig(object):
    SECRET_KEY = environ['SECRET_KEY']
    DEBUG = False
    ORATOR_DATABASES = {
		'default': 'postgres',
		'postgres': {
			'driver': 'pgsql',
			'host': environ['POSTGRES_HOST'],
			'database': environ['POSTGRES_DATABASE'],
			'user': environ['POSTGRES_USER'],
			'password': environ['POSTGRES_PASSWORD'],
			'prefix': ''
		}
	}
    AUTH_CONFIG = {
        'client_id': environ['CLIENT_ID'],
        'client_secret': environ['CLIENT_SECRET'],
        'api_base_url': environ['DOMAIN'],
        'access_token_url': environ['DOMAIN'] + '/oauth/token',
        'authorize_url': environ['DOMAIN'] + '/authorize',
        'client_kwargs': {
            'scope': 'profile app_metadata'
        }
    }
    AUTH_PROVIDER = 'auth0'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5001
    REDIRECT_URI = 'http://localhost:5001/auth/callback'
    HOME_URI = 'http://localhost:5001/'


class ProductionConfig(BaseConfig):
    HOST = '0.0.0.0'
    # Probably set these in your .env
    PORT = environ.get('PORT', None)
    REDIRECT_URI = environ.get('REDIRECT_URI', None)
    HOME_URI = environ.get('HOME_URI', None)

