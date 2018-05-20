from flask import Blueprint, request
from flask_orator import jsonify
from src.auth.default import protect_events, api_requires_auth, api_requires_body, api_requires_types
from src.models.drinker import Drinker
from src.models.event import Event
from src.models.event_type import EventType

drinkers = Blueprint('drinkers', __name__)


@drinkers.route('/', methods=['GET'])
def get_drinkers():
    return jsonify({'drinkers': Drinker.all().serialize(), 'version': Drinker.version()})


@drinkers.route('/version', methods=['GET'])
def get_version():
    return jsonify(Drinker.version())


@drinkers.route('/sort', methods=['GET'])
def sort_drinkers():
    event_type = request.args.get('event_type_id', 1)
    order = request.args.get('order', 'DESC')
    time = request.args.get('time', '*')
    all_drinker_ids = Drinker.all().pluck('id')
    sorted_drinker_ids = list(Drinker.sort_by_event(event_type=event_type, time=time, order=order).pluck('id'))

    # Sort will not return an id if it has 0 events - have to append missing on the end
    return jsonify(sorted_drinker_ids + [drinker_id for drinker_id in all_drinker_ids if drinker_id not in sorted_drinker_ids])


@drinkers.route('/<int:drinker_id>/is_public', methods=['PUT'])
@api_requires_auth
@api_requires_body('is_public')
@api_requires_types(is_public=bool)
def update_is_public(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    body = request.get_json()
    drinker.update(is_public=body['is_public'])

    return jsonify(drinker)


@drinkers.route('/<int:drinker_id>/bio_line', methods=['PUT'])
@api_requires_auth
@api_requires_body('bio_line')
@api_requires_types(bio_line=str)
def update_bio_line(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    body = request.get_json()
    drinker.update(bio_line=body['bio_line'])

    return jsonify(drinker)


@drinkers.route('/<int:drinker_id>/profile_photos', methods=['PUT'])
@api_requires_auth
@api_requires_body('profile_photos')
@api_requires_types(profile_photos=str)
def update_profile_photos(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    body = request.get_json()
    raw_profile_photos = body['profile_photos']
    profile_photos = ','.join([url.strip() for url in raw_profile_photos.split(',')])
    drinker.update(profile_photos=profile_photos)

    return jsonify(drinker)


@drinkers.route('/<int:drinker_id>/profile_pivot_type', methods=['PUT'])
@api_requires_auth
@api_requires_body('profile_pivot_type')
@api_requires_types(profile_pivot_type=int)
def update_profile_pivot_type(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    body = request.get_json()
    profile_pivot_type = body['profile_pivot_type']
    event_type = EventType.find_or_fail(profile_pivot_type)
    drinker.update(profile_pivot_type=profile_pivot_type)

    return jsonify(drinker)


@drinkers.route('/<int:drinker_id>/profile_pivot_increment', methods=['PUT'])
@api_requires_auth
@api_requires_body('profile_pivot_increment')
@api_requires_types(profile_pivot_increment=int)
def update_profile_pivot_increment(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    body = request.get_json()
    drinker.update(profile_pivot_increment=body['profile_pivot_increment'])

    return jsonify(drinker)


@drinkers.route('/<int:drinker_id>/events', methods=['GET'])
def get_drinker_events(drinker_id):
    drinker = Drinker.find_or_fail(drinker_id)
    if protect_events(drinker=drinker):
        return jsonify({})
    else:
        return jsonify(drinker.event_counts())


@drinkers.route('/<int:drinker_id>/events/<int:event_type_id>', methods=['POST'])
@api_requires_auth
def add_event(drinker_id, event_type_id):
    drinker = Drinker.find_or_fail(drinker_id)
    event_type = EventType.find_or_fail(event_type_id)
    event = drinker.events().create(event_type_id=event_type_id)

    return jsonify(event)


@drinkers.route('/<int:drinker_id>/events/<int:event_type_id>', methods=['DELETE'])
@api_requires_auth
def delete_event(drinker_id, event_type_id):
    drinker = Drinker.find_or_fail(drinker_id)
    event_type = EventType.find_or_fail(event_type_id)
    one_deleted = drinker.events().where('event_type_id', '=', event_type_id).created_within('30m').last().delete()

    return jsonify(one_deleted)
