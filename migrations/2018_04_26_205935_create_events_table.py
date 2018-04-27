from orator.migrations import Migration


class CreateEventsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('events') as table:
            table.increments('id')
            table.integer('drinker_id').unsigned()
            table.foreign('drinker_id').references('id').on('drinkers').on_delete('cascade')
            table.integer('event_type_id').unsigned()
            table.foreign('event_type_id').references('id').on('event_types').on_delete('cascade')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('events')
