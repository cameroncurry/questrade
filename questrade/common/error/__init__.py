#
# Copyright Cameron Curry (c) 2017
#


class QTError(Exception):

    def __init__(self, status_code, message):
        super().__init__('Questrade Responded with: {} {}'.format(status_code, message))


class QTGeneralError(Exception):

    def __init__(self, status_code, qt_code, message):
        super().__init__('{} code: {}, message: {}'.format(status_code, qt_code, message))


class QTTokenInvalidError(QTGeneralError):
    pass


class QTInvalidEndpointError(QTGeneralError):
    pass
