
from functools import wraps

from util.exceptions.exceptions import ApiResponseNotFound, BadRequest, InvalidFileExtension, \
    BankAccountInsufficientFounds, UserInvalidVerification
from util.response import json_response, handle_exception_json_response


def api_resource_endpoint():
    """
    Wrapper function to handle API endpoint
    :return decorator_function: the decorator itself
    """

    def wrapper_function(function):
        """
        Decorator used in API endpoints to handle the exceptions possibly raised
        :param function: function to be decorated. Function
        :return decorator_function: the decorator itself
        """

        @wraps(function)
        def decorator_function(*args, **kwargs):

            try:
                return function(*args, **kwargs)

            except ApiResponseNotFound as e:
                return handle_exception_json_response(e)

            except BadRequest as e:
                return handle_exception_json_response(e)

            except InvalidFileExtension as e:
                return handle_exception_json_response(e)

            except BankAccountInsufficientFounds as e:
                return handle_exception_json_response(e)

            except UserInvalidVerification as e:
                return handle_exception_json_response(e)

            except Exception as e:
                return json_response({'message': 'An error occurred while processing the request. ERROR: {0}'.format(e)}, 500)

        return decorator_function

    return wrapper_function
