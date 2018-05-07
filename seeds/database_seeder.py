from orator.seeds import Seeder
import drinkers_table_seeder
import event_types_table_seeder
import events_table_seeder


class DatabaseSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.call(drinkers_table_seeder.DrinkersTableSeeder)
        self.call(event_types_table_seeder.EventTypesTableSeeder)
        self.call(events_table_seeder.EventsTableSeeder)
