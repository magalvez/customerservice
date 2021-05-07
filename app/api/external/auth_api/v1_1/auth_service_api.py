import json
import requests

from app import AUTH_URL, AUTH_USER, AUTH_PASS

from util.response import DecimalEncoder


def generate_jwt_token():
    """
    Generate JWT token
    :return json_response: JSON object, Ie, {'token': 'eyW87n', 'user_id': 1}
    """

    data = {
        'username': AUTH_USER,
        'password': AUTH_PASS
    }

    response = requests.post(
        AUTH_URL,
        data=json.dumps(data, cls=DecimalEncoder),
        headers={'Content-Type': 'application/json'})

    json_response = json.loads(response.text)
    print(json_response)
    return json_response
