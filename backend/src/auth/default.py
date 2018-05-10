import requests
from src.app import auth, app
from src.support import decorators
from flask import Blueprint, session, redirect, url_for, request
from flask_orator import jsonify
from functools import wraps
from six.moves.urllib.parse import urlencode

auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    resp = auth.authorize_access_token()

    url = app.config['AUTH_CONFIG']['api_base_url'] + '/userinfo'
    headers = {'authorization': 'Bearer ' + resp['access_token']}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()

    # Store the tue user information in flask session.
    session['jwt_payload'] = userinfo

    verified = userinfo.get('app_metadata', {}).get('verified', False)

    if verified:
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'email': userinfo.get('email', 'unknown@example.com')
        }
    else:
        session.clear()

    return redirect('/')


@auth_routes.route('/login')
def login():
    return auth.authorize_redirect(redirect_uri=app.config['REDIRECT_URI'], audience=app.config['AUTH_CONFIG']['api_base_url'] + '/userinfo')


@auth_routes.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': app.config['HOME_URI'], 'client_id': app.config['AUTH_CONFIG']['client_id']}
    return redirect(auth.api_base_url + '/v2/logout?' + urlencode(params))


@auth_routes.route('/me')
def get_me():
    return jsonify(session.get('profile', {}))


def api_requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return jsonify(False)
    return f(*args, **kwargs)
    
  return decorated

@decorators.parametrized
def api_requires_body(f, *params):
  @wraps(f)
  def decorated(*args, **kwargs):
    body = request.get_json()

    if len(list(set(params) & set(body.keys()))) != len(params):
      return jsonify(False)
    return f(*args, **kwargs)
    
  return decorated


@decorators.parametrized
def api_requires_types(f, **body_types):
  @wraps(f)
  def decorated(*args, **kwargs):
    body = request.get_json()

    for key, v_type in body_types.iteritems():
        if type(body[key]) is not v_type:
            return jsonify(False)
    return f(*args, **kwargs)
    
  return decorated


def protect_events(drinker=None):
    if not drinker.is_public and ('profile' not in session):
        return True
    else:
        return False
