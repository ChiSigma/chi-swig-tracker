import os
from flask import Flask
from flask_orator import Orator, jsonify
from flask_dotenv import DotEnv
from authlib.flask.client import OAuth
from .config import DevelopmentConfig, ProductionConfig

# Creating Flask application
app = Flask(__name__)

# Initializing config
mode = os.environ.get('RUN_MODE', None)
if mode == 'development':
	app.config.from_object(DevelopmentConfig)
else:
	app.config.from_object(ProductionConfig)

# Initializing Orator
db = Orator(app)
if mode == 'development':
    db.connection().enable_query_log()

# Initialize Authentication
oauth = OAuth(app)
auth = oauth.register(
        app.config['AUTH_PROVIDER'],
        client_id=app.config['AUTH_CONFIG']['client_id'],
        client_secret=app.config['AUTH_CONFIG']['client_secret'],
        api_base_url=app.config['AUTH_CONFIG']['api_base_url'],
        access_token_url=app.config['AUTH_CONFIG']['access_token_url'],
        authorize_url=app.config['AUTH_CONFIG']['authorize_url'],
        client_kwargs=app.config['AUTH_CONFIG']['client_kwargs']
    )
from .auth.default import auth_routes
app.register_blueprint(auth_routes, url_prefix='/auth')

# Initialize Routes
from .controllers.drinkers_controller import drinkers
from .controllers.event_types_controller import event_types
app.register_blueprint(drinkers, url_prefix="/api/drinkers")
app.register_blueprint(event_types, url_prefix="/api/event_types")
