
import json

from decimal import Decimal
from flask import Response
from datetime import datetime, date


class DecimalEncoder(json.JSONEncoder):
    """
    Encode Decimal values for json dumps.
    :return dict, the encoded json data.
    """
    def default(self, obj):

        if isinstance(obj, datetime) or isinstance(obj, date):
            return str(obj)
        elif isinstance(obj, Decimal):
            return float(obj)

        return json.JSONEncoder.default(self, obj)


def handle_exception_json_response(exception):
    """
    Prepare exception for json_response call
    :param exception: dict, the dict data for the response.
    :return: Response, the response object to return.
    """
    message = exception.description
    if hasattr(exception, 'data'):
        message = exception.data['message']
    return json_response({"message": message}, exception.code)


def json_response(data, status=200):
    """
    Prepare data to build Response.
    :param data: dict, the dict data for the response.
    :param status: integer, code status. Ie, 200
    :return: Response, the response object to return.
    """
    data_as_str = DecimalEncoder().encode(data)
    return Response(response=data_as_str, status=status, mimetype="application/json")
