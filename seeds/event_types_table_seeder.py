from orator.seeds import Seeder


class EventTypesTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('event_types').insert({
            'name': 'Drank',
            'icon': 'beer'
        })

        self.db.table('event_types').insert({
            'name': 'Puked',
            'icon': 'trash'
        })

        self.db.table('event_types').insert({
            'name': 'Blacked Out',
            'icon': 'calendar-times'
        })

        self.db.table('event_types').insert({
            'name': 'Cleaned',
            'icon': 'broom'
        })

        self.db.table('event_types').insert({
            'name': 'Cooked',
            'icon': 'utensils'
        })

