from orator.migrations import Migration


class AddSuperuserToDrinkers(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.boolean('superuser').default(False)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.drop_column('superuser')
