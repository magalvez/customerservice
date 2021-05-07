import json
import requests

from app import US_VALIDATE_USER_ACCOUNT_URL

from util.header import token_headers
from util.response import DecimalEncoder


def validate_user_account(user_id, pin, token):
    """
    Validate User Account
    :param user_id: String, Ie. 'name@domain.com'
    :param pin: String, Ie. 'password'
    :param token: JWT token. String, Ie. 'eyWih&89'
    :return json_response: JSON object, Ie, {'is_valid': true}
    """

    data = {
        'user_id': user_id,
        'pin': pin
    }

    response = requests.post(
        US_VALIDATE_USER_ACCOUNT_URL,
        data=json.dumps(data, cls=DecimalEncoder),
        headers=token_headers(token=token))

    json_response = json.loads(response.text)
    return json_response
