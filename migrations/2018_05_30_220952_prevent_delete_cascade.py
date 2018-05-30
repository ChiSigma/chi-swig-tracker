from orator.migrations import Migration


class PreventDeleteCascade(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('events') as table:
            table.drop_foreign('events_drinker_id_foreign')
            table.foreign('drinker_id').references('id').on('drinkers')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('events') as table:
            table.drop_foreign('events_drinker_id_foreign')
            table.foreign('drinker_id').references('id').on('drinkers').on_delete('cascade')
