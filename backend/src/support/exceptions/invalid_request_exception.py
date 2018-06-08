from swig_core_exception import SwigCoreException

class InvalidRequestException(SwigCoreException):
    status_code = 400

    def __init__(self, error):
        message = 'Invalid request: {0}'.format(error)
        SwigCoreException.__init__(self, message)
