"""
This module handles the passing of data between the dal and the presentation layer, it does that
by calling the api as necessary for the presentation layer.
"""
from dal import CurrencyExchangeAdapter
from logs import get_logger


logging = get_logger(__name__)


def get_currency_names(currency_callback_success, currency_callback_error):
    """
    This function is used to get the currency names from the api
    :param currency_callback_success: if the api was successful
    :param currency_callback_error: if the api failed
    :return: a json dictionary
    """
    currency_adapter = CurrencyExchangeAdapter(currency_callback_success, currency_callback_error)
    currency_adapter.run_api()
    logging.info(f'Executing Currency Adapter: {currency_adapter}')


def get_exchange_rates(rates_callback_success, rates_callback_error):
    """
    This function is used to get the currency rates, currency and record dates from the api
    :param rates_callback_success: if the api was successful
    :param rates_callback_error: if the api failed
    :return: a json dictionary
    """
    rates_adapter = CurrencyExchangeAdapter(rates_callback_success, rates_callback_error)
    rates_adapter.run_api()
    logging.info(f'Executing Rate Adapter: {rates_adapter}')