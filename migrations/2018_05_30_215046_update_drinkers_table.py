from orator.migrations import Migration


class UpdateDrinkersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.string('profile_photos').default('default.png').change()
            table.string('bio_line').default("I am lame wihtout a bio :(").change()
            table.integer('profile_pivot_increment').default(3).change()
            table.integer('profile_pivot_type').unsigned().default(1).change()
            table.integer('primary_group_id').unsigned().default(1)
            table.foreign('primary_group_id').references('id').on('groups')
            table.string('email').nullable()
            table.drop_column('is_public')
            table.enum('privacy_setting', ['public', 'hide_events', 'unlisted']).default('public')
            table.boolean('group_admin').default(False)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.string('profile_photos').change()
            table.string('bio_line').change()
            table.integer('profile_pivot_increment').change()
            table.integer('profile_pivot_type').unsigned().change()
            table.drop_column('primary_group_id')
            table.drop_column('email')
            table.boolean('is_public')
            table.drop_column('privacy_setting')
