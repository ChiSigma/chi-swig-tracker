from src.app import db


class ModelConcerns(object):
    @classmethod
    def create(cls, _attributes=None, _unsafe=False, **attributes):
        temp_attributes = attributes.copy()
        temp_attributes.update(_attributes if _attributes else {})

        if (_unsafe): return super(ModelConcerns, cls).create(temp_attributes, **attributes)

        with db.transaction():
            return super(ModelConcerns, cls).create(temp_attributes, **attributes)

    def update(self, _attributes=None, _unsafe=False, **attributes):
        temp_attributes = attributes.copy()
        temp_attributes.update(_attributes if _attributes else {})

        if (_unsafe): return super(ModelConcerns, self).update(temp_attributes, **attributes)

        with db.transaction():
            return super(ModelConcerns, self).update(temp_attributes, **attributes)

    def delete(self, _unsafe=False):
        if (_unsafe): return super(ModelConcerns, self).delete()

        with db.transaction():
            return super(ModelConcerns, self).delete()
