from orator.seeds import Seeder


class DrinkersTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('drinkers').insert({
            'name': 'Melons',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'profile_pivot_type': 1,
            'profile_pivot_increment': 3,
            'is_public': True,
            'bio_line': 'My name is Melons!'
        })

        self.db.table('drinkers').insert({
            'name': 'JNorth',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'profile_pivot_type': 1,
            'profile_pivot_increment': 3,
            'is_public': True,
            'bio_line': 'My name is JNorth!'
        })

        self.db.table('drinkers').insert({
            'name': 'Rag',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'profile_pivot_type': 1,
            'profile_pivot_increment': 3,
            'is_public': False,
            'bio_line': 'My name is Rag!'
        })

        self.db.table('drinkers').insert({
            'name': 'Zaddy',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'profile_pivot_type': 1,
            'profile_pivot_increment': 3,
            'is_public': True,
            'bio_line': 'My name is Zaddy!'
        })

        self.db.table('drinkers').insert({
            'name': 'Rock Man',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'profile_pivot_type': 1,
            'profile_pivot_increment': 3,
            'is_public': True,
            'bio_line': 'My name is Rock Man!'
        })

        self.db.table('drinkers').insert({
            'name': 'Eel-i',
            'profile_photos': 'http://example1.com,http://example2.com,http://example3.com,http://example4.com',
            'profile_pivot_type': 1,
            'profile_pivot_increment': 3,
            'is_public': True,
            'bio_line': 'My name is Eel-i!'
        })
