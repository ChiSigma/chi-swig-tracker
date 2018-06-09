from flask import Blueprint, request, g
from flask_orator import jsonify
from src.auth.admin import inject_in_scope, has_access, verify_enums, verify_char_lens
from src.auth.default import inject_request_body, verify_presence
from src.models import Group, Membership

groups_admin = Blueprint('groups_admin', __name__)
REQUIRED_VALUES = ['name']
VALID_PRIVACY_SETTINGS = ['public', 'hide_events', 'unlisted']
VALID_MEMBERSHIP_SETTINGS = ['open', 'private', 'ephemeral', 'primary']
VALID_MEMBERSHIP_TYPES = ['primary', 'ephemeral']
ALLOWED_MEMBERSHIP_FIELDS = ['drinker_id', 'group_id', 'type', 'admin']
REQUIRED_MEMBERSHIP_FIELDS = ['drinker_id', 'group_id', 'type']
NAME_CHAR_LIMIT = 10
BIO_CHAR_LIMIT = 24


@groups_admin.route('', methods=['GET'])
@inject_in_scope(model=Group, inject='groups')
def get_groups(groups):
    return jsonify({'groups': groups.admin_serialize()})


@groups_admin.route('/<int:group_id>', methods=['PUT'])
@has_access(model=Group, id_key='group_id', inject=True)
@inject_request_body(allowed=Group.admin_writable())
@verify_enums(enumerated_values={'privacy_setting': VALID_PRIVACY_SETTINGS, 'membership_policy': VALID_MEMBERSHIP_SETTINGS})
@verify_char_lens(char_values={'name': NAME_CHAR_LIMIT, 'bio_line': BIO_CHAR_LIMIT})
def edit_group(group, data):
    group.update(data)
    return jsonify(group.admin_serialize())


@groups_admin.route('', methods=['POST'])
@has_access(model=Group, superuser=True)
@inject_request_body(allowed=Group.admin_writable())
@verify_presence(required=REQUIRED_VALUES)
@verify_enums(enumerated_values={'privacy_setting': VALID_PRIVACY_SETTINGS})
@verify_char_lens(char_values={'name': NAME_CHAR_LIMIT, 'bio_line': BIO_CHAR_LIMIT})
def create_group(data):
    group = Group.create(data)
    return jsonify(group.admin_serialize())


@groups_admin.route('/<int:group_id>', methods=['DELETE'])
@has_access(model=Group, id_key='group_id', inject=True, superuser=True)
def delete_group(group):
    success = group.delete()
    return jsonify(success)


@groups_admin.route('/<int:group_id>/memberships', methods=['GET'])
@has_access(model=Group, id_key='group_id', inject=True)
def get_memberships(group):
    return jsonify(Membership.where('group_id', '=', group.id).get().serialize())


@groups_admin.route('/<int:group_id>/memberships/<int:membership_id>', methods=['DELETE'])
@has_access(id_keys={ Group: 'group_id', Membership: 'membership_id' } , inject=True)
def delete_membership(group, membership):
    success = membership.delete()
    return jsonify(success)


@groups_admin.route('/<int:group_id>/memberships/<int:membership_id>', methods=['PUT'])
@has_access(id_keys={ Group: 'group_id', Membership: 'membership_id' } , inject=True)
@inject_request_body(allowed=ALLOWED_MEMBERSHIP_FIELDS)
@verify_enums(enumerated_values={'type': VALID_MEMBERSHIP_TYPES, 'admin': [True, False]})
def edit_membership(group, membership, data):
    membership.update(data)
    return jsonify(membership.serialize())


@groups_admin.route('/<int:group_id>/memberships', methods=['POST'])
@has_access(id_keys={ Group: 'group_id' } , inject=True)
@inject_request_body(allowed=ALLOWED_MEMBERSHIP_FIELDS)
@verify_presence(required=REQUIRED_MEMBERSHIP_FIELDS)
@verify_enums(enumerated_values={'type': VALID_MEMBERSHIP_TYPES, 'admin': [True, False]})
def create_membership(group, data):
    Membership.create(data)
    membership = Membership.where('group_id', '=', group.id).order_by('id', 'desc').limit(1).first()
    return jsonify(membership.serialize())
