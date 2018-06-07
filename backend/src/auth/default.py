import requests
from src.app import app
from src.models.drinker import Drinker
from src.models.primary_membership import PrimaryMembership
from src.auth.oauth import OAuthSignIn
from src.support import decorators
from src.support.exceptions import ForbiddenAccessException
from flask import Blueprint, session, redirect, url_for, request, flash, g
from flask_login import login_user, logout_user, current_user 
from flask_orator import jsonify
from functools import wraps

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/callback')
def callback_handling():
  if not current_user.is_anonymous:
    return redirect(url_for('index'))

  oauth = OAuthSignIn.get_provider()
  email, name = oauth.callback()
  if email is None:
      flash('Authentication failed.')
      return redirect(url_for('index'))

  drinker = Drinker.where('email', '=', email).first()

  if drinker is None:
    with Drinker.transaction():
      drinker = Drinker.create(name=name, email=email)
      PrimaryMembership.create(drinker_id=drinker.id, group_id=1)

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


@decorators.parametrized
def has_access(f, **params):
  @wraps(f)
  def decorated(*args, **kwargs):
    scope = 'in_{0}_scope'.format(params['scope']) if 'scope' in params else 'in_scope'
    if kwargs[params['id_key']] not in getattr(params['model'], scope)().lists('id'):
      raise ForbiddenAccessException('You do not have access to {0}: {1}').format(params['model'].name, params['id_key'])
    return f(*args, **kwargs)
    
  return decorated


@decorators.parametrized
def inject_in_scope(f, **params):
  @wraps(f)
  def decorated(*args, **kwargs):
    ids = [int(d) for d in request.args.get('ids').split(',') if d.isdigit()] if 'ids' in request.args else []
    drinker_ids = [int(d) for d in request.args.get('drinker_ids').split(',') if d.isdigit()] if 'drinker_ids' in request.args else []
    group_ids = [int(d) for d in request.args.get('group_ids').split(',') if d.isdigit()] if 'group_ids' in request.args else []
    event_type_ids = [int(d) for d in request.args['event_type_ids'].split(',') if d.isdigit()] if 'event_type_ids' in request.args else []
    time = request.args['time'] if 'time' in request.args else None

    filtered_scope = getattr(params['model'], 'filter')(params['model'], ids=ids, drinker_ids=drinker_ids, group_ids=group_ids, event_type_ids=event_type_ids, time=time)
    
    scope_method = 'in_{0}_scope'.format(params['scope']) if 'scope' in params else 'in_scope'
    unscoped_length = filtered_scope.count()
    scope = getattr(filtered_scope, scope_method)()

    kwargs[params['inject']] = scope
    g.is_limited = unscoped_length > scope.count()

    return f(*args, **kwargs)
    
  return decorated


def protect_events(drinker=None):
    if not drinker.is_public and current_user.is_anonymous:
        return True
    else:
        return False
