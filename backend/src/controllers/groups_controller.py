from flask import Blueprint, request
from flask_orator import jsonify
from src.auth.default import protect_events, api_requires_auth, api_requires_body, api_requires_types
from src.models.drinker import Drinker
from src.models.event import Event
from src.models.event_type import EventType
from src.models.group import Group

groups = Blueprint('groups', __name__)

@groups.route('/', methods=['GET'])
def get_groups():
    # TODO :: Need to filter based on auth!
    return jsonify({'groups': Group.all().serialize(), 'version': Group.version()})


@groups.route('/version', methods=['GET'])
def get_version():
    return jsonify(Group.version())


@groups.route('/sort', methods=['GET'])
def sort_groups():
    # TODO :: Need to sort based on auth!
    event_type = request.args.get('event_type_id', 1)
    order = request.args.get('order', 'DESC')
    time = request.args.get('time', '*')
    sorted_group_ids = Group.sort_by_event(event_type=event_type, time=time, order=order)

    return jsonify(sorted_group_ids)


@groups.route('/<int:drinker_id>/is_public', methods=['PUT'])
@api_requires_auth
@api_requires_body('is_public')
@api_requires_types(is_public=bool)
def update_is_public(drinker_id):
    # TODO :: No longer the correct endpoint
    drinker = Drinker.find_or_fail(drinker_id)
    body = request.get_json()
    drinker.update(is_public=body['is_public'])

    return jsonify(drinker)


@groups.route('/<int:group_id>/events', methods=['GET'])
def get_group_events(group_id):
    # TODO :: Need to protect this
    group = Group.find_or_fail(group_id)
    
    return jsonify(group.event_counts())


@groups.route('/<int:group_id>/drinkers', methods=['GET'])
def get_group_drinkers(group_id):
    # TODO :: Need to filter these by in_scope
    group = Group.find_or_fail(group_id)
    primary_drinkers = group.primary_drinkers.serialize()
    ephemeral_drinkers = group.ephemeral_drinkers.serialize()

    return jsonify({'drinkers': [drinker for drinker in primary_drinkers + ephemeral_drinkers], 'version': Drinker.version()})


@groups.route('/<int:group_id>/drinkers/sort', methods=['GET'])
def sort_group_drinkers(group_id):
    # TODO :: Need to filter these by in_scope
    group = Group.find_or_fail(group_id)
    primary_drinkers = list(group.primary_drinkers.pluck('id'))
    ephemeral_drinkers = list(group.ephemeral_drinkers.pluck('id'))

    event_type = request.args.get('event_type_id', 1)
    order = request.args.get('order', 'DESC')
    time = request.args.get('time', '*')
    sorted_drinker_ids = Drinker.sort_by_event(event_type=event_type, time=time, order=order, in_scope=primary_drinkers + ephemeral_drinkers)

    return jsonify(sorted_drinker_ids)
