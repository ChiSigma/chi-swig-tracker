from flask import Blueprint, request, g
from flask_orator import jsonify
from src.support.exceptions import NoModelException
from src.auth.default import has_access, inject_in_scope, inject_request_body
from src.models import Drinker, Event, EventType

drinkers = Blueprint('drinkers', __name__)


@drinkers.route('', methods=['GET'])
@inject_in_scope(model=Drinker, inject='drinkers')
def get_drinkers(drinkers):
    return jsonify({'drinkers': drinkers.with_('primary_membership.group', 'ephemeral_memberships.group').public_serialize(), 'version': drinkers.version(), 'is_limited': g.get('is_limited', False)})


@drinkers.route('/version', methods=['GET'])
@inject_in_scope(model=Drinker, inject='drinkers')
def get_version(drinkers):
    return jsonify({'version': drinkers.version(), 'is_limited': g.get('is_limited', False)})


@drinkers.route('/sort', methods=['GET'])
@inject_in_scope(model=Drinker, inject='drinkers')
def sort_drinkers(drinkers):
    event_type = request.args.get('event_type_id', 1)
    normalized = request.args.get('normalized', 'false') == 'true'
    order = request.args.get('order', 'DESC')
    time = request.args.get('time', '*')
    # Scoping is handled @ the model level
    sorted_drinker_ids = Drinker.sort_by_event(event_type=event_type, time=time, order=order, in_scope=drinkers, normalized=normalized)

    return jsonify(sorted_drinker_ids)


@drinkers.route('/<int:drinker_id>/events/<int:event_type_id>', methods=['POST'])
@has_access(model=Drinker, scope='member', id_key='drinker_id')
@inject_request_body(allowed=['location'])
def add_event(drinker_id, event_type_id, data):
    drinker = Drinker.find_or_fail(drinker_id)
    event_type = EventType.find_or_fail(event_type_id)
    location = data.get('location', 'unknown')
    event = Event.create(event_type_id=event_type_id, drinker_id=drinker_id, location=location)

    return jsonify(event)


@drinkers.route('/<int:drinker_id>/events/<int:event_type_id>', methods=['DELETE'])
@has_access(model=Drinker, scope='member', id_key='drinker_id')
def delete_event(drinker_id, event_type_id):
    # Need to add group member auth too
    drinker = Drinker.find_or_fail(drinker_id)
    event_type = EventType.find_or_fail(event_type_id)
    one_deleted = Event.where('drinker_id', '=', drinker_id).where('event_type_id', '=', event_type_id).created_within('30m').last().delete()

    if not one_deleted: raise NoModelException('Could not delete. 0 {0} events within a 30m window.'.format(event_type.name))
    return jsonify(one_deleted)
