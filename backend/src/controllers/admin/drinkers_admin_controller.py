from flask import Blueprint, request, g
from flask_orator import jsonify
from src.auth.admin import inject_in_scope, has_access, verify_enums, verify_char_lens
from src.auth.default import inject_request_body, verify_presence
from src.models import Drinker, Membership

drinkers_admin = Blueprint('drinkers_admin', __name__)
VALID_PRIVACY_SETTINGS = ['public', 'hide_events', 'unlisted']
VALID_MEMBERSHIP_TYPES = ['primary', 'ephemeral']
ALLOWED_MEMBERSHIP_FIELDS = ['drinker_id', 'group_id', 'type', 'admin']
REQUIRED_MEMBERSHIP_FIELDS = ['drinker_id', 'group_id', 'type']
VALID_MEMBERSHIP_SETTINGS = ['open', 'private', 'ephemeral', 'primary']
NAME_CHAR_LIMIT = 10
BIO_CHAR_LIMIT = 22


@drinkers_admin.route('', methods=['GET'])
@inject_in_scope(model=Drinker, inject='drinkers')
def get_drinkers(drinkers):
    return jsonify({'drinkers': drinkers.admin_serialize()})


@drinkers_admin.route('/<int:drinker_id>', methods=['PUT'])
@has_access(model=Drinker, id_key='drinker_id', inject=True)
@inject_request_body(allowed=Drinker.admin_writable())
@verify_enums(enumerated_values={'privacy_setting': VALID_PRIVACY_SETTINGS, 'membership_policy': VALID_MEMBERSHIP_SETTINGS})
@verify_char_lens(char_values={'name': NAME_CHAR_LIMIT, 'bio_line': BIO_CHAR_LIMIT})
def edit_drinker(drinker, data):
    if 'profile_photos' in data:
        raw_profile_photos = data['profile_photos']
        data['profile_photos'] = ','.join([url.strip() for url in raw_profile_photos.split(',')])

    drinker.update(data)
    return jsonify(drinker.admin_serialize())


@drinkers_admin.route('/<int:drinker_id>', methods=['DELETE'])
@has_access(model=Drinker, id_key='drinker_id', inject=True, superuser=True)
def delete_drinker(drinker):
    success = drinker.delete()
    return jsonify(success)


@drinkers_admin.route('/<int:drinker_id>/memberships', methods=['GET'])
@has_access(model=Drinker, id_key='drinker_id', inject=True)
def get_memberships(drinker):
    return jsonify(Membership.where('drinker_id', '=', drinker.id).get().serialize())


@drinkers_admin.route('/<int:drinker_id>/memberships/<int:membership_id>', methods=['DELETE'])
@has_access(id_keys={ Drinker: 'drinker_id', Membership: 'membership_id' } , inject=True)
def delete_membership(drinker, membership):
    success = membership.delete()
    return jsonify(success)


@drinkers_admin.route('/<int:drinker_id>/memberships/<int:membership_id>', methods=['PUT'])
@has_access(id_keys={ Drinker: 'drinker_id', Membership: 'membership_id' } , inject=True)
@inject_request_body(allowed=ALLOWED_MEMBERSHIP_FIELDS)
@verify_enums(enumerated_values={'type': VALID_MEMBERSHIP_TYPES, 'admin': [True, False]})
def edit_membership(drinker, membership, data):
    membership.update(data)
    return jsonify(membership.serialize())


@drinkers_admin.route('/<int:drinker_id>/memberships', methods=['POST'])
@has_access(id_keys={ Drinker: 'drinker_id' } , inject=True)
@inject_request_body(allowed=ALLOWED_MEMBERSHIP_FIELDS)
@verify_presence(required=REQUIRED_MEMBERSHIP_FIELDS)
@verify_enums(enumerated_values={'type': VALID_MEMBERSHIP_TYPES, 'admin': [True, False]})
def create_membership(drinker, data):
    membership = membership.create(data)
    return jsonify(membership.serialize())
