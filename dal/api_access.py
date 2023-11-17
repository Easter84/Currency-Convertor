"""
This module controls access to the API that is being used, it has an Abstract Parent Class and one
child class for this purpose
"""
from abc import ABC, abstractmethod
import configuration as config
from logs import get_logger
import requests


logger = get_logger(__name__)


class ApiAdapter(ABC):
    """
    This is the parent abstract class used for any api adapters that are needed. It ensures that there are
    callbacks for all api's.
    """
    def __init__(self, callback_success, callback_error):
        self.callback_success = callback_success
        self.callback_error = callback_error

    @abstractmethod
    def run_api(self, *args, **kwargs):
        pass

    def make_request(self, url, params=None):
        """
        This function handles all error for an API call
        :param url: the url for the api call
        :param params: any parameters needed for the api call
        :return: status of api call
        """
        try:
            response = requests.get(url, params=params)
            self.callback_success(response)
            logger.info(f'Response is {response} in self.make_request()')
            return response
        except requests.Timeout as time_out:
            logger.error(f'Connection timed out, {time_out}')
            self.callback_error(f"Request timed out: {time_out}")
        except requests.ConnectionError as connection_error:
            logger.error(f'Connection Error: {connection_error}')
            self.callback_error(f'Connection Error: {connection_error}')
        except requests.RequestException as request_exception:
            logger.error(f'Request Failed: {request_exception}')
            self.callback_error(f'Request Failed: {request_exception}')


class CurrencyExchangeAdapter(ApiAdapter):
    """
    This is the adapter that is responsible for getting the currency, rates, and date of record.
    """
    def run_api(self):
        """
        This function is responsible for executing the api call and return the results
        :return: json results
        """
        url = f"{config.base_url}{config.endpoint}{config.currency_query}"
        logger.info(f'Attempting Contact with URL: {url}')
        results = self.make_request(url)
        logger.info(f"Results: {results}")
        return results
