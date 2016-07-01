"""Module providing output logs, usefull for debugging"""
import logging
from pprint import pformat

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:  %(message)s')


def log(msg):
    """Print a log message with timestamp
    
    Args:
        msg (str): message to print
    
    Returns:
        None: Description
    """
    logging.debug(msg)


def logobject(obj, obname=None):
    """Print an object and all its attributes
    not recursive as to avoid a lot of output
    
    Args:
        obj (object): Object to print
        obname (str, optional): Name of an object to print, for clarity
    
    Returns:
        None: Description
    """
    if obname is None:
        s = obj.__class__.__name__+'\n'+pformat(vars(obj))
        log(s)
    else:
        log(obj.__class__.__name__+'\n%s:%s' % (obname, pformat(vars(obj))))
