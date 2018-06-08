from orator.migrations import Migration


class AddDrinkerMembershipPolicy(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.enum('membership_policy', ['open', 'private', 'primary', 'ephemeral']).default('open')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.drop_column('membership_policy')
