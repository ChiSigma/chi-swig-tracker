from flask import Blueprint, request
from flask_orator import jsonify
from src.auth.default import protect_events, api_requires_auth
from src.models.drinker import Drinker
from src.models.event import Event
from src.models.event_type import EventType

drinkers = Blueprint('drinkers', __name__)


@drinkers.route('/', methods=['GET'])
def get_drinkers():
    return jsonify(Drinker.all())


@drinkers.route('/sort', methods=['GET'])
def sort_drinkers():
    event_type = request.args.get('event_type_id', 1)
    order = request.args.get('order', 'DESC')
    time = request.args.get('time', '*')
    return jsonify(Drinker.sort_by_event(event_type=event_type, time=time, order=order).pluck('id'))


@drinkers.route('/<int:drinker_id>/is_public', methods=['PUT'])
@api_requires_auth
def update_is_public(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    drinker.update(**request.get_json())

    return jsonify(drinker)


@drinkers.route('/<int:drinker_id>/events', methods=['GET'])
def get_drinker_events(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    if protect_events(drinker=drinker):
        return jsonify({})
    else:
        return jsonify(drinker.event_counts())


@drinkers.route('/<int:drinker_id>/events', methods=['POST'])
#@api_requires_auth
def add_event(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    params = request.get_json()
    event_type = EventType.find_or_fail(params.get('event_type_id', None))
    event = drinker.events().create(**params)

    return jsonify(event)


@drinkers.route('/<int:drinker_id>/events/<int:event_type_id>', methods=['DELETE'])
#@api_requires_auth
def delete_event(drinker_id, event_type_id):
    drinker = Drinker.find_or_fail(drinker_id)
    event_type = EventType.find_or_fail(event_type_id)
    one_deleted = drinker.events().where('event_type_id', '=', event_type_id).created_within('30m').last().delete()

    return jsonify(one_deleted)
