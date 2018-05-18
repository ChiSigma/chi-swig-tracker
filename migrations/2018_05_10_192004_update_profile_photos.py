from orator.migrations import Migration


class UpdateProfilePhotos(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.drop_column('profile_photo')
            table.string('profile_photos')
            table.integer('profile_pivot_increment')
            table.integer('profile_pivot_type').unsigned()
            table.foreign('profile_pivot_type').references('id').on('event_types').on_delete('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.drop_column('profile_photos')
            table.drop_column('profile_pivot_increment')
            table.drop_column('profile_pivot_type')
            table.string('profile_photo').default('')
