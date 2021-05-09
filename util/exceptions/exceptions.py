from werkzeug.exceptions import HTTPException


class BadRequest(HTTPException):
    def __init__(self):
        HTTPException.__init__(self)
        self.code = 400
        self.data = dict()
        self.data['message'] = 'The request cannot be fulfilled due to bad syntax.'


class ApiResponseNotFound(HTTPException):
    def __init__(self, data_request_id):
        HTTPException.__init__(self)
        self.code = 404
        self.data = dict()
        self.data['message'] = "There is not an api response associated to the data request with id '{0}'".format(
            data_request_id)


class InvalidFileExtension(HTTPException):
    def __init__(self):
        HTTPException.__init__(self)
        self.code = 400
        self.data = {
            'message': "Invalid File Extension"
        }


class BankAccountInsufficientFounds(HTTPException):
    def __init__(self, account_number, amount, currency, workflow_messages):
        HTTPException.__init__(self)
        workflow_messages.\
            append("ERROR MESSAGE: Insufficient funds to perform a {0} {1} withdrawal, account_number {2}.".
                   format(amount, currency, account_number))
        self.code = 409
        self.data = {
            'message': workflow_messages
        }


class UserInvalidVerification(HTTPException):
    def __init__(self, user_id, pin, workflow_messages):
        HTTPException.__init__(self)
        workflow_messages. \
            append("ERROR MESSAGE: The User your trying to process is not validate. [user_id: {} and pin: {}].".
                   format(user_id, pin))
        self.code = 401
        self.data = {
            'message': workflow_messages
        }


class JsonDecodeError(ValueError):
    """
    Class to identify an exception raised if json.loads method fails, because it contains non serializable data
    """

    def __init__(self, text):
        """
        Initialize ValueError class
        :param text: name of the parameter involved in the error. String, Ie. 'application'
        """
        self._text = text
        self._message = "The received text couldn't be decoded: %s" % self._text
