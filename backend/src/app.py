import os
import src.support.scheduler as scheduler
from flask import Flask, render_template
from flask_orator import Orator
from flask_login import LoginManager
from .config import DevelopmentConfig, ProductionConfig

# Creating Flask application
app = Flask(__name__, static_folder=os.path.join(os.getcwd(),'frontend','build', 'static'), template_folder=os.path.join(os.getcwd(),'frontend','build'))

# Initializing config
mode = os.environ.get('FLASK_ENV', None)
if mode == 'development':
	app.config.from_object(DevelopmentConfig)
else:
	app.config.from_object(ProductionConfig)

# Initializing Orator
db = Orator(app)
if mode == 'development':
    db.connection().enable_query_log()

# Login Manager
lm = LoginManager(app)

# Scheduler
if mode != 'development':
	print "Starting job scheduler"
	scheduler.scheduler.start()

# Initialize Authentication
from .auth.default import auth_routes
app.register_blueprint(auth_routes, url_prefix='/auth')

# Initialize Routes
@app.route('/')
def index():
	return render_template('index.html')

from .controllers.drinkers_controller import drinkers
from .controllers.event_types_controller import event_types
app.register_blueprint(drinkers, url_prefix="/api/drinkers")
app.register_blueprint(event_types, url_prefix="/api/event_types")
