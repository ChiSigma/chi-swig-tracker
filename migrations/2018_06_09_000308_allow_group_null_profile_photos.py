from orator.migrations import Migration


class AllowGroupNullProfilePhotos(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('groups') as table:
            table.string('profile_photo').nullable().default('default.png').change()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('groups') as table:
            table.string('profile_photo').default('default.png').change()
