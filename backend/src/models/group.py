import drinker
import event
import event_type
import ephemeral_membership
import primary_membership
import model
import src.auth.group_auth_mixin as group_auth
from orator.orm import has_many, has_many_through, accessor


class Group(model.Model, group_auth.GroupAuthMixin):
    __hidden__ = ['primary_drinkers', 'primary_memberships', 'ephemeral_memberships', 'ephemeral_drinkers']
    __appends__ = ['num_days_dry', 'max_days_dry']

    @staticmethod
    def sort_by_event(event_type=None, time=None, order=None, in_scope=None):
        in_scope_group_ids = Group.in_scope().lists('id') if in_scope is None else in_scope.lists('id')
        sorted_group_ids = event.Event \
                                    .join('memberships', 'events.drinker_id', '=', 'memberships.drinker_id') \
                                    .where('memberships.type', '=', 'primary') \
                                    .raw(raw_statement='count(*) as count, memberships.group_id as group_id') \
                                    .where('events.event_type_id', '=', event_type) \
                                    .where_in('group_id', in_scope_group_ids) \
                                    .created_within(time=time, table_name='events.') \
                                    .group_by('group_id') \
                                    .order_by('count', order) \
                                    .get().map(lambda e: e.group_id)
        if order == 'DESC':
            append_table = in_scope_group_ids
            base_table = sorted_group_ids
        else:
            append_table = sorted_group_ids
            base_table = in_scope_group_ids

        return list(base_table) + [group_id for group_id in append_table if group_id not in base_table]

    @staticmethod
    def filter(scope, **kwargs):
        if kwargs.get('ids', []) or kwargs.get('group_ids', []):
            group_ids = set().union(kwargs.get('ids', []), kwargs.get('group_ids', []))
            in_scope_ids = set(scope.lists('id'))
            filtered_ids = list(in_scope_ids.intersection(group_ids))
            scope = Group.where_in('groups.id', filtered_ids)
        return scope

    @has_many('drinker_id')
    def primary_memberships(self):
        return primary_membership.PrimaryMembership

    @has_many('drinker_id')
    def ephemeral_memberships(self):
        return ephemeral_membership.EphemeralMembership

    @accessor
    def primary_drinkers(self):
        return self.primary_memberships.pluck('drinker')

    @accessor
    def ephemeral_drinkers(self):
        return self.ephemeral_memberships.pluck('drinker')

    @accessor
    def max_days_dry(self):
        drinkers = sorted(self.primary_drinkers, reverse=True, key=lambda d: d.max_days_dry)
        return drinkers[0].max_days_dry if len(drinkers) > 0 else 0

    @accessor
    def num_days_dry(self):
        return self.primary_drinkers.avg('num_days_dry')

    @accessor
    def profile_photo(self):
        profile_url = self.get_raw_attribute('profile_photo')
        if profile_url == 'default.png':
            profile_url = 'https://ui-avatars.com/api/?name={0}&background=B70000&color=fff&size=200&letters=3&uppercase=false'.format(self.name.replace(' ', '+'))
        return profile_url
