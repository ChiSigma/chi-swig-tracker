from swig_core_exception import SwigCoreException

class InvalidEnumException(SwigCoreException):
    status_code = 400

    def __init__(self, value=None, field=None):
        message = '{0} is not a valid value for {1}'.format(value, field)
        SwigCoreException.__init__(self, message)
