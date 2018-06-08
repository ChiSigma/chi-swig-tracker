import model_concerns
from src.app import db
from src.models import primary_membership

class GroupConcerns(object):
    def delete(self):
        self.__fix_orphaned_drinkers()
        return super(GroupConcerns, self).delete()

    def update(self, _attributes=None, **attributes):
        return super(GroupConcerns, self).update(_attributes, **attributes)

    def __fix_orphaned_drinkers(self):
        orphaned_drinkers = db.table('memberships').where('group_id', '=', self.id).where('type', '=', 'primary').lists('drinker_id')

        for drinker in orphaned_drinkers:
            primary_membership.PrimaryMembership.create(_unsafe=True, drinker_id=drinker, group_id=1)
