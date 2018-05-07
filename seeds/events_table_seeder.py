from orator.seeds import Seeder


class EventsTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """

        drinkers = self.db.table('drinkers').get()
        event_types = self.db.table('event_types').get()

        for d in range(1, 7):
            for event_type in event_types:
                self.db.table('events').insert({
                        'drinker_id': d,
                        'event_type_id': event_type['id']
                    })

        for d in [1,3,5]:
            for event_type in event_types:
                self.db.table('events').insert({
                        'drinker_id': d,
                        'event_type_id': event_type['id']
                    })

        for event_type in event_types:
            self.db.table('events').insert({
                    'drinker_id': 1,
                    'event_type_id': event_type['id']
                })
