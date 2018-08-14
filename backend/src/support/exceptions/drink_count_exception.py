from swig_core_exception import SwigCoreException

class DrinkCountException(SwigCoreException):
    status_code = 422

    def __init__(self, limit, time):
        message = 'Cannot create drink event as it exceeds limit of {0} drinks in {1}!'.format(limit, time)
        SwigCoreException.__init__(self, message)
