from orator.migrations import Migration


class AddDaysDryToGroup(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('groups') as table:
            table.integer('num_days_dry').default(0)
            table.integer('max_days_dry').default(0)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('groups') as table:
            table.drop_column('num_days_dry')
            table.drop_column('max_days_dry')
