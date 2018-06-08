from swig_core_exception import SwigCoreException

class OrphanException(SwigCoreException):
    status_code = 400

    def __init__(self, error):
        message = 'Doing this would orphan {0}'.format(error)
        SwigCoreException.__init__(self, message)
