from flask import request
from flask_login import current_user
from src.app import db
from orator.orm import scope
from src.support.exceptions import OrphanException, InvalidRequestException, ForbiddenAccessException

class MembershipAuthMixin(object):
    table_name = 'memberships'

    @scope
    def in_admin_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query
        current_drinker_id = current_user.id if not current_user.is_anonymous else 0
        current_group_ids = db.table(MembershipAuthMixin.table_name) \
                                                                    .where('drinker_id', '=', current_drinker_id) \
                                                                    .lists('group_id')
        group_admins_ids = list(db.table(MembershipAuthMixin.table_name) \
                                                                    .where_in('group_id', current_group_ids) \
                                                                    .where('admin', '=', True) \
                                                                    .lists('drinker_id'))
        return base_query.where_in('drinker_id', group_admins_ids + [current_drinker_id])

    @classmethod
    def create(cls, _attributes=None, **attributes):
        cls.__undeclared_ephemeral_concern(None, attributes)
        cls.__admin_primary_only_concern(None, attributes)
        cls.__single_primary_only_concern(None, attributes)

        if request and not current_user.is_anonymous:
            self.__admin_to_create_admin(self, attributes)
            current_user_id = current_user.id
            drinker_id = attributes['drinker_id']
            group_id = attributes['group_id']
            membership_type = attributes['type']

            is_drinker_initiated = drinker_id == current_user_id
            if is_drinker_initiated:
                self.__check_group_privacy_concern(group_id, membership_type)
            else:
                self.__check_drinker_privacy_concern(drinker_id, membership_type)

        return super(MembershipAuthMixin, cls).create(_attributes, **attributes)

    def update(self, _attributes=None, **attributes):
        self.__undeclared_ephemeral_concern(self, attributes)
        self.__admin_primary_only_concern(self, attributes)
        self.__single_primary_only_concern(self, attributes)

        if request:
            self.__admin_to_create_admin(self, attributes)
            current_user_id = current_user.id
            drinker_id = attributes.get('drinker_id', self.drinker_id)
            group_id = attributes.get('group_id', self.group_id)
            membership_type = attributes.get('type', self.type)

            is_drinker_initiated = drinker_id == current_user_id
            has_changed = (drinker_id != self.drinker_id) or (group_id != self.group_id) or (membership_type != self.type)
            if is_drinker_initiated and has_changed:
                self.__check_group_privacy_concern(group_id, membership_type)
            elif has_changed:
                self.__check_drinker_privacy_concern(drinker_id, membership_type)

        return super(MembershipAuthMixin, self).update(_attributes, **attributes)

    def delete(self):
        if self.group_id == 1 and self.type == 'primary': raise OrphanException('Drinker {0}'.format(self.drinker_id))
        self.__fix_orphaned_drinker()

        return super(MembershipAuthMixin, self).delete()

    def __fix_orphaned_drinker(self):
        from src.models import PrimaryMembership
        is_orphaned = self.type == 'primary'

        if is_orphaned: PrimaryMembership.create(_unsafe=True, drinker_id=self.drinker_id, group_id=1)

    @classmethod
    def __check_if_privacy_violation(membership_policy, membership_type):
        if membership_policy == 'open':
            return False
        elif membership_policy == 'private':
            return True
        elif membership_policy == 'primary':
            return not membership_type == 'primary'
        elif membership_policy == 'ephemeral':
            return not membership_type == 'ephemeral'
        else:
            raise InvalidRequestException('Unknown membership_policy: {0}'.format(membership_policy))

    @staticmethod
    def __check_group_privacy_concern(group_id, membership_type):
        group_membership_policy = db.table('groups').where('id', '=', group_id).first().get('membership_policy', 'private')
        if MembershipAuthMixin.__check_if_privacy_violation(group_membership_policy, membership_type):
            raise ForbiddenAccessException('join group {0} as type {1}').format(group_id, membership_type)

    @staticmethod
    def __check_drinker_privacy_concern(drinker_id, membership_type):
        drinker_membership_policy = db.table('drinkers').where('id', '=', drinker_id).first().get('membership_policy', 'private')
        if MembershipAuthMixin.__check_if_privacy_violation(drinker_membership_policy, membership_type):
            raise ForbiddenAccessException('add drinker {0} as type {1}').format(drinker_id, membership_type)

    @staticmethod
    def __admin_to_create_admin(self, attributes):
        is_admin = False if current_user.is_anonymous else current_user.is_admin()
        group_id = attributes['group_id'] if 'group_id' in attributes else (self.group_id if self else None)
        is_creating_admin = attributes['admin'] if 'admin' in attributes else (self.admin if self else False)
        if is_creating_admin and not is_admin:
            raise ForbiddenAccessException('make an admin for group {0}'.format(group_id))

    @staticmethod
    def __undeclared_ephemeral_concern(self, attributes):
        membership_type = attributes['type'] if 'type' in attributes else (self.type if self else None)
        group_id = attributes['group_id'] if 'group_id' in attributes else (self.group_id if self else None)

        if membership_type == 'ephemeral' and int(group_id) == 1: raise InvalidRequestException('Cannot make Undeclared an ephemeral group')

    @staticmethod
    def __admin_primary_only_concern(self, attributes):
        membership_type = attributes['type'] if 'type' in attributes else (self.type if self else None)
        is_admin = attributes['admin'] if 'admin' in attributes else (self.admin if self else False)

        if membership_type != 'primary' and is_admin: raise InvalidRequestException('Cannot be admin for type: {0}'.format(membership_type))

    @staticmethod
    def __single_primary_only_concern(self, attributes):
        from src.models import PrimaryMembership
        membership_type = attributes['type'] if 'type' in attributes else (self.type if self else None)
        drinker_id = attributes['drinker_id'] if 'drinker_id' in attributes else (self.drinker_id if self else 0)
        group_id = attributes['group_id'] if 'group_id' in attributes else (self.group_id if self else None)

        if membership_type == 'primary':
            primary_groups = PrimaryMembership.where('drinker_id', '=', drinker_id)
            has_no_group = len(primary_groups) == 0
            primary_group_id = 0 if has_no_group else primary_groups[0].id

            if not (primary_group_id in [0, 1] or primary_group_id == group_id):
                raise InvalidRequestException('Cannot have more than 1 primary group')

            if primary_group_id == 1 and primary_group_id != group_id:
                # Need to delete the undeclared group first before making new membership
                primary_groups[0].delete(_unsafe=True)
