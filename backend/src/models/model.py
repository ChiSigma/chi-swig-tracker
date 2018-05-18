import datetime
from src.app import db
from orator.orm import scope

class Model(db.Model):
    @scope
    def created_within(self, query, time=None):
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

        return query.where('created_at', '>', now - delta)

    @scope
    def last(self, query):
        return query.order_by('created_at', 'desc').limit(1).first()

    @scope
    def raw(self, query, raw_statement=None):
        if raw_statement is None:
            return query

        return query.select(db.raw(raw_statement))

