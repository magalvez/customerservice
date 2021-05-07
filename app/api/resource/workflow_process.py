#!flask/bin/python
import json

from flask import jsonify, request
from flask_restful import Resource

from app.api.controllers.workflow_process import WorkflowProcessController
from util.decorators.endpoint_api import api_resource_endpoint
from util.utils import validate_document


class WorkflowProcessAPI(Resource):
    """
    Class WorkflowProcessAPI resource to perform workflow executions
    """

    @api_resource_endpoint()
    def post(self):
        """
        Process JSON file to trigger a workflow definition
        :return: dict: Ie, {'balance' 23434, ;;;;}
        """
        json_to_processor = request.files['file'] if request.files and 'file' in request.files else {}

        result = None
        if json_to_processor:
            validate_document(json_to_processor, 'json')
            json_data = json.loads(json_to_processor.read())
            result = WorkflowProcessController(json_data).process()

        return jsonify({
            'workflow': result
        })
