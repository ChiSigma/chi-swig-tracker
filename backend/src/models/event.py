import drinker
import event_type
import model
from orator.orm import belongs_to, scope

class Event(model.Model):
    __fillable__ = ['event_type_id']
    __touches__ = ['drinker']

    @belongs_to
    def drinker(self):
        return drinker.Drinker

    @belongs_to
    def event_type(self):
        return event_type.EventType
