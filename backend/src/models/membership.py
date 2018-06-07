import src.support.sti_scope as sti_scope
from orator import Model
from orator.orm import belongs_to


class Membership(Model):
    __table__     = 'memberships'
    __sti_type__  = None

    @classmethod
    def _boot(cls):
        cls.add_global_scope(sti_scope.STIScope())
        super(Membership, cls)._boot()
    
    @belongs_to
    def drinker(self):
        from drinker import Drinker
        return Drinker

    @belongs_to
    def group(self):
        from group import Group
        return Group
