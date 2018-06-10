import requests
from src.app import app
from src.models import Drinker, PrimaryMembership
from oauth import OAuthSignIn
from src.support import decorators
from src.support.exceptions import ForbiddenAccessException, InvalidRequestException
from flask import Blueprint, session, redirect, url_for, request, flash, g
from flask_login import login_user, logout_user, current_user 
from flask_orator import jsonify
from functools import wraps
from src.support.utils import keydefaultdict
from src.support.slack_alerts import new_user_alert

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
      drinker = Drinker.create(_unsafe=True, name=name, email=email)
      new_user_alert(name, email)


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
    is_superuser = (not current_user.is_anonymous) and current_user.superuser
    superuser_required = params.get('superuser', False)
    # Short circuit if superuser level is required and current_user isn't super
    if superuser_required and not is_superuser:
      raise ForbiddenAccessException('this superuser-required action.')

    # Models mapped to the key to lookup the requested model.id in kwargs
    models_and_id_keys = { params['model']: params['id_key'] } if 'id_key' in params else params.get('id_keys', {})

    # Models mapped to the requested model.id
    models_and_ids = { model: kwargs[models_and_id_keys[model]] for model in models_and_id_keys }

    # Method to call on model to get the desired scope
    scope_method = 'in_{0}_scope'.format(params['scope']) if 'scope' in params else 'in_scope'

    # Cache of Model mapped to the individual models that are in scope
    # Not really being used, but could be useful to set on g and use in all auth methods
    models_in_scope_cache = keydefaultdict(lambda model: getattr(model, scope_method)().get())
    
    for model in models_and_ids:
      requested_model_id = models_and_ids[model]
      models = { m.id: m for m in models_in_scope_cache[model] }

      if requested_model_id not in models:
        raise ForbiddenAccessException('{0}: {1}'.format(model.__name__, requested_model_id))

      if params.get('inject', False):
        kwargs[models_and_id_keys[model].replace('_id', '')] = models[requested_model_id]
        del kwargs[models_and_id_keys[model]]

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
    membership_policies = [mp for mp in request.args['membership_policies'].split(',')] if 'membership_policies' in request.args else []
    time = request.args.get('time', None)

    filtered_scope = getattr(params['model'], 'filter')(params['model'], ids=ids, 
                                                                         drinker_ids=drinker_ids, 
                                                                         group_ids=group_ids, 
                                                                         event_type_ids=event_type_ids, 
                                                                         time=time,
                                                                         membership_policies=membership_policies)
    
    scope_method = 'in_{0}_scope'.format(params['scope']) if 'scope' in params else 'in_scope'
    unscoped_length = filtered_scope.count()
    scope = getattr(filtered_scope, scope_method)()

    kwargs[params['inject']] = scope
    scoped_length = scope.count()
    g.num_in_scope = scoped_length
    g.is_limited = unscoped_length > scoped_length

    return f(*args, **kwargs)
    
  return decorated


@decorators.parametrized
def inject_request_body(f, **params):
  @wraps(f)
  def decorated(*args, **kwargs):
    data = request.get_json(force=True, silent=True)
    if data is None:
      raise InvalidRequestException('Expected a JSON request body!')

    if 'allowed' in params:
      data = {k:data[k] for k in params['allowed'] if k in data}

    kwargs['data'] = data
    return f(*args, **kwargs)

  return decorated


@decorators.parametrized
def verify_presence(f, **params):
    @wraps(f)
    def decorated(*args, **kwargs):
        required = params.get('required', [])
        for field in required:
            request_data = kwargs.get('data', {})
            if field not in request_data:
                raise InvalidRequestException('Expected Field: {0}'.format(field))
        return f(*args, **kwargs)

    return decorated
