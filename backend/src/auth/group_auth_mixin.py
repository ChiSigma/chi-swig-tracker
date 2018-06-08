import model_auth_mixin as model_auth
from flask_login import current_user
from src.app import db
from orator.orm import scope

class GroupAuthMixin(model_auth.ModelAuthMixin):
    table_name = 'groups'

    @scope
    def in_admin_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query.clean_query(table_name=GroupAuthMixin.table_name)
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        group_ids = db.table('memberships').where('drinker_id', '=', drinker_id).where('admin', '=', True).lists('group_id')

        return base_query.where_in('groups.id', group_ids)

    @scope
    def in_primary_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query.clean_query(table_name=GroupAuthMixin.table_name)
        group_id = current_user.primary_group.id if not current_user.is_anonymous else 0
        return base_query.where('groups.id', '=', group_id)

    @scope
    def in_ephemeral_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query.clean_query(table_name=GroupAuthMixin.table_name)
        ephemeral_ids = current_user.ephemeral_groups.lists('id') if not current_user.is_anonymous else []
        return base_query.where_in('groups.id', ephemeral_ids)

    @scope
    def in_member_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query.clean_query(table_name=GroupAuthMixin.table_name)
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        group_ids = db.table('memberships').where('drinker_id', '=', drinker_id).lists('group_id')

        return base_query.where_in('groups.id', group_ids)

    @scope
    def in_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query.clean_query(table_name=GroupAuthMixin.table_name)
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        group_ids = db.table('memberships').where('drinker_id', '=', drinker_id).lists('group_id')

        return base_query.where(db.query().where('groups.privacy_setting', '!=', 'unlisted') \
                                                                    .or_where(db.query().where_in('groups.id', group_ids)))
