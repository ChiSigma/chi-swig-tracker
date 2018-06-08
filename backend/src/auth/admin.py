from src.support import decorators
from src.support.exceptions import InvalidEnumException, InvalidCharException
from flask import Blueprint, session, redirect, url_for, request, g
from flask_login import current_user 
from flask_orator import jsonify
from functools import wraps
from default import inject_in_scope as default_scope_injection, has_access as default_has_access


@decorators.parametrized
def inject_in_scope(f, **params):
  @wraps(f)
  @default_scope_injection(model=params['model'], inject=params['inject'], scope='admin')
  def decorated(*args, **kwargs):
    return f(*args, **kwargs)
    
  return decorated


@decorators.parametrized
def has_access(f, **params):
  @wraps(f)
  @default_has_access(model=params['model'], id_key=params.get('id_key', None), scope='admin', 
                      superuser=params.get('superuser', False), inject=params.get('inject', False))
  def decorated(*args, **kwargs):
    return f(*args, **kwargs)
    
  return decorated


@decorators.parametrized
def verify_enums(f, **params):
    @wraps(f)
    def decorated(*args, **kwargs):
        enumerated_values = params.get('enumerated_values', {})
        for field in enumerated_values:
            request_data = kwargs.get('data', {})
            request_value = request_data.get(field, None)
            permitted_values = enumerated_values.get(field, [])
            if request_value and request_value not in permitted_values:
                raise InvalidEnumException(value=request_value, field=field)
        return f(*args, **kwargs)

    return decorated


@decorators.parametrized
def verify_char_lens(f, **params):
    @wraps(f)
    def decorated(*args, **kwargs):
        char_values = params.get('char_values', {})
        for field in char_values:
            request_data = kwargs.get('data', {})
            request_value = request_data.get(field, None)
            permitted_length = char_values.get(field, 0)
            if request_value and len(request_value) > permitted_length:
                raise InvalidCharException(value=request_value, field=field, error='Too long!')
        return f(*args, **kwargs)

    return decorated
