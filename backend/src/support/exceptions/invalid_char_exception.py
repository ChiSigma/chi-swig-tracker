from swig_core_exception import SwigCoreException

class InvalidCharException(SwigCoreException):
    status_code = 400

    def __init__(self, value=None, field=None, error=None):
        message = '{0} invalid for {1} because: {2}'.format(value, field, error)
        SwigCoreException.__init__(self, message)
