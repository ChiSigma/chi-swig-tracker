from orator.migrations import Migration


class ChangeProfilePhotosType(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.text('profile_photos').nullable().default('default.png').change()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.string('profile_photos').nullable().default('default.png').change()
