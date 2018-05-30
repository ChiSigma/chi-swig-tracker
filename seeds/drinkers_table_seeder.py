from orator.seeds import Seeder


class DrinkersTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('drinkers').insert({
            'name': 'Melons',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'email': 'melons@example.com'
        })

        self.db.table('drinkers').insert({
            'name': 'JNorth',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'email': 'jnorth@example.com'
        })

        self.db.table('drinkers').insert({
            'name': 'Rag',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'email': 'rag@example.com'
        })

        self.db.table('drinkers').insert({
            'name': 'Zaddy',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'email': 'zaddy@example.com'
        })

        self.db.table('drinkers').insert({
            'name': 'Rock Man',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'email': 'rockman@example.com'
        })

        self.db.table('drinkers').insert({
            'name': 'Eel-i',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'email': 'eeli@example.com'
        })
