"""Recursively add an object (basically the copy.deepCopy function rewritten)"""
from logs import logobject


def copyObject(obj):
    """Copies and object and calls itself Recursively for
    attributes that are objects
    
    Args:
        obj (object): Object to copy
    
    Returns:
        obj: New instance of same type and same attributes
    """
    logobject(obj)
    theType = type(obj)
    newObject = theType()
    for attr, value in obj.__dict__.iteritems():
        if hasattr(value, '__dict__'):
            setattr(newObject, attr, copyObject(value))
        else:
            setattr(newObject, attr, value)
    return newObject
