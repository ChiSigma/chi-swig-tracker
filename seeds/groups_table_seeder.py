from orator.seeds import Seeder
from datetime import datetime

class GroupsTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('groups').insert({
            'name': 'Undeclared'
        })
        self.db.table('groups').insert({
            'name': 'Chi Sigma',
            'profile_photo': "https://chisigma.co/img/crest.png",
            'created_at': datetime(2018, 5, 23, 17, 58, 5, 939)
        })

