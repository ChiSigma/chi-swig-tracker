from orator.seeds import Seeder


class MembershipsSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('memberships').delete()

        self.db.table('memberships').insert({
            'drinker_id': 2,
            'group_id': 2,
            'type': 'primary',
            'admin': True
        })

        self.db.table('memberships').insert({
            'drinker_id': 2,
            'group_id': 1,
            'type': 'ephemeral'
        })

        self.db.table('memberships').insert({
            'drinker_id': 1,
            'group_id': 2,
            'type': 'primary'
        })

        self.db.table('memberships').insert({
            'drinker_id': 3,
            'group_id': 2,
            'type': 'primary'
        })

        self.db.table('memberships').insert({
            'drinker_id': 4,
            'group_id': 2,
            'type': 'primary'
        })

        self.db.table('memberships').insert({
            'drinker_id': 5,
            'group_id': 2,
            'type': 'primary'
        })

        self.db.table('memberships').insert({
            'drinker_id': 6,
            'group_id': 2,
            'type': 'primary'
        })

