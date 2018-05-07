from orator.seeds import Seeder


class EventTypesTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('event_types').insert({
            'name': 'Drank',
            'icon': 'http://example.com'
        })

        self.db.table('event_types').insert({
            'name': 'Puked',
            'icon': 'http://example.com'
        })

        self.db.table('event_types').insert({
            'name': 'Blacked Out',
            'icon': 'http://example.com'
        })

        self.db.table('event_types').insert({
            'name': 'Cleaned',
            'icon': 'http://example.com'
        })

        self.db.table('event_types').insert({
            'name': 'Cooked',
            'icon': 'http://example.com'
        })

