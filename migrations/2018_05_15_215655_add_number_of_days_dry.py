from orator.migrations import Migration


class AddNumberOfDaysDry(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.integer('num_days_dry').default(0)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.drop_column('num_days_dry')
