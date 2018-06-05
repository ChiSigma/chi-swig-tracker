import model_auth_mixin as model_auth
from flask_login import current_user
from src.app import db
from orator.orm import scope

class EventAuthMixin(model_auth.ModelAuthMixin):
    table_name = 'events'

    @scope
    def in_primary_scope(self, query, is_or=False):
        # if not current_user.is_anonymous and current_user.superuser: return query

        base_query = (db.query() if is_or else query.clean_query(table_name=EventAuthMixin.table_name)).join('drinkers', 'events.drinker_id', '=', 'drinkers.id')
        group_id = current_user.primary_group_id if (not current_user.is_anonymous) and current_user.primary_group_id != 1 else 0
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        event_scope = base_query.select('events.id', 'drinker_id').where(db.query().where('drinkers.primary_group_id', '=', group_id) \
                                                                                    .or_where(db.query().where('drinkers.id', '=', drinker_id)))
        if is_or:
            return event_scope
        else:
            return event_scope.clean_query(table_name=EventAuthMixin.table_name)

    @scope
    def in_ephemeral_scope(self, query, is_or=False):
        # if not current_user.is_anonymous and current_user.superuser: return query
        
        base_query = (db.query() if is_or else query.clean_query(table_name=EventAuthMixin.table_name)).join('drinkers', 'events.drinker_id', '=', 'drinkers.id')
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        ephemeral_ids = current_user.ephemeral_group_ids if not current_user.is_anonymous else []
        ephemeral_drinkers = db.table('drinkers_ephemeral_groups').where_in('group_id', ephemeral_ids).lists('drinker_id') + [drinker_id]
        event_scope = base_query.select('events.id', 'drinker_id').where_in('drinkers.id', ephemeral_drinkers)

        if is_or:
            return event_scope
        else:
            return event_scope.clean_query(table_name=EventAuthMixin.table_name)

    @scope
    def in_member_scope(self, query, is_or=False):
        # if not current_user.is_anonymous and current_user.superuser: return query

        base_query = (db.query() if is_or else query.clean_query(table_name=EventAuthMixin.table_name)).join('drinkers', 'events.drinker_id', '=', 'drinkers.id')
        group_id = current_user.primary_group_id if (not current_user.is_anonymous) and current_user.primary_group_id != 1 else 0
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        ephemeral_ids = current_user.ephemeral_group_ids if not current_user.is_anonymous else []
        ephemeral_drinkers = db.table('drinkers_ephemeral_groups').where_in('group_id', ephemeral_ids).lists('drinker_id')

        event_scope = base_query.select('events.id', 'drinker_id').where(db.query().where_in('drinkers.id', ephemeral_drinkers) \
                                                                    .or_where(db.query().where('drinkers.primary_group_id', '=', group_id)) \
                                                                    .or_where(db.query().where('drinkers.id', '=', drinker_id)))
        if is_or:
            return event_scope
        else:
            return event_scope.clean_query(table_name=EventAuthMixin.table_name)

    @scope
    def in_scope(self, query, is_or=False):
        # if not current_user.is_anonymous and current_user.superuser: return query

        base_query = (db.query() if is_or else query.clean_query(table_name=EventAuthMixin.table_name)).join('drinkers', 'events.drinker_id', '=', 'drinkers.id')
        group_id = current_user.primary_group_id if (not current_user.is_anonymous) and current_user.primary_group_id != 1 else 0
        drinker_id = current_user.id if not current_user.is_anonymous else 0
        ephemeral_ids = current_user.ephemeral_group_ids if not current_user.is_anonymous else []
        ephemeral_drinkers = db.table('drinkers_ephemeral_groups').where_in('group_id', ephemeral_ids).lists('drinker_id')

        event_scope = base_query.select('events.id', 'drinker_id').where(db.query().where('drinkers.privacy_setting', '=', 'public') \
                                                                    .or_where(db.query().where_in('drinkers.id', ephemeral_drinkers)) \
                                                                    .or_where(db.query().where('drinkers.primary_group_id', '=', group_id)) \
                                                                    .or_where(db.query().where('drinkers.id', '=', drinker_id)))

        if is_or:
            return event_scope
        else:
            return event_scope.clean_query(table_name=EventAuthMixin.table_name)
