import model
import event
import event_type
import hashlib
from src.app import lm
from flask_login import UserMixin
from orator.orm import has_many, accessor

class Drinker(UserMixin, model.Model):
    __fillable__ = ['is_public', 'bio_line', 'num_days_dry', 'profile_pivot_increment', 'profile_pivot_type', 'profile_photos']
    __hidden__   = ['events', 'profile_pivot_increment', 'profile_pivot_type', 'profile_photos']
    __appends__  = ['profile_photo']
    # (Name for the frontend, window for querying the db)
    COUNT_WINDOWS = [('Past Day', '24h'), ('Past Week', '7d'), ('All Time', '*')]

    @staticmethod
    def sort_by_event(event_type=None, time=None, order=None):
        sorted_drinker_ids = event.Event \
                                    .raw(raw_statement='count(*) as count, drinker_id') \
                                    .where('event_type_id', '=', event_type) \
                                    .created_within(time=time) \
                                    .group_by('drinker_id') \
                                    .order_by('count', order)

        return sorted_drinker_ids.with_('drinker').get().map(lambda e: e.drinker)

    @staticmethod
    def version():
        updated_times = Drinker.order_by('id').get().pluck('updated_at')
        return hashlib.md5(str([ut for ut in updated_times])).hexdigest()

    @lm.user_loader
    def load_user(id):
        return Drinker.find(id)

    @has_many
    def events(self):
        return event.Event

    @accessor
    def profile_photos(self):
        return self.get_raw_attribute('profile_photos').split(',')

    @accessor
    def profile_photo(self):
        event_count = self.events() \
                                    .where('event_type_id', '=', self.profile_pivot_type) \
                                    .created_within(time='24h') \
                                    .count()
        photo_index = min(int(event_count / self.profile_pivot_increment), len(self.profile_photos) - 1)

        return self.profile_photos[photo_index]

    def is_dry(self):
        return self.events().created_within(time='24h').count() == 0

    def event_counts(self):
        event_sums = {e_type.name: {window[0]: 0 for window in self.COUNT_WINDOWS} for e_type in event_type.EventType.all()}
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

                event_sums[event_type_name][window_name] += count
        return event_sums
