import drinker
import group
from orator import Model
from orator.orm import belongs_to


class EphemeralMembership(Model):
    __table__ = 'drinkers_ephemeral_groups'
    
    @belongs_to
    def drinker(self):
        return drinker.Drinker

    @belongs_to
    def group(self):
        return group.Group
