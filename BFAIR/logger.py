# Logging utils for the BFAIR modules.

import logging


def get_logger(name):
    """
    Returns a logger with the specified name.

    Paramters
    ---------
    name : str
        Name of the logger.

    Returns
    -------
    logging.Logger
        A logger object.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("[%(levelname)s]: %(message)s"))
        logger.addHandler(handler)
    return logger
