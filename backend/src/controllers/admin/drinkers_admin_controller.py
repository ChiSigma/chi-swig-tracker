from flask import Blueprint, request, g
from flask_orator import jsonify
from src.auth.admin import inject_in_scope, has_access, verify_enums, verify_char_lens
from src.auth.default import inject_request_body
from src.models import Drinker

drinkers_admin = Blueprint('drinkers_admin', __name__)
VALID_PRIVACY_SETTINGS = ['public', 'hide_events', 'unlisted']
NAME_CHAR_LIMIT = 10
BIO_CHAR_LIMIT = 22


@drinkers_admin.route('', methods=['GET'])
@inject_in_scope(model=Drinker, inject='drinkers')
def get_drinkers(drinkers):
    return jsonify({'drinkers': drinkers.admin_serialize()})


@drinkers_admin.route('/<int:drinker_id>', methods=['PUT'])
@has_access(model=Drinker, id_key='drinker_id', inject=True)
@inject_request_body(allowed=Drinker.admin_writable())
@verify_enums(enumerated_values={'privacy_setting': VALID_PRIVACY_SETTINGS})
@verify_char_lens(char_values={'name': NAME_CHAR_LIMIT, 'bio_line': BIO_CHAR_LIMIT})
def edit_drinker(drinker, data):
    if 'profile_photos' in data:
        raw_profile_photos = data['profile_photos']
        data['profile_photos'] = ','.join([url.strip() for url in raw_profile_photos.split(',')])

    drinker.update(data)
    return jsonify(drinker.admin_serialize())
