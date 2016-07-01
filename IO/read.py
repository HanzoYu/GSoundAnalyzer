"""Collection of functions performing reading operations on files, return abstractions
Currently only data from scope file is implemented."""
from logs import log
import numpy as np
from classes import ScopeData  # abstraction of scope info

def readScopeFile(fname):
    """Reads the scopefile in *fname* and returns an abstraction of it
    
    Args:
        fname (string): Filename of file to be read. Relative or absolute.
    
    Returns:
        ScopeData: Instance of scoapedata, containing all usefull data of scope file
    """
    # TODO error handling here
    
    # save metadata
    f = ScopeData()  # abstraction of scope data file
    f.fname = fname  # save name of file
    # save the headrule (contains path of ini file)
    with open(fname, 'r') as scopeFile:
        f.headrule = scopeFile.readline()

    # save data points
    # f.date = np.loadtxt(fname, usecols=(0,))  # not used (data format is non-trivial)
    # f.time = np.loadtxt(fname, usecols=(1,))  # not used (time format is non-trivial)
    f.sens1 = np.loadtxt(fname, usecols=(2,))  # sensor data 1 (pressure)
    f.sens2 = np.loadtxt(fname, usecols=(3,))  # sensor data 2 (close accelerometer)
    f.sens3 = np.loadtxt(fname, usecols=(4,))  # sensor data 3 (far accelerometer)

    # return the object
    return f
