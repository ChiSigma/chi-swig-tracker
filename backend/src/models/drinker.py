import model
import event
import group
import event_type
from src.app import lm
from flask_login import UserMixin
from orator.orm import has_many, accessor, belongs_to, belongs_to_many

class Drinker(UserMixin, model.Model):
    __fillable__ = ['is_public', 'bio_line', 'num_days_dry', 'profile_pivot_increment', 'profile_pivot_type', 'profile_photos', 'max_days_dry']
    __hidden__   = ['events', 'profile_pivot_increment', 'profile_pivot_type', 'profile_photos', 'email', 'ephemeral_groups']
    __touches__  = ['primary_group']
    __appends__  = ['profile_photo', 'ephemeral_group_ids']

    @staticmethod
    def sort_by_event(event_type=None, time=None, order=None, in_scope=None):
        # Default this to all in scope with current auth user
        in_scope_drinker_ids = Drinker.all().pluck('id') if in_scope is None else in_scope
        sorted_drinker_ids = event.Event \
                                    .raw(raw_statement='count(*) as count, drinker_id') \
                                    .where('event_type_id', '=', event_type) \
                                    .where_in('drinker_id', in_scope_drinker_ids) \
                                    .created_within(time=time) \
                                    .group_by('drinker_id') \
                                    .order_by('count', order) \
                                    .get().map(lambda e: e.drinker_id)
        if order == 'DESC':
            append_table = in_scope_drinker_ids
            base_table = sorted_drinker_ids
        else:
            append_table = sorted_drinker_ids
            base_table = in_scope_drinker_ids

        return list(base_table) + [group_id for group_id in append_table if group_id not in base_table]

    @lm.user_loader
    def load_user(id):
        return Drinker.find(id)

    @has_many
    def events(self):
        return event.Event

    @belongs_to('primary_group_id')
    def primary_group(self):
        return group.Group

    @belongs_to_many('drinkers_ephemeral_groups')
    def ephemeral_groups(self):
        return group.Group

    @accessor
    def ephemeral_group_ids(self):
        return list(self.ephemeral_groups.pluck('id'))

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
        photo_url = self.profile_photos[photo_index]

        if photo_url == 'default.png':
            photo_url = "https://api.adorable.io/avatars/200/{0}.png".format(self.id)
        return photo_url

    def is_dry(self):
        return self.events().where('event_type_id', '=', 1).created_within(time='24h').count() == 0

    def event_counts(self):
        event_sums = {e_type.name: {window[0]: 0 for window in event_type.EventType.COUNT_WINDOWS} for e_type in event_type.EventType.all()}
        for window in event_type.EventType.COUNT_WINDOWS:
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
