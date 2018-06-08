from src.app import db
from orator.orm import scope

class ModelAuthMixin(object):
    __default_admin__ = ['id', 'created_at', 'updated_at']
    __admin__ = []
    __protect__ = []

    @scope
    def clean_query(self, query, table_name=None):
        ids = query.lists('id')
        return query._model.new_query().where_in('{0}.id'.format(table_name), ids)

    @classmethod
    def admin_readable(cls):
        return cls.__admin__ + cls.__default_admin__

    @classmethod
    def admin_writable(cls):
        return list(set(cls.__admin__) - set(cls.__protect__))
