from swig_core_exception import SwigCoreException

class ForbiddenAccessException(SwigCoreException):
    status_code = 403

    def __init__(self, entity):
        message = 'You do not have access to {0}'.format(entity)
        SwigCoreException.__init__(self, message)
