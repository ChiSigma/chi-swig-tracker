from flask import Blueprint, request, g
from flask_orator import jsonify
from src.auth.admin import inject_in_scope, has_access, verify_enums, verify_char_lens
from src.auth.default import inject_request_body, verify_presence
from src.models import Group

groups_admin = Blueprint('groups_admin', __name__)
REQUIRED_VALUES = ['name']
VALID_PRIVACY_SETTINGS = ['public', 'hide_events', 'unlisted']
NAME_CHAR_LIMIT = 10
BIO_CHAR_LIMIT = 22


@groups_admin.route('', methods=['GET'])
@inject_in_scope(model=Group, inject='groups')
def get_groups(groups):
    return jsonify({'groups': groups.admin_serialize()})


@groups_admin.route('/<int:group_id>', methods=['PUT'])
@has_access(model=Group, id_key='group_id', inject=True)
@inject_request_body(allowed=Group.admin_writable())
@verify_enums(enumerated_values={'privacy_setting': VALID_PRIVACY_SETTINGS})
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
