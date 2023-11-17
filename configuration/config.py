"""
This module is responsible for maintaining all the necessary default settings the application will use.
"""
import configparser as cp

config = cp.ConfigParser()
config.read('configuration/config.ini')


base_url = config['API']['base_url']
endpoint = config['API']['end_point']
currency_query = config['API']['currency_query']
