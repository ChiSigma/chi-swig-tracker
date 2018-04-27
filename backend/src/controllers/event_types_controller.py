from flask import Blueprint
from flask_orator import jsonify
from src.models.event_type import EventType

event_types = Blueprint('event_types', __name__)

@event_types.route('/', methods=['GET'])
def get_event_types():
    return jsonify(EventType.all())