import json
import requests

from app import BANK_ACCOUNT_GET_ACCOUNT_URL, BANK_ACCOUNT_DEPOSIT_URL, BANK_ACCOUNT_WITHDRAWAL_URL

from util.header import token_headers
from util.response import DecimalEncoder


def get_account_balance(user_id, token):
    """
    Validate User Account
    :param user_id: String, Ie. 'name@domain.com'
    :param token: JWT token. String, Ie. 'eyWih&89'
    :return json_response: JSON object, Ie, {'is_valid': true}
    """

    response = requests.get(
        BANK_ACCOUNT_GET_ACCOUNT_URL.format(user_id=user_id),
        headers=token_headers(token=token))

    json_response = json.loads(response.text)
    return json_response


def deposit_money(account_number, amount, token):
    """
    Deposit Money
    :param account_number: String, Ie. '0001'
    :param amount: Float, Ie. 23434535.0
    :param token: JWT token. String, Ie. 'eyWih&89'
    :return json_response: JSON object, Ie, {'is_valid': true}
    """

    data = {
        'amount': amount
    }

    response = requests.patch(
        BANK_ACCOUNT_DEPOSIT_URL.format(account_number=account_number),
        data=json.dumps(data, cls=DecimalEncoder),
        headers=token_headers(token=token))

    json_response = json.loads(response.text)
    return json_response


def withdraw(account_number, amount, currency, trm, token):
    """
    Create withdrawal
    :param account_number: String, Ie. '0001'
    :param amount: Float, Ie. 23434535.0
    :param currency: String, Ie. 'COP'
    :param trm: Float, Ie. 3800.33
    :param token: JWT token. String, Ie. 'eyWih&89'
    :return json_response: JSON object, Ie, {'balance': 345345}
    """

    data = {
        'amount': amount,
        'currency': currency,
        'trm': trm
    }

    response = requests.patch(
        BANK_ACCOUNT_WITHDRAWAL_URL.format(account_number=account_number),
        data=json.dumps(data, cls=DecimalEncoder),
        headers=token_headers(token=token))

    json_response = json.loads(response.text)
    return json_response
