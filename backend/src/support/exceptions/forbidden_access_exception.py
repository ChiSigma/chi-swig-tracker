from swig_core_exception import SwigCoreException

class ForbiddenAccessException(SwigCoreException):
    status_code = 403
