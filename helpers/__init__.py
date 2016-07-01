"""Module containing several usefull functions"""
from integrate import integrate
from integrate import intFrom


def indexOfFirst(signal, threshold, mode='ABOVE'):
    """Get the index of the first point where a signal
    is either above or below a threshold
    
    Args:
        signal (arrayLike): signal
        threshold (float): threshold value to compare signal to
        mode (str, optional): Switch to toggle above or below
    
    Returns:
        int: index of the point
    """
    idxFound = 0
    if mode == 'ABOVE':
        for idx, n in enumerate(signal):
            if (n > threshold):
                idxFound = idx
                break
    if mode == 'BELOW':
        for idx, n in enumerate(signal):
            if (n < threshold):
                idxFound = idx
                break
    return idxFound