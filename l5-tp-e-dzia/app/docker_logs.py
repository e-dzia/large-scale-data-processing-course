"""Docker logs file."""

import logging


def get_logger(mod_name):
    """Gets logger.

    :param mod_name: name of logger
    :return:
    """
    logger = logging.getLogger(mod_name)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
