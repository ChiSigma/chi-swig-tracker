from orator.migrations import Migration


class CreateEventTypesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('event_types') as table:
            table.increments('id')
            table.string('name')
            table.string('icon')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('event_types')
