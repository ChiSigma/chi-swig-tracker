import drinker
import event_type
import primary_membership
import model
from concerns import model_concerns, event_concerns
from src.auth import EventAuthMixin
from orator.orm import belongs_to, scope


class Event(model_concerns.ModelConcerns, event_concerns.EventConcerns, EventAuthMixin, model.Model):
    __fillable__ = ['event_type_id', 'drinker_id']
    __touches__ = ['drinker']

    @belongs_to
    def drinker(self):
        return drinker.Drinker

    @belongs_to
    def event_type(self):
        return event_type.EventType

    @staticmethod
    def filter(scope, **kwargs):
        if kwargs.get('time', None):
            in_scope_ids = list(set(scope.lists('id')))
            scope = Event.created_within(time=kwargs['time']).where_in('events.id', in_scope_ids)

        if kwargs.get('event_type_ids', []):
            in_scope_ids = list(set(scope.lists('id')))
            scope = Event.where_in('event_type_id', kwargs['event_type_ids']).where_in('events.id', in_scope_ids)

        if kwargs.get('drinker_ids', []):
            drinker_ids = list(set(kwargs.get('drinker_ids', [])))
            in_scope_ids = list(set(scope.lists('id')))
            scope = Event.where_in('drinker_id', drinker_ids).where_in('events.id', in_scope_ids)

        if kwargs.get('group_ids', []):
            group_ids = list(set(kwargs.get('group_ids', [])))
            in_scope_event_ids = scope.lists('id')
            primary_drinker_ids = primary_membership.PrimaryMembership.where_in('group_id', group_ids).lists('drinker_id')
            scope = Event.where_in('drinker_id', primary_drinker_ids).where_in('events.id', in_scope_event_ids)

        event_ids = scope.lists('id')
        return Event.where_in('events.id', event_ids)

    @staticmethod
    def counts(scope=None):
        event_sums = {e_type.name: {window[0]: 0 for window in event_type.EventType.COUNT_WINDOWS} for e_type in event_type.EventType.all()}
        for window in event_type.EventType.COUNT_WINDOWS:
            window_name = window[0]
            time = window[1]
            event_ids = scope.lists('id')
            events_in_window = Event \
                                        .raw(raw_statement='count(*) as count, event_type_id') \
                                        .where_in('events.id', event_ids) \
                                        .created_within(time=time) \
                                        .group_by('event_type_id')

            for event_obj in events_in_window.with_('event_type').get():
                count = event_obj.count
                event_type_name = event_obj.event_type.name

                event_sums[event_type_name][window_name] += count
        return event_sums
