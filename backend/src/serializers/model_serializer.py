from serializer import serializer


class ModelSerializer(object):
    @serializer
    def admin_serialize(self):
        return self.admin_readable()

    @serializer
    def public_serialize(self):
        return self.public_readable()
