import src.support.sti_scope as sti_scope
from concerns import model_concerns
from orator import Model
from orator.orm import belongs_to
from src.auth import MembershipAuthMixin


class Membership(model_concerns.ModelConcerns, MembershipAuthMixin, Model):
    __fillable__  = ['drinker_id', 'group_id', 'type', 'admin']
    __table__     = 'memberships'
    __sti_type__  = None
    __timestamps__ = False

    @classmethod
    def _boot(cls):
        cls.add_global_scope(sti_scope.STIScope())
        super(Membership, cls)._boot()

    @classmethod
    def create(cls, _attributes=None, **attributes):
        attributes['type'] = cls.__sti_type__
        super(Membership, cls).create(_attributes, **attributes)
    
    @belongs_to
    def drinker(self):
        from drinker import Drinker
        return Drinker

    @belongs_to
    def group(self):
        from group import Group
        return Group
