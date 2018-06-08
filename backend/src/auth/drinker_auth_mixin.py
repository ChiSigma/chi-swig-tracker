import model_auth_mixin as model_auth
from flask_login import current_user
from src.app import db
from orator.orm import scope

class DrinkerAuthMixin(model_auth.ModelAuthMixin):
    table_name = 'drinkers'

    @scope
    def in_admin_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query.clean_query(table_name=DrinkerAuthMixin.table_name)
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        return base_query.where('drinkers.id', '=', drinker_id)

    @scope
    def in_primary_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query.clean_query(table_name=DrinkerAuthMixin.table_name)
        primary_group = current_user.primary_group if (not current_user.is_anonymous) and current_user.primary_group.id != 1 else None
        primary_drinker_ids = list(primary_group.primary_drinkers.lists('id')) if primary_group is not None else []
        drinker_id = current_user.id if not current_user.is_anonymous else 0

        return base_query.where_in('drinkers.id', primary_drinker_ids + [drinker_id])

    @scope
    def in_ephemeral_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query
        
        base_query = db.query() if is_or else query.clean_query(table_name=DrinkerAuthMixin.table_name)
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        ephemeral_ids = list(current_user.ephemeral_groups.lists('id')) if not current_user.is_anonymous else []
        ephemeral_drinkers = list(db.table('memberships').where_in('group_id', ephemeral_ids).where('type', '=', 'ephemeral').lists('drinker_id')) + [drinker_id]

        return base_query.where_in('drinkers.id', ephemeral_drinkers)

    @scope
    def in_member_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query.clean_query(table_name=DrinkerAuthMixin.table_name)
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        group_ids = list(db.table('memberships').where('drinker_id', '=', drinker_id).lists('group_id'))
        group_drinkers = list(db.table('memberships').where_in('group_id', group_ids).lists('drinker_id')) + [drinker_id]

        return base_query.where_in('drinkers.id', group_drinkers)

    @scope
    def in_scope(self, query, is_or=False):
        if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query.clean_query(table_name=DrinkerAuthMixin.table_name)
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        group_ids = list(db.table('memberships').where('drinker_id', '=', drinker_id).lists('group_id'))
        group_drinkers = list(db.table('memberships').where_in('group_id', group_ids).lists('drinker_id')) + [drinker_id]

        return base_query.where(db.query().where('drinkers.privacy_setting', '!=', 'unlisted').or_where(db.query().where_in('drinkers.id', group_drinkers)))