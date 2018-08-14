from orator.migrations import Migration


class AddLimitToDrinkCounts(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.integer('drink_count_limit').default(30)
            table.text('drink_time_limit').default('6h')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.drop_column('drink_count_limit')
            table.drop_column('drink_time_limit')
