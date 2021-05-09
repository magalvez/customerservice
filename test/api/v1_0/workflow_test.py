#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import json

from contexter import Contexter
from werkzeug.datastructures import FileStorage

from app import app
from app.api import api

from test.test_helper import BaseTest, TestHttpRequest, deserialize_json
from util.test.workflow_mock import WORKFLOW_MOCK


class WorkflowProcessTest(BaseTest):
    """
    Set of tests for Workflow endpoint
    """

    @classmethod
    def setUpClass(cls):

        cls.__endpoint_url = '/customerservice/api/v1.0/workflow-process'

        # So the exception would be catch by flask-restful
        app.config['PROPAGATE_EXCEPTIONS'] = False
        cls.app = app.test_client()

        cls.http_request = TestHttpRequest(cls.app, cls.__endpoint_url, is_form_data=True)

    def get_patches(self, new_patches=None):
        """
        Get the mock patches to be used.
        :return: list, the mock patches to apply.
        """

        patch_dict = {
            'app.api.controllers.workflow_process.generate_jwt_token': {
                'return_value': {'pin': 2091,
                                 'token': 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTYyMDQzMDYzOSwiZXhwIjoxNjI5MDcwNjM5fQ.eyJ1c2VyX2lkIjoiMTA1Mzk4ODkwIiwicGluIjoyMDkxLCJleHBpcmF0aW9uX2RhdGUiOiIwOC8xNS8yMDIxIiwiZXhwaXJlX2RhdGUiOiIwOC8xNS8yMDIxIDE4OjM3OjE5IiwiZXhwIjoxNjI5MDcwNjM5LjAyMzgyfQ.Az8u-6Q5KyhuJ0dkMPhgHKQJBPg5eyrG3LoKeUvmyjk',
                                 'user_id': '105398890'}
            }, 'app.api.controllers.workflow_process.validate_user_account': {
                'return_value': {'is_valid': True}
            },
            'app.api.controllers.workflow_process.get_current_trm': {
                'return_value': {
                    'data': {
                        'unit': 'COP',
                        'validityFrom': '2019-02-02T05:00:00.000Z',
                        'validityTo': '2019-02-04T05:00:00.000Z',
                        'value': 3800.33,
                        'success': True
                    }
                }
            },
            'app.api.controllers.workflow_process.get_account_balance': {
                'return_value': {'user_id': '105398891', 'balance': 1000, 'account_number': '000101'}
            },
            'app.api.controllers.workflow_process.deposit_money': {
                'return_value': {'balance': 115000}
            },
            'app.api.controllers.workflow_process.withdraw': {
                'return_value': {'balance': 230000}
            }
        }

        if new_patches is not None:
            for key, value in new_patches.items():
                patch_dict[key] = value

        return self.build_patches(patch_dict)

    def test_workflow_success(self):
        """
        Check the endpoint returns a success workflow response (HTTP 200)
        """
        workflow_json = json.dumps(WORKFLOW_MOCK).encode("utf-8")

        with Contexter(*self.get_patches()):
            workflow_data = FileStorage(
                stream=io.BytesIO(workflow_json),
                filename="workflow_data.json",
                content_type="application/json",
            )

            response = self.http_request.post(workflow_data)
            self.json_structure_response_code_assert(200, response)

    def test_workflow_insufficient_founds_error(self):
        """
        Check the endpoint returns a insufficient founds workflow response (HTTP 409)
        """
        workflow_json = json.dumps(WORKFLOW_MOCK).encode("utf-8")

        new_patch_dict = {
            'app.api.controllers.workflow_process.get_account_balance': {
                'return_value': {'user_id': '105398891', 'balance': 110000, 'account_number': '000101'}
            }, 'app.api.controllers.workflow_process.deposit_money': {
                'return_value': {'balance': 1}
            },
            'app.api.controllers.workflow_process.withdraw': {
                'return_value': {'balance': 23000000000}
            }
        }

        with Contexter(*self.get_patches(new_patch_dict)):
            workflow_data = FileStorage(
                stream=io.BytesIO(workflow_json),
                filename="workflow_data.json",
                content_type="application/json",
            )

            response = self.http_request.post(workflow_data)
            self.json_structure_response_code_assert(409, response)

            data = deserialize_json(response.data)
            messages = data['message']
            error = messages[len(messages)-1]
            self.assertEqual(error, 'ERROR MESSAGE: Insufficient funds to perform a 30 USD withdrawal, account_number 000101.')

    def test_valid_user_verification(self):
        """
        Check the endpoint returns a valid user workflow response (HTTP 200)
        """
        workflow_json = json.dumps(WORKFLOW_MOCK).encode("utf-8")

        new_patch_dict = {
            'app.api.controllers.workflow_process.validate_user_account': {
                'return_value': {'is_valid': True}
            }
        }

        with Contexter(*self.get_patches(new_patch_dict)):
            workflow_data = FileStorage(
                stream=io.BytesIO(workflow_json),
                filename="workflow_data.json",
                content_type="application/json",
            )

            response = self.http_request.post(workflow_data)
            self.json_structure_response_code_assert(200, response)

    def test_invalid_user_verification(self):
        """
        Check the endpoint returns a invalid user workflow response (HTTP 200)
        """
        workflow_json = json.dumps(WORKFLOW_MOCK).encode("utf-8")

        new_patch_dict = {
            'app.api.controllers.workflow_process.validate_user_account': {
                'return_value': {'is_valid': False}
            }
        }

        with Contexter(*self.get_patches(new_patch_dict)):
            workflow_data = FileStorage(
                stream=io.BytesIO(workflow_json),
                filename="workflow_data.json",
                content_type="application/json",
            )

            response = self.http_request.post(workflow_data)
            self.json_structure_response_code_assert(401, response)
