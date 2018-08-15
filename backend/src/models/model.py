import datetime
import hashlib
from src.support.exceptions import InvalidRequestException
from src.serializers import ModelSerializer
from src.app import db
from orator.orm import scope


class Model(ModelSerializer, db.Model):
    __default_public__ = ['id', 'created_at', 'updated_at']
    __public__ = []

    @classmethod
    def public_readable(cls):
        return cls.__public__ + cls.__default_public__ + cls.__appends__

    @staticmethod
    def normalization_factor(time=None, created_at=None):
        now = datetime.datetime.utcnow()
        time_ago = now - Model.parse_time_delta(time) if time and not '*' in time else None
        time_factor = (now - time_ago).total_seconds() if time_ago else None
        created_at_factor = (now - created_at).total_seconds() if created_at else None

        if not time_factor and not created_at_factor:
            raise InvalidRequestException("Incorrect params passed to normalization_factor")
        elif time_factor and not created_at_factor:
            return time_factor
        elif created_at_factor and not time_factor:
            return created_at_factor
        else:
            return min(time_factor, created_at_factor)

    @staticmethod
    def normalized_sort(models, time=None, order=None):
        def normalized_comparison_factor(model):
            return float(model.count / Model.normalization_factor(time=time, created_at=model.created_at) / model.n)

        reverse = True if order == 'DESC' else False
        return sorted(models, key=normalized_comparison_factor, reverse=reverse)

    @scope
    def created_within(self, query, time=None, table_name=''):
        if '*' in time or time is None:
            return query

        delta = Model.parse_time_delta(time)
        now = datetime.datetime.utcnow()
        return query.where('{0}created_at'.format(table_name), '>', now - delta)

    @staticmethod
    def transaction():
        return db.transaction()

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

    @staticmethod
    def parse_time_delta(time_string):
        time_ago = time_string.lower()
        time_ago_parsed = ''.join([d for d in time_ago if d.isdigit()])

        if time_ago_parsed == '':
            raise InvalidRequestException("Unknown time format: {0} passed to parse_time!".format(time_ago))

        time_ago_int = int(time_ago_parsed)
        if 'd' in time_ago:
            delta = datetime.timedelta(days=time_ago_int)
        elif 'h' in time_ago:
            delta = datetime.timedelta(hours=time_ago_int)
        elif 'm' in time_ago:
            delta = datetime.timedelta(minutes=time_ago_int)
        else:
            raise InvalidRequestException("Unknown time format: {0} passed to parse_time!".format(time_ago))
        return delta
