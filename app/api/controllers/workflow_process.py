#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from app.api.external.auth_api.v1_1.auth_service_api import generate_jwt_token
from app.api.external.bank_api.v1_1.bank_account_service_api import get_account_balance, deposit_money, withdraw
from app.api.external.trm.trm_api import get_current_trm
from app.api.external.us_api.v1_1.user_service_api import validate_user_account
from util.dict_helper import get


class WorkflowProcessController(object):
    """
    Class WorkflowProcessController executes and manages the workflow process definition
    """

    def __init__(self, json_data):
        self.json_data = json_data
        self.actions = {
            "validate_account": self.validate_account,
            "withdraw_in_dollars": self.withdraw_in_dollars,
            "withdraw_in_pesos": self.withdraw_in_pesos,
            "deposit_money": self.deposit_money,
            "get_account_balance": self.get_account_balance
        }
        self.steps = {}
        self.switcher_operator = {
            "eq": self.equals,
            "gt": self.greater_than,
            "gte": self.greater_than_equals,
            "lt": self.lower_than,
            "lte": self.lower_than_equals
        }
        self.workflow_session = {
            'start': {},
            'validate_account': {},
            'account_balance': {},
            'messages': []
        }
        self.balance = 0
        self.token = None
        self.trm = 0
        self.get_trm()

    def process(self):
        """
        Start Process
        """
        trigger = self.json_data.get('trigger')
        steps = self.json_data.get('steps')
        steps_dict = {step.get("id"): step for step in steps}
        steps_dict[trigger.get('id')] = trigger
        self.steps = steps_dict
        step_id = self.get_trigger(trigger)
        if not step_id:
            raise
        return self.run_workflow(step_id)

    def get_trigger(self, trigger):
        """
        Get the workflow trigger
        """
        transitions = trigger.get('transitions')
        step_id = get(next(iter(transitions)), ['target'], None)
        return step_id

    def run_workflow(self, step_id):
        """
        Run Workflow
        :param step_id:
        :return: {'balance', 4345, ...}
        """

        step = self.steps.get(step_id)

        while step is not None:
            param = self.get_params(step.get('params'))
            self.execute_action(step.get('action'), param)
            transitions = step.get('transitions')
            if not transitions:
                step = None
                continue
            for transition in transitions:
                if transition.get('condition'):
                    is_valid_condition = self.validate_conditions(transition.get('condition'))
                    if is_valid_condition:
                        step = self.steps[transition.get('target')]
                        break
                    else:
                        step = None
                else:
                    step = self.steps[transition.get('target')]

            if not step:
                self.workflow_session['messages'].append('No step condition matched, this is the end of the process')

        return self.workflow_session

    def get_params(self, step_params):
        """
        Get params from workflows steps
        :param step_params:
        :return: {'key': 'sdfsdf', 'value': 'asdasd'}
        """
        params = {}
        for key, step_param in step_params.items():
            from_id = step_param.get('from_id')
            param_id = step_param.get('param_id')
            param_value = get(self.steps, [from_id, 'params', param_id]) if from_id else step_param.get('value')
            params[key] = param_value
        return params

    def execute_action(self, action, param):
        """
        Execute workflow actions
        :param action: String, Ie 'validate_account'
        :param param: dict Ie, {'param1', 'param2'}
        :return: dict, {'key': 'ere', value: 'wrwer'}
        """
        return self.actions[action](param)

    def validate_conditions(self, conditions):
        """
        Validate conditions results
        :param conditions: array
        :return: dict
        """
        result = True
        for condition in conditions:
            from_id = condition.get('from_id')
            field_id = condition.get('field_id')
            value_result = get(self.workflow_session, [from_id, field_id])
            operator = condition['operator']
            value_condition = condition['value']
            result = self.switcher_operator[operator](value_result, value_condition)
            if not result:
                break
        return result

    @staticmethod
    def equals(result_value, condition_value):
        return result_value == condition_value

    @staticmethod
    def greater_than(result_value, condition_value):
        return result_value > condition_value

    @staticmethod
    def greater_than_equals(result_value, condition_value):
        return result_value >= condition_value

    @staticmethod
    def lower_than(result_value, condition_value):
        return result_value < condition_value

    @staticmethod
    def lower_than_equals(result_value, condition_value):
        return result_value <= condition_value

    def validate_account(self, params):
        current_user = generate_jwt_token()
        self.token = current_user['token']
        validate_account = validate_user_account(params['user_id'], params['pin'], token=current_user['token'])
        self.workflow_session['start']['user_id'] = params['user_id']
        self.workflow_session['start']['pin'] = params['pin']
        self.workflow_session['validate_account'] = validate_account
        self.workflow_session['messages'].append('Executed step [validate_account] - params [{0}] - {1}'.
                                                 format(params, validate_account))
        return validate_account

    def get_account_balance(self, params):
        account = get_account_balance(params['user_id'], self.token)
        account_balance = {'account_number': account['account_number'], 'balance': account['balance']}
        self.workflow_session['account_balance'] = account_balance
        self.workflow_session['messages'].append('Executed step [get_account_balance] - params [{0}] - {1}'.
                                                 format(params, account_balance))
        return account_balance

    def deposit_money(self, params):
        account_balance = deposit_money(self.workflow_session['account_balance']['account_number'],
                                        params['money'], self.token)
        self.workflow_session['account_balance']['balance'] = account_balance['balance']
        self.workflow_session['messages'].append('Executed step [deposit_money] - params [{0}] - {1}'.
                                                 format(params, account_balance))

    def withdraw_in_pesos(self, params):
        account_balance = withdraw(self.workflow_session['account_balance']['account_number'], params['money'],
                                   'COP', self.trm, self.token)
        self.workflow_session['account_balance']['balance'] = account_balance['balance']
        self.workflow_session['messages'].append('Executed step [withdraw_in_pesos] - params [{0}] - {1}'.
                                                 format(params, account_balance))

    def withdraw_in_dollars(self, params):
        amount = params['money'] * self.trm
        account_balance = withdraw(self.workflow_session['account_balance']['account_number'], amount,
                                   'USD', self.trm, self.token)

        self.workflow_session['account_balance']['balance'] = account_balance['balance']
        self.workflow_session['messages'].append('Executed step [withdraw_in_dollars] - params [{0}] - {1}'.
                                                 format(params, account_balance))

    def get_trm(self):
        """
        Get current TRM based on a specific date
        :param: trm_date: String, Ie '2021-05-06'
        :return json_response: JSON object, Ie, {
                "data":{
                    "unit":"COP",
                    "validityFrom":"2019-02-02T05:00:00.000Z",
                    "validityTo":"2019-02-04T05:00:00.000Z",
                    "value":3102.61,
                    "success":true
                },
                "dev":"Jonhatan Fajardo",
                "web":"www.makaw.dev"
            }
        """
        current_date = datetime.today().strftime('%Y-%m-%d')
        trm_response = get_current_trm(current_date)
        if get(trm_response, ['data']) and get(trm_response, ['data', 'success']):
            self.trm = get(trm_response, ['data', 'value'])
