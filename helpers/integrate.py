"""Functions providing an easy way to integrate signals"""
import numpy as np

def integrate(signal, dt=float(1E-6)):
    """Integrate a signal using forward difference
    Assumes integration constant = 0
    
    Args:
        signal (arrayLike): singal to integrate
        dt (Name, optional): timestep size
    
    Returns:
        arrayLike: integrated signal of same size
    """
    intContributions = (signal[:-1]+signal[1:])*dt/2
    intContributions = np.insert(intContributions, 0, 0)
    runningInt = np.cumsum(intContributions)
    return runningInt

def intFrom(signal, ROIleft, avg, dt=float(1E-6)):
    """Integrate a signal starting from ROIleft,
    using avg as a base value
    
    Args:
        signal (arrayLike): signal to integrate
        ROIleft (int): index of the beginning of the ROI
        avg (float): average value of noise, used to remove offset
        dt (float, optional): Timestep size
    
    Returns:
        arrayLike: integrated signal of same size
    """
    toInt = signal[ROIleft:] - avg
    intI = integrate(toInt, dt)
    zeros = np.linspace(0, 0, len(signal) - len(intI))
    intI = np.concatenate((zeros, intI))
    return intI
