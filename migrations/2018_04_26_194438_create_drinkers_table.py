from orator.migrations import Migration


class CreateDrinkersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('drinkers') as table:
            table.increments('id')
            table.string('name')
            table.string('profile_photo')
            table.boolean('is_public')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('drinkers')
