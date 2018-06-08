from functools import update_wrapper
from orator.orm import scope


class serializer(scope):
    class SerializedCollection(list):
        def __nonzero__(self):
            return True

    def __init__(self, method):
        super(serializer, self).__init__(method)

        self._method = method
        self._owner = None
        self._instance = None

        update_wrapper(self, method)

    def __get__(self, instance, owner, *args, **kwargs):
        self._instance = instance
        self._owner = owner

        return self

    @staticmethod
    def __pluck__(model, attributes):
        return {key: model[key] for key in attributes if key in model}
            
    def __call__(self, *args, **kwargs):
        instance_serialize = len(args) == 0
        subject = self._instance if instance_serialize else self._owner
        attributes = self._method(subject)

        if instance_serialize:
            return self.__pluck__(self._instance.serialize(), attributes)
        else:
            models = map(lambda m: self.__pluck__(m, attributes), args[0].get().serialize())
            return self.SerializedCollection(models)
