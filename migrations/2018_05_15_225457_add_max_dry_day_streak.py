from orator.migrations import Migration


class AddMaxDryDayStreak(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.integer('max_days_dry').default(0)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.drop_column('max_days_dry')
