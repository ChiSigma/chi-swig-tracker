from src.app import db
from orator.orm import scope

class ModelAuthMixin(object):
    @scope
    def clean_query(self, query, table_name=None):
        ids = query.lists('id')
        return query._model.new_query().where_in('{0}.id'.format(table_name), ids)