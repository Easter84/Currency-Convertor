"""
This module is responsible for creating and maintaining all logs related to the application.
"""
import logging as log


log.basicConfig(filename='logs/log_data.log',
                level=log.INFO,
                format='[%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')


def get_logger(module_name):
    """
    Is used to create a logging object
    :param module_name: the name of the current module
    :return: the log
    """
    return log.getLogger(module_name)
