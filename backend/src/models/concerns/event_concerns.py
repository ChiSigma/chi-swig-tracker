from src.app import db
from src.support.exceptions import DrinkCountException


class EventConcerns(object):
    @classmethod
    def create(cls, _attributes=None, **attributes):
        if _attributes.get('event_type_id', 0) == 1:
            from src.models import Drinker

            drinker = Drinker.with_('events').find(_attributes['drinker_id'])
            drink_count_limit = drinker.drink_count_limit
            drink_time_limit = drinker.drink_time_limit
            event_count = drinker.events().where('event_type_id', '=', 1).created_within(time=drink_time_limit).count()
            if event_count + 1 > drink_count_limit:
                raise DrinkCountException(drink_count_limit, drink_time_limit)

        return super(EventConcerns, cls).create(_attributes, **attributes)
