from orator.seeds import Seeder


class AddCannabisEvent(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('event_types').insert({
            'name': 'Smoked',
            'icon': 'cannabis'
        })
