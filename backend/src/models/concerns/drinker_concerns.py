import model_concerns
from src.app import db
from src.models import primary_membership


class DrinkerConcerns(object):
    @classmethod
    def create(cls, _attributes=None, **attributes):
        drinker = super(DrinkerConcerns, cls).create(_attributes, **attributes)
        primary_membership.PrimaryMembership.create(_unsafe=True, drinker_id=drinker.id, group_id=1)
        return drinker
