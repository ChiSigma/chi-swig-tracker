from flask_login import current_user
from src.app import db
from orator.orm import scope

class GroupAuthMixin(object):
    @scope
    def in_primary_scope(self, query, is_or=False):
        # if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query
        group_id = current_user.primary_group_id if not current_user.is_anonymous else 0
        return base_query.where('groups.id', '=', group_id)

    @scope
    def in_ephemeral_scope(self, query, is_or=False):
        # if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query
        ephemeral_ids = current_user.ephemeral_group_ids if not current_user.is_anonymous else []
        return base_query.where_in('groups.id', ephemeral_ids)

    @scope
    def in_member_scope(self, query, is_or=False):
        # if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query
        group_id = current_user.primary_group_id if not current_user.is_anonymous else 0
        ephemeral_ids = current_user.ephemeral_group_ids if not current_user.is_anonymous else []

        return base_query.where(db.query().where_in('groups.id', ephemeral_ids)) \
                                                                    .or_where(db.query().where('groups.id', '=', group_id))

    @scope
    def in_scope(self, query, is_or=False):
        # if not current_user.is_anonymous and current_user.superuser: return query

        base_query = db.query() if is_or else query
        group_id = current_user.primary_group_id if not current_user.is_anonymous else 0
        ephemeral_ids = current_user.ephemeral_group_ids if not current_user.is_anonymous else []

        return base_query.where('groups.privacy_setting', '!=', 'unlisted') \
                                                                    .or_where(db.query().where_in('groups.id', ephemeral_ids)) \
                                                                    .or_where(db.query().where('groups.id', '=', group_id))
