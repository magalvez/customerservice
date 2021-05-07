import copy

JSON_HEADERS = {'Content-Type': "application/json"}


def token_headers(token):
    token_headers_result = copy.deepcopy(JSON_HEADERS)
    token_headers_result['Authorization'] = "Bearer " + token
    return token_headers_result
