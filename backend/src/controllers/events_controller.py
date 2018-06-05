from flask import Blueprint, request, g
from flask_orator import jsonify
from src.auth.default import protect_events, has_access, inject_in_scope
from src.models.drinker import Drinker
from src.models.event import Event
from src.models.event_type import EventType
from src.models.group import Group

events = Blueprint('events', __name__)

@events.route('/', methods=['GET'])
@inject_in_scope(model=Event, inject='events')
def get_events(events):
    return jsonify({'events': events.get().serialize(), 'is_limited': g.get('is_limited', False)})

@events.route('/counts', methods=['GET'])
@inject_in_scope(model=Event, inject='events')
def get_event_counts(events):
    return jsonify({'counts': Event.counts(scope=events), 'is_limited': g.get('is_limited', False)})
