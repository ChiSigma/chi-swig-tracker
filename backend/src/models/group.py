import drinker
import event
import event_type
import ephemeral_membership
import model
import src.auth.group_auth_mixin as group_auth
from orator.orm import has_many, has_many_through, accessor


class Group(model.Model, group_auth.GroupAuthMixin):
    @staticmethod
    def sort_by_event(event_type=None, time=None, order=None, in_scope=None):
        in_scope_group_ids = Group.in_scope().lists('id') if in_scope is None else in_scope
        sorted_group_ids = event.Event \
                                    .join('drinkers', 'events.drinker_id', '=', 'drinkers.id') \
                                    .join('groups', 'drinkers.primary_group_id', '=', 'groups.id') \
                                    .raw(raw_statement='count(*) as count, groups.id') \
                                    .where('events.event_type_id', '=', event_type) \
                                    .where_in('groups.id', in_scope_group_ids) \
                                    .created_within(time=time) \
                                    .group_by('groups.id') \
                                    .order_by('count', order) \
                                    .get().map(lambda e: e.id)
        if order == 'DESC':
            append_table = in_scope_group_ids
            base_table = sorted_group_ids
        else:
            append_table = sorted_group_ids
            base_table = in_scope_group_ids

        return list(base_table) + [group_id for group_id in append_table if group_id not in base_table]

    @staticmethod
    def filter(scope, **kwargs):
        if kwargs.get('ids', []) or kwargs('group_ids', []):
            group_ids = set().union(kwargs.get('ids', []), kwargs.get('group_ids', []))
            in_scope_ids = set(scope.lists('id'))
            filtered_ids = list(in_scope_ids.intersection(group_ids))
            scope = Group.where_in('groups.id', filtered_ids)
        return scope

    @has_many('primary_group_id')
    def primary_drinkers(self):
        return drinker.Drinker.with_('events')

    @has_many
    def ephemeral_memberships(self):
        return ephemeral_membership.EphemeralMembership.with_('drinker')

    @accessor
    def ephemeral_drinkers(self):
        return self.ephemeral_memberships.pluck('drinker')

    @accessor
    def profile_photo(self):
        profile_url = self.get_raw_attribute('profile_photo')
        if profile_url == 'default.png':
            profile_url = 'https://ui-avatars.com/api/?name={0}&background=B70000&color=fff&size=200&letters=3&uppercase=false'.format(self.name.replace(' ', '+'))
        return profile_url

    def event_counts(self):
        event_sums = {e_type.name: {window[0]: 0 for window in event_type.EventType.COUNT_WINDOWS} for e_type in event_type.EventType.all()}
        for window in event_type.EventType.COUNT_WINDOWS:
            window_name = window[0]
            time = window[1]
            events_in_window = event.Event \
                                            .raw(raw_statement='count(*) as count, event_type_id') \
                                            .where_in('drinker_id', self.primary_drinkers.pluck('id')) \
                                            .created_within(time=time) \
                                            .group_by('event_type_id')

            for event_obj in events_in_window.with_('event_type').get():
                count = event_obj.count
                event_type_name = event_obj.event_type.name

                event_sums[event_type_name][window_name] += count
        return event_sums