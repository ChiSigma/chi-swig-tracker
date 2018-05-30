from orator.migrations import Migration


class AddingEphemeralGroups(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('drinkers_ephemeral_groups') as table:
            table.increments('id')
            table.integer('drinker_id').unsigned()
            table.foreign('drinker_id').references('id').on('drinkers')
            table.integer('group_id').unsigned()
            table.foreign('group_id').references('id').on('groups')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers_ephemeral_groups') as table:
            self.schema.drop('drinkers_ephemeral_groups')
