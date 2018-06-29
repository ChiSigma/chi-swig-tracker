from orator.migrations import Migration


class AddTotalDaysDry(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.integer('total_days_dry').default(0)

        with self.schema.table('groups') as table:
            table.integer('total_days_dry').default(0)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.drop_column('total_days_dry')

        with self.schema.table('groups') as table:
            table.drop_column('total_days_dry')
