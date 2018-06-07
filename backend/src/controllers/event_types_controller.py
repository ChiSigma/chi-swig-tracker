from flask import Blueprint
from flask_orator import jsonify
from src.models import EventType

event_types = Blueprint('event_types', __name__)

@event_types.route('', methods=['GET'])
def get_event_types():
    event_type_info = {e_type.name: e_type.serialize() for e_type in EventType.all()}
    event_times = [window[0] for window in EventType.COUNT_WINDOWS]
    return jsonify({"event_types": event_type_info, "times": event_times})
