class ScopeData:
    """Abstraction of data in a scope file
    
    Attributes:
        date (list): list of dates (1 for every data point) (unused)
        fname (str): Name of file
        headRule (str): First line of the file
        sens1 (list): data from the first sensor (pressure?)
        sens2 (list): data from second sensor (column 3, close sensor)
        sens3 (list): data from third sensor (column 4, far sensor)
        time (list): time data (unused)
    """
    def __init__(self):
        """init class to set lists empty"""
        self.fname = ''
        self.headRule = ''

        self.date = []
        self.time = []
        self.sens1 = []
        self.sens2 = []
        self.sens3 = []


class AnalysedSignal:
    """Class to hold the usefull information gotten during analysis
    such as peak location and width
    
    Attributes:
        avg (float): average value (during noise)
        hwLeft (PointOnGraph): left halway point
        hwRight (TYPE): right halfway point
        peak (TYPE): location and height of the peak
        ROIleft (int): index (begin) of the region of interest
        std (float): standard deviation (used for threshold)
    """
    def __init__(self):
        """Set all values to 0"""
        self.std = 0.0
        self.avg = 0.0
        self.ROIleft = 0
        self.hwLeft = PointOnGraph(0, 0)
        self.hwRight = PointOnGraph(0, 0)
        self.peak = PointOnGraph(0, 0)


class PointOnGraph:
    """Class to hold information about a point
    consists of width an height only
    
    Attributes:
        h (float): height
        idx (int): index (location)
    """
    def __init__(self, idx=0, h=0):
        """Return the object
        
        Args:
            h (float): height
            idx (int): index (location)
        """
        self.idx = idx
        self.h = h


class PeakWidth:
    """Class to hold multiple definitions of the peak width
    
    Attributes:
        halfwayWidth (float): width as defined by the two halfway points
        leftToPeak (float): distance from peak to left halfway points
    """
    def __init__(self, hwl, p, hwr):
        """Calculates the widths from points
        
        Args:
            hwl (PointOnGraph): left halfway point
            p (PointOnGraph): peak
            hwr (PointOnGraph): right halfway point
        """
        self.halfwayWidth = hwr.idx - hwl.idx
        self.leftToPeak = p.idx - hwl.idx

    def getWidth(self, method='HALFWAY_POINTS'):
        """Get a value for the width of a peak,
        using a specific method
        
        Args:
            method (str, optional): Method to use for determining width
        
        Raises:
            Exception: raises exception when an unkonw method is requested
        
        Returns:
            float: width of the peak
        """
        if method == 'HALFWAY_POINTS':
            return self.halfwayWidth
        elif method == 'LEFT_TO_PEAK':
            return (2 * self.leftToPeak)
        else:
            raise Exception('Unknown method to determine peak width.')
