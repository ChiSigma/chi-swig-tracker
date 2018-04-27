import model
import event
from orator.orm import has_many, accessor

class Drinker(model.Model):
    __fillable__ = ['is_public']
    __hidden__   = ['events']
    # (Name for the frontend, window for querying the db)
    COUNT_WINDOWS = [('Past Day', '24h'), ('Past Week', '7d'), ('All Time', '*')]

    @staticmethod
    def sort_by_event(event_type=None, time=None, order=None):
        sorted_drinker_ids = event.Event \
                                    .raw(raw_statement='count(*) as count, drinker_id') \
                                    .created_within(time=time) \
                                    .group_by('drinker_id') \
                                    .order_by('count', order)

        return sorted_drinker_ids.with_('drinker').get().map(lambda e: e.drinker)

    @has_many
    def events(self):
        return event.Event

    def event_counts(self):
        event_sums = {}
        for window in self.COUNT_WINDOWS:
            window_name = window[0]
            time = window[1]
            events_in_window = self.events() \
                                            .raw(raw_statement='count(*) as count, event_type_id') \
                                            .created_within(time=time) \
                                            .group_by('event_type_id')

            for event_obj in events_in_window.with_('event_type').get():
                count = event_obj.count
                event_type_name = event_obj.event_type.name

                event_type_counts = event_sums.get(event_type_name, {})
                event_sums[event_type_name] = event_type_counts

                event_type_time_count = event_type_counts.get(window_name, 0)
                event_type_counts[window_name] = event_type_time_count

                event_sums[event_type_name][window_name] += count
        return event_sums
