from orator.seeds import Seeder


class MembershipsSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('memberships').delete()
        all_ids = self.db.table('drinkers').lists('id')
        new_ids = list(set(all_ids) - set([1,2,3,4,5,6]))

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

        for new_id in new_ids:
            self.db.table('memberships').insert({
                'drinker_id': new_id,
                'group_id': 1,
                'type': 'primary',
                'admin': False
            })

