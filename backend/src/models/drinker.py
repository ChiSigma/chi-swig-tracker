import model
import event
import group
import event_type
import ephemeral_membership
import primary_membership
import membership
import src.auth.drinker_auth_mixin as drinker_auth
from src.app import lm
from flask_login import UserMixin
from orator.orm import has_many, has_one, accessor

class Drinker(UserMixin, drinker_auth.DrinkerAuthMixin, model.Model):
    __fillable__ = ['name', 'email', 'is_public', 'bio_line', 'num_days_dry', 'profile_pivot_increment', 'profile_pivot_type', 'profile_photos', 'max_days_dry']
    __hidden__   = ['events', 'profile_pivot_increment', 'profile_pivot_type', 'profile_photos', 'email', 'primary_membership']
    __touches__  = ['primary_group']
    __appends__  = ['profile_photo', 'primary_group', 'groups_can_edit']

    @staticmethod
    def sort_by_event(event_type=None, time=None, order=None, in_scope=None):
        # Default this to all in scope with current auth user
        in_scope_drinker_ids = Drinker.in_scope().lists('id') if in_scope is None else in_scope.lists('id')
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

        return list(base_table) + [drinker_id for drinker_id in append_table if drinker_id not in base_table]

    @staticmethod
    def filter(scope, **kwargs):
        if kwargs.get('ids', []) or kwargs.get('drinker_ids', []):
            drinker_ids = set().union(kwargs.get('ids', []), kwargs.get('drinker_ids', []))
            in_scope_ids = set(scope.lists('id'))
            filtered_ids = list(in_scope_ids.intersection(drinker_ids))
            scope = Drinker.where_in('drinkers.id', filtered_ids)

        if kwargs.get('group_ids', []):
            group_ids = kwargs.get('group_ids', [])
            in_scope_drinker_ids = scope.lists('id')
            drinker_ids = membership.Membership.where_in('group_id', group_ids).where_in('drinker_id', in_scope_drinker_ids).lists('drinker_id')
            filtered_ids = list(set(drinker_ids).intersection(in_scope_drinker_ids))
            scope = Drinker.where_in('drinkers.id', filtered_ids)

        return scope

    @lm.user_loader
    def load_user(id):
        return Drinker.find(id)

    @has_many
    def events(self):
        return event.Event

    @has_one
    def primary_membership(self):
        return primary_membership.PrimaryMembership

    @has_many
    def ephemeral_memberships(self):
        return ephemeral_membership.EphemeralMembership

    @accessor
    def ephemeral_groups(self):
        return self.ephemeral_memberships.pluck('group')

    @accessor
    def primary_group(self):
        return self.primary_membership.group if self.primary_membership else {}

    @accessor
    def groups_can_edit(self):
        return [self.primary_membership.group.id] + list(self.ephemeral_groups.pluck('id'))

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
