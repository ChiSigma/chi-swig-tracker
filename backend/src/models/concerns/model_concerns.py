from src.app import db


class ModelConcerns(object):
    @classmethod
    def create(cls, _attributes=None, _unsafe=False, **attributes):
        if (_unsafe): return super(ModelConcerns, cls).create(_attributes, **attributes)

        with db.transaction():
            return super(ModelConcerns, cls).create(_attributes, **attributes)

    def update(self, _attributes=None, _unsafe=False, **attributes):
        if (_unsafe): return super(ModelConcerns, self).update(_attributes, **attributes)

        with db.transaction():
            return super(ModelConcerns, self).update(_attributes, **attributes)

    def delete(self, _unsafe=False):
        if (_unsafe): return super(ModelConcerns, self).delete()

        with db.transaction():
            return super(ModelConcerns, self).delete()