

def get(base_dict, nested_keys, default_value=None):
    """
    Get a nested value from dict if exist or return default value
    :param base_dict: dict, Dictionary to be checked. Ie, {"key": 'value'}
    :param nested_keys: list, dict keys to be validated on the dict. Ie, ["key", "sub_key"]
    :param default_value: any, The default value you whant to return if no has in dict. Ie "key"
    :return Object: Element found on the dict or the value of default_value. Ie, "sub_value" or None
    """

    key_exist, keys_value = keys_exists(base_dict, nested_keys, not_found_value=default_value)

    return keys_value


def keys_exists(validation_dict, nested_keys, not_found_value=None):
    """
    Validate nested attributes on dictionary
    Based on https://stackoverflow.com/questions/43491287/elegant-way-to-check-if-a-nested-key-exists-in-a-python-dict/43491315
    :param validation_dict: dict, Dictionary to be checked. Ie, {"key": {"sub_key": "sub_value"}}
    :param nested_keys: list, dict keys to be validated on the dict. Ie, ["key", "sub_key"]
    :param not_found_value: Value returned when no element is found on the dict. Ie, None or []
    :return Tuple:
        - boolean, Confirms if nested key is found. Ie, True
        - Element found on the dict or the value of not_found_value. Ie, "sub_value" or None

    Usage examples:

        > # success example
        > validation_dict = {"key": {"sub_key": "sub_value"}}
        > nested_keys = ["key", "sub_key"]
        > not_found_value = []
        > keys_exists(validation_dict, nested_keys, not_found_value)
        (True, 'sub_value')

        > # not found example
        > validation_dict = {"key": {"sub_key": "sub_value"}}
        > nested_keys = ["key", "sub_key_not_found"]
        > not_found_value = []
        > keys_exists(validation_dict, nested_keys, not_found_value)
        (False, [])

        > # empty dict example
        > validation_dict = {}
        > nested_keys = ["key", "sub_key_not_found"]
        > not_found_value = []
        > keys_exists(validation_dict, nested_keys, not_found_value)
        (False, [])

        > # empty key list example
        > validation_dict = {"key": {"sub_key": "sub_value"}}
        > nested_keys = []
        > not_found_value = []
        > keys_exists(validation_dict, nested_keys, not_found_value)
        (False, [])
    """

    if type(validation_dict) is not dict or not nested_keys:
        return False, not_found_value

    temp_validation_dict = validation_dict
    for key in nested_keys:
        try:
            temp_validation_dict = temp_validation_dict[key]
        except Exception:
            return False, not_found_value
    return True, temp_validation_dict
