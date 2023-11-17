"""
This module handles services for the application it has two functions one to check for valid input and the
other performs the conversion work for the presentation layer.
"""
from logs import get_logger


logging = get_logger(__name__)


def check_dollar_amount(amount):
    """
    This function checks to ensure that the amount the user inputted was a valid number.
    :param amount: a user inputted number
    :return: True or False
    """
    try:
        float_value = float(amount)
        return True
    except ValueError:
        return False


def convert_amount(amount_in_usd, exchange_rate):
    """
    This function converts the exchange rate and amount into floats then calculates and returns
    the new amount.
    :param amount_in_usd: a user inputted number
    :param exchange_rate: retrieved from the json file of the api
    :return: a float amount
    """
    try:
        exchange_rate = float(exchange_rate)
        amount_in_usd = float(amount_in_usd)
        converted_amount = amount_in_usd * exchange_rate
        logging.info(f'Multipling {amount_in_usd} * {exchange_rate}')
        return converted_amount
    except ValueError:
        return None
