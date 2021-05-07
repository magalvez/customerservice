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
