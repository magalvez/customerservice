import json
import requests

from app import TRM_USER_SERVICE_URL


def get_current_trm(trm_date):
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

    response = requests.get(
        TRM_USER_SERVICE_URL.format(trm_date),
        headers={'Content-Type': 'application/json'})

    json_response = json.loads(response.text)
    return json_response
