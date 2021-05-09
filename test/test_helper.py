import json
import unittest

from mock import patch

from util.exceptions.exceptions import JsonDecodeError
from util.response import DecimalEncoder


class MockMixinClass(object):

    @staticmethod
    def build_patches(patch_dict):
        """
        Create patch objects to be sent to a context manager
        :param patch_dict: Dict, patches to be applied to mock imports. Ie,
            {
                'util.dict_helper':
                    {'return_value': {u'user_id': u'10', u'account_number': u'80672'}
            }
        :return: List with patch objects. Ie,
            [
                patch('util.dict_helper', return_value={u'user_id': u'10', ...})
            ]
        """
        patches = []

        for key, value in patch_dict.items():
            patcher = patch(key, **value)
            patches.append(patcher)

        return patches


class JsonAssertMissing(unittest.TestCase):
    """
    Class to handles the JSON response codes
    """

    def response_code_assert(self, code_to_check, response):
        """Check http response"""

        self.assertEqual(response.status_code, code_to_check)

    def json_structure_response_code_assert(self, code_to_check, response):
        """Check http response"""

        self.assertEqual(response.content_type, 'application/json')

        if response.data:
            self.assertEqual(response.status_code, code_to_check)


class TestHttpRequest:
    """
    Class to handle http request in tests
    """

    def __init__(self, app, endpoint_url, is_form_data=False):
        self.app = app
        self.endpoint_url = endpoint_url
        self.headers = {'Content-Type': 'multipart/form-data'} if is_form_data else {'Content-Type': 'application/json'}
        self.is_form_data = is_form_data

    def set_endpoint_url(self, new_endpoint_url):
        """
        Set a new endpoint URL for endpoint with params on it.
        :param new_endpoint_url: str, the new URL to set. Ie. '/application/12345/has_cashflow'
        """
        self.endpoint_url = new_endpoint_url

    def get(self, data=None, headers=None, params=None):
        """
        Return a result of a request using GET method
        """
        optional_params = self.__process_params(data=data, headers=headers, params=params)
        return self.app.get(self.endpoint_url, **optional_params)

    def post(self, data=None, headers=None, authorization=None):
        """
        Return a result of a request using POST method
        """
        optional_params = self.__process_params(data=data, headers=headers, authorization=authorization)
        return self.app.post(self.endpoint_url, **optional_params)

    def put(self, data=None, headers=None):
        """
        Return a result of a request using PUT method
        """
        optional_params = self.__process_params(data=data, headers=headers)
        return self.app.put(self.endpoint_url, **optional_params)

    def patch(self, data=None, headers=None):
        """
        Return a result of a request using PATCH method
        """
        optional_params = self.__process_params(data=data, headers=headers)
        return self.app.patch(self.endpoint_url, **optional_params)

    def delete(self, data=None, headers=None):
        """
        Return a result of a request using DELETE method
        """
        optional_params = self.__process_params(data=data, headers=headers)
        return self.app.delete(self.endpoint_url, **optional_params)

    def __process_params(self, data=None, headers=None, authorization=None, params=None):
        """
        Process HTTP Request params
        """

        optional_params = {}
        if data:
            optional_params['data'] = {'file': data} if self.is_form_data else json.dumps(data, cls=DecimalEncoder)

        optional_params['headers'] = self.headers
        if headers:
            optional_params['headers'].update(headers)

        if authorization:
            optional_params.update(authorization)

        if params:
            optional_params['query_string'] = params

        return optional_params


class BaseTest(MockMixinClass, JsonAssertMissing, unittest.TestCase):

    def tearDown(self):
        """
        Close In Memory MongoDB Instance
        """
        pass


def deserialize_json(text):
    """
    Function to deserialize a JSON argument
    :param text: text to be deserialized. String, Ie. '{data: 1}'
    :return dictionary containing the json deserialized data. Dict, Ie. {data: 1}
    """
    try:
        return json.loads(text)
    except ValueError as e:
        raise JsonDecodeError(text)
