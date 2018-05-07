from orator.seeds import Seeder


class DrinkersTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('drinkers').insert({
            'name': 'Melons',
            'profile_photo': 'http://example.com',
            'is_public': True
        })

        self.db.table('drinkers').insert({
            'name': 'JNorth',
            'profile_photo': 'http://example.com',
            'is_public': True
        })

        self.db.table('drinkers').insert({
            'name': 'Rag',
            'profile_photo': 'http://example.com',
            'is_public': False
        })

        self.db.table('drinkers').insert({
            'name': 'Zaddy',
            'profile_photo': 'http://example.com',
            'is_public': True
        })

        self.db.table('drinkers').insert({
            'name': 'Rock Man',
            'profile_photo': 'http://example.com',
            'is_public': True
        })

        self.db.table('drinkers').insert({
            'name': 'Eel-i',
            'profile_photo': 'http://example.com',
            'is_public': True
        })
