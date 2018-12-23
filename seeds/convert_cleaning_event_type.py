from orator.seeds import Seeder


class ConvertCleaningEventType(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('event_types').where('id', 4).update({
            'name': "mi's Run",
            'icon': 'running'
        })

        self.db.table('events').where('event_type_id', 4).delete()
