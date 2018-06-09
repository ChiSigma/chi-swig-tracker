from src.app import db
from src.models import primary_membership


class GroupConcerns(object):
    def delete(self):
        self.__fix_orphaned_drinkers()
        return super(GroupConcerns, self).delete()

    def __fix_orphaned_drinkers(self):
        orphaned_drinkers = db.table('memberships').where('group_id', '=', self.id).where('type', '=', 'primary').lists('drinker_id')

        for drinker in orphaned_drinkers:
            db.table('memberships').insert({"drinker_id": drinker, "type": "primary", "group_id": 1, "admin": False})
