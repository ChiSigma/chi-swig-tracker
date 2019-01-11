from orator.migrations import Migration


class AddLocationToEvents(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('events') as table:
            table.string('location').default("unknown")

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('events') as table:
            table.drop_column('location')
