from orator.migrations import Migration


class CreateGroupsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('groups') as table:
            table.increments('id')
            table.string('name')
            table.string('profile_photo').default('default.png')
            table.string('bio_line').default("I am lame with no bio :(")
            table.enum('privacy_setting', ['public', 'hide_events', 'unlisted']).default('public')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('groups') as table:
            self.schema.drop('groups')
