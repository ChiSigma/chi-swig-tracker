from orator.migrations import Migration


class AddingMemberships(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('memberships') as table:
            table.increments('id')
            table.boolean('admin').default(False)
            table.enum('type', ['ephemeral', 'primary'])
            table.integer('drinker_id').unsigned()
            table.foreign('drinker_id').references('id').on('drinkers')
            table.integer('group_id').unsigned()
            table.foreign('group_id').references('id').on('groups')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('memberships') as table:
            self.schema.drop('memberships')
