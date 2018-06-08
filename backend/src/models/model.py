import datetime
import hashlib
from src.serializers import ModelSerializer
from src.app import db
from orator.orm import scope


class Model(db.Model, ModelSerializer):
    __default_public__ = ['id', 'created_at', 'updated_at']
    __public__ = []

    @classmethod
    def public_readable(cls):
        return cls.__public__ + cls.__default_public__ + cls.__appends__

    @scope
    def created_within(self, query, time=None, table_name=''):
        time_ago = time.lower()

        if '*' in time_ago or time_ago is None:
            return query

        time_ago_parsed = ''.join([d for d in time_ago if d.isdigit()])

        if time_ago_parsed == '':
            raise "Unknown time format: {0} passed to parse_time!".format(time_ago)

        time_ago_int = int(time_ago_parsed)
        now = datetime.datetime.utcnow()

        if 'd' in time_ago:
            delta = datetime.timedelta(days=time_ago_int)
        elif 'h' in time_ago:
            delta = datetime.timedelta(hours=time_ago_int)
        elif 'm' in time_ago:
            delta = datetime.timedelta(minutes=time_ago_int)
        else:
            raise "Unknown time format: {0} passed to parse_time!".format(time_ago)

        return query.where('{0}created_at'.format(table_name), '>', now - delta)

    @staticmethod
    def transaction():
        return db.transaction()

    @classmethod
    def create(cls, _attributes=None, **attributes):
        with db.transaction():
            return super(Model, cls).create(_attributes, **attributes)

    @classmethod
    def unsafe_create(cls, _attributes=None, **attributes):
        return super(Model, cls).create(_attributes, **attributes)

    def update(self, _attributes=None, **attributes):
        with db.transaction():
            return super(Model, self).update(_attributes, **attributes)

    def unsafe_update(self, _attributes=None, **attributes):
        return super(Model, self).update(_attributes, **attributes)

    def delete(self):
        with db.transaction():
            return super(Model, self).delete()

    def unsafe_delete(self):
        return super(Model, self).delete()

    @scope
    def last(self, query):
        return query.order_by('created_at', 'desc').limit(1).first()

    @scope
    def version(self, query):
        updated_times = query.order_by('id').get().lists('updated_at')
        return hashlib.md5(str([ut for ut in updated_times])).hexdigest()

    @scope
    def raw(self, query, raw_statement=None):
        if raw_statement is None:
            return query

        return query.select(db.raw(raw_statement))

