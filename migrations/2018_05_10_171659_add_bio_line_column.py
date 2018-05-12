from orator.migrations import Migration


class AddBioLineColumn(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.string('bio_line').default("I am boring and have nothing to say.")

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('drinkers') as table:
            table.drop_column('bio_line')
