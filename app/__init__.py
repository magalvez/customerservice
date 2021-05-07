"""
Flask app module
"""

from os import environ
from flask import Flask

app = Flask(__name__)
app.config.from_object("default_config")

AUTH_USER = environ.get("AUTH_USER") or 'playvox'
AUTH_PASS = environ.get("AUTH_PASS") or 'pl4yv0x'

AUTH_API_V1_URL = environ.get("ATS_API_V1_URL") or 'http://localhost:8100/service/auth'
US_API_V1_URL = environ.get("US_API_V1_URL") or 'http://localhost:8200/userservice/api/v1.0'
BAS_API_V1_URL = environ.get("BAS_API_V1_URL") or 'http://localhost:8300/bankaccountservice/api/v1.0'

AUTH_URL = AUTH_API_V1_URL
US_VALIDATE_USER_ACCOUNT_URL = US_API_V1_URL + '/validate-user-account'
BANK_ACCOUNT_GET_ACCOUNT_URL = BAS_API_V1_URL + '/account/{user_id}'
BANK_ACCOUNT_DEPOSIT_URL = BAS_API_V1_URL + '/account/{account_number}/deposit'
BANK_ACCOUNT_WITHDRAWAL_URL = BAS_API_V1_URL + '/account/{account_number}/withdrawal'

# TRM
TRM_USER_SERVICE_URL = 'https://trm-colombia.vercel.app/?date={}'
