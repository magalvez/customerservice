import locale


def format_currency(value):
    """
    Given a number value, return the currency format.
    :param value: Number, Number not formatted. Ie, 346.9
    :return value: Value formatted. Ie, $346.9
    """
    locale.setlocale(locale.LC_ALL, 'en_US')
    formatted_value = locale.currency(value, grouping=True)
    number_values = formatted_value.split('.')
    formatted_value = number_values[0]
    if len(number_values) > 1:
        decimals = int(number_values[1])
        if decimals > 0:
            formatted_value = formatted_value + '.{0}'.format(decimals)

    return formatted_value
