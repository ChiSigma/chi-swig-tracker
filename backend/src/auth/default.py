import requests
from src.app import auth, app
from src.models.drinker import Drinker
from src.auth.oauth import OAuthSignIn
from src.support import decorators
from flask import Blueprint, session, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user 
from flask_orator import jsonify
from functools import wraps
from six.moves.urllib.parse import urlencode

auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.route('/callback')
def callback_handling():
  if not current_user.is_anonymous:
    return redirect(url_for('index'))

  oauth = OAuthSignIn.get_provider()
  drinker_id = oauth.callback()
  if drinker_id is None:
      flash('Authentication failed.')
      return redirect(url_for('index'))

  drinker = Drinker.find(drinker_id)
  if not drinker:
    flash('Unknown drinker ID came back from OAuth.')
    return redirect(url_for('index'))

  login_user(drinker, True)
  return redirect(url_for('index'))


@auth_routes.route('/login')
def login():
  if not current_user.is_anonymous:
    return redirect(url_for('index'))

  oauth = OAuthSignIn.get_provider()
  return oauth.authorize()


@auth_routes.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))


@auth_routes.route('/me')
def get_me():
  if not current_user.is_anonymous:
    return jsonify(current_user)
  return jsonify({})


def api_requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if current_user.is_anonymous:
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
    if not drinker.is_public and current_user.is_anonymous:
        return True
    else:
        return False
