from orator.orm.scopes import Scope


class STIScope(Scope):

    def apply(self, builder, model):
        return builder if model.__sti_type__ is None else builder.where('type', model.__sti_type__)
