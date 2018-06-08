from flask import Blueprint, request, g
from flask_orator import jsonify
from src.auth.default import has_access, inject_in_scope
from src.models import Drinker, Event, EventType, Group

groups = Blueprint('groups', __name__)

@groups.route('', methods=['GET'])
@inject_in_scope(model=Group, inject='groups')
def get_groups(groups):
    return jsonify({'groups': groups.with_('primary_memberships.drinker').public_serialize(), 'version': groups.version(), 'is_limited': g.get('is_limited', False)})


@groups.route('/version', methods=['GET'])
@inject_in_scope(model=Group, inject='groups')
def get_version(groups):
    return jsonify({'version': groups.version(), 'is_limited': g.get('is_limited', False)})


@groups.route('/sort', methods=['GET'])
@inject_in_scope(model=Group, inject='groups')
def sort_groups(groups):
    # Scoping is handled at the model level
    event_type = request.args.get('event_type_id', 1)
    order = request.args.get('order', 'DESC')
    time = request.args.get('time', '*')
    sorted_group_ids = Group.sort_by_event(event_type=event_type, time=time, order=order, in_scope=groups)

    return jsonify(sorted_group_ids)


@groups.route('/<int:drinker_id>/is_public', methods=['PUT'])
def update_is_public(drinker_id):
    # TODO :: No longer the correct endpoint
    drinker = Drinker.find_or_fail(drinker_id)
    body = request.get_json()
    drinker.update(is_public=body['is_public'])

    return jsonify(drinker)
