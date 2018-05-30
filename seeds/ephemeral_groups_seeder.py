from orator.seeds import Seeder


class EphemeralGroupsSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('drinkers_ephemeral_groups').delete()

        self.db.table('drinkers_ephemeral_groups').insert({
            'drinker_id': 2,
            'group_id': 1
        })

