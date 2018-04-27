from flask import Blueprint, request
from flask_orator import jsonify
from src.auth.default import protect_events, api_requires_auth
from src.models.drinker import Drinker
from src.models.event import Event

drinkers = Blueprint('drinkers', __name__)


@drinkers.route('/', methods=['GET'])
@api_requires_auth
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
@api_requires_auth
def add_event(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    event = drinker.events().create(**request.get_json())

    return jsonify(event)


@drinkers.route('/<int:drinker_id>/events', methods=['DELETE'])
@api_requires_auth
def delete_event(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    one_deleted = drinker.events().created_within('30m').last().delete()

    return one_deleted
