#!flask/bin/python

"""
Restful API
"""

from flask_cors import CORS
from flask_restful import Api

from app import app
from app.api.resource.workflow_process import WorkflowProcessAPI


api = Api(app)


api.add_resource(
    WorkflowProcessAPI,
    '/customerservice/api/v1.0/workflow-process',
    endpoint='workflow-process-api'
)

CORS(
    app,
    origins="*",
    allow_headers="*",
    supports_credentials=True
)
