from orator.seeds import Seeder


class DrinkersTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('drinkers').insert({
            'name': 'Melons',
            'profile_photo': 'http://example.com',
            'is_public': True,
            'bio_line': 'My name is Melons!'
        })

        self.db.table('drinkers').insert({
            'name': 'JNorth',
            'profile_photo': 'http://example.com',
            'is_public': True,
            'bio_line': 'My name is JNorth!'
        })

        self.db.table('drinkers').insert({
            'name': 'Rag',
            'profile_photo': 'http://example.com',
            'is_public': False,
            'bio_line': 'My name is Rag!'
        })

        self.db.table('drinkers').insert({
            'name': 'Zaddy',
            'profile_photo': 'http://example.com',
            'is_public': True,
            'bio_line': 'My name is Zaddy!'
        })

        self.db.table('drinkers').insert({
            'name': 'Rock Man',
            'profile_photo': 'http://example.com',
            'is_public': True,
            'bio_line': 'My name is Rock Man!'
        })

        self.db.table('drinkers').insert({
            'name': 'Eel-i',
            'profile_photo': 'http://example.com',
            'is_public': True,
            'bio_line': 'My name is Eel-i!'
        })
