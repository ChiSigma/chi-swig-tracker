import os
import logging
from flask import Flask, render_template, send_file, jsonify
from flask_orator import Orator
from flask_login import LoginManager
from .config import DevelopmentConfig, ProductionConfig

# Creating Flask application
app = Flask(__name__, static_folder=os.path.join(os.getcwd(),'frontend','build', 'static'), template_folder=os.path.join(os.getcwd(),'frontend','build'))

# Initializing config
mode = os.environ.get('FLASK_ENV', None)
if mode == 'development':
    app.config.from_object(DevelopmentConfig)

    # Setting so ORATOR SQL queries get logged
    default_db = app.config['ORATOR_DATABASES']['default']
    app.config['ORATOR_DATABASES'][default_db]['log_queries'] = True

    logger = logging.getLogger('orator.connection.queries')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        'It took %(elapsed_time)sms to execute the query %(query)s'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
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
    from .support import scheduler
    print "Starting job scheduler"
    scheduler.start()

# Initialize Authentication
from .auth.default import auth_routes
app.register_blueprint(auth_routes, url_prefix='/auth')

# Register Error Handler
from .support.exceptions import SwigCoreException
base_class_exception = Exception
if mode == 'development':
    base_class_exception = SwigCoreException
@app.errorhandler(base_class_exception)
def handle_swig_core_exception(error):
    status_code = 500
    payload = {'error': 'The application hit an unknown error. Please contact support.'}

    if isinstance(error, SwigCoreException):
        payload = error.to_dict()
        status_code = error.status_code
    else:
        from .support.slack_alerts import exception_alert
        app.logger.error('Unhandled Exception: %s', (error))
        exception_alert(error)

    response = jsonify(payload)
    return response, status_code

# Initialize Default Routes
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_file(app.template_folder + '/favicon.ico')

# Initialize Default API Routes
from .controllers import drinkers, event_types, groups, events
app.register_blueprint(drinkers, url_prefix="/api/drinkers")
app.register_blueprint(event_types, url_prefix="/api/event_types")
app.register_blueprint(groups, url_prefix="/api/groups")
app.register_blueprint(events, url_prefix="/api/events")

# Initialize Admin API Routes
from .controllers.admin import drinkers_admin, groups_admin, memberships_admin
app.register_blueprint(drinkers_admin, url_prefix="/api/admin/drinkers")
app.register_blueprint(groups_admin, url_prefix="/api/admin/groups")
app.register_blueprint(memberships_admin, url_prefix="/api/admin/memberships")
