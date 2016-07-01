"""Class that automatically analyzes peaks in a signal and provides input and output options"""
import IO
from logs import log, logobject
from classes import AnalysedSignal, PointOnGraph, PeakWidth
from helpers import indexOfFirst
from helpers import intFrom

import os
import numpy as np
import operator

class Analyzer():
    """Main class to analyze scope signal
    
    Attributes:
        analysedSignals (list): list of signals that are analyzed already
        beginRange (list): 2-item list with start and end of begin range
        data (ScopeData): ScopeData read from file, ready to analyze
        distance (float): Distance between sensors
        dt (float): timestep size
        ROIsafety (int): Size the region of interest must be moved to the left for safety
        sensitivity (list): sensitivity for each sensor
        sigmaFactor (int): how many times the standard deviation must be multiplied to find threshold
        stdLength (int): length of interval from which standard deviation is calculated
        toAnalyze (list): List of names of arrays in data that need to be analyzed
        v (arrayLike): veloctity signal (integrated from acceleration)
        widths (list): widhts of peaks
    """
    def __init__(self, fname):
        """Retreives data from files, calls all functions to analyze
        
        Args:
            fname (str): File name of data to analyze
        """
        # TODO get these settings from config file
        # settings for the analyzer
        self.toAnalyze = ['sens2', 'sens3']
        self.beginRange = [1, 500]  # some points containing only noise
        self.ROIsafety = 500  # position of ROI is moved this much to left
        self.sigmaFactor = 10  # set's what is a significant increase
        self.dt = float(1E-6)  # timestep size
        self.stdLength = 100  # length of interval after ROI
        self.distance = float(4.5E-2)  # distance between sensors (in m)
        self.sensitivity = [0.009645, 0.09965] # V/ms^-2

        log('Starting analyzer for : '+fname)

        # read the data from file
        self.data = IO.readScopeFile(fname)

        # analyse the signals
        self.analysedSignals = self.analyseAll()

        # get speed
        self.v = self.calcSpeed(self.analysedSignals[0],
                                self.analysedSignals[1])

        # get widths
        self.widths = self.calcWidths()

    def calcWidths(self):
        """Calculated width of all analyzed signals
        
        Returns:
            list: list containing widths of peaks
        """
        widths = []
        for s in self.analysedSignals:
            w = PeakWidth(s.hwLeft, s.peak, s.hwRight)
            widths.append(w)
        return widths

    def calcSpeed(self, s1, s2, mode='HALFWAY'):
        """Calculate the speed based on signal s1 and s2
        
        Args:
            s1 (analysedSignal): signal 1
            s2 (analysedSignal): signal 2
            mode (str, optional): Use peaks or first halfway point
        
        Raises:
            Exception: exception when unknown mode is requested
        
        Returns:
            float: wavespeed
        """
        if mode == 'PEAKS':
            n = abs(s1.peak.idx - s2.peak.idx)
            tof = n * self.dt
            v = self.distance / tof
            return v
        elif mode == 'HALFWAY':
            n = abs(s1.hwLeft.idx - s2.hwLeft.idx)
            tof = n * self.dt
            v = self.distance / tof
            return v
        else:
            raise Exception('Unknown speed calculation mode')

    def analyseAll(self):
        """Calls the analyseSignal function for every signal that needs
        to be analyzed
        
        Returns:
            list: list of analysedSignals
        """
        analysed = []
        for sens in self.toAnalyze:
            if type(getattr(self.data, sens, False)) is not bool:
                a = self.analyseSignal(getattr(self.data, sens, False))
                analysed.append(a)
        return analysed

    def analyseSignal(self, signal):
        """Analyse a signal by finding its peak and halway points
        
        Args:
            signal (arrayLike): acceleration data to analyze
        
        Returns:
            analysedSignal: resulting data from analysis
        """
        # create object to store data
        # this reinitilizing is needed to remove links
        a = AnalysedSignal()

        # get standard deviation and average of beginning
        a.std = np.std(signal[self.beginRange[0]:self.beginRange[1]])
        avg = np.mean(signal[self.beginRange[0]:self.beginRange[1]])

        # calculates how much a value deviates (positive) from the threshold
        threshold = avg+self.sigmaFactor*a.std
        # find first significant increase, subtract safety factor
        a.ROIleft = indexOfFirst(signal, threshold, mode='ABOVE') - self.ROIsafety

        # base average on roi rather than beginning of signal
        avg = np.mean(signal[a.ROIleft-len(self.beginRange):a.ROIleft])
        a.avg = avg
        # integrate the signal
        a.v = intFrom(signal, a.ROIleft, avg, self.dt)
        stdInV = np.std(a.v[a.ROIleft:a.ROIleft+self.stdLength])
        a.stdInV = stdInV

        # guess a value for the peak
        peakSearch = a.v[a.ROIleft:]
        peakIdx = self.findPeak(peakSearch, self.sigmaFactor*stdInV)\
            + a.ROIleft
        peakVal = a.v[peakIdx]

        hwVal = (peakVal)/2  # guess value for halfway point

        # threshold for halway points (guess)
        rhwIdx = indexOfFirst(a.v[peakIdx:], hwVal, mode='BELOW') + peakIdx
        lhwIdx = peakIdx - indexOfFirst(reversed(a.v[:peakIdx]), hwVal,
                                        mode='BELOW')

        # true peak
        peakSearch = a.v[lhwIdx:rhwIdx]
        peakIdx, peakVal = max(enumerate(peakSearch),
                               key=operator.itemgetter(1))
        peakIdx = peakIdx + lhwIdx
        a.peak = PointOnGraph(peakIdx, peakVal)

        # true halfway points
        hwVal = (a.peak.h)/2
        rhwIdx = indexOfFirst(a.v[peakIdx:], hwVal, mode='BELOW') + peakIdx
        lhwIdx = peakIdx - indexOfFirst(reversed(a.v[:peakIdx]), hwVal,
                                        mode='BELOW')
        a.hwLeft = PointOnGraph(lhwIdx, a.v[lhwIdx])
        a.hwRight = PointOnGraph(rhwIdx, a.v[rhwIdx])

        return a

    def findPeak(self, signal, threshold):
        """Find a peak in a signal, starting from the left
        triggered when the signal exceeds thershold,
        maximum is triggerd when signal drops below maximum-threshold
        
        Args:
            signal (arrayLike): Signal containing the peak to be found
            threshold (float): threshold value
        
        Returns:
            int: index of peak
        """
        maxTillNow = -float('Inf')
        for idx, n in enumerate(signal):
            if (n > maxTillNow):
                maxTillNow = n
                maxIdx = idx
            if n < (maxTillNow - threshold) and n > 0:
                break
        return maxIdx

    def writeOut(self):
        """Create a string containing all important information, ready to be written to file
        
        Returns:
            str: String with all the info, seperated by spaces
        """
        toReturn = []
        # general info
        toReturn.append(self.data.fname.split('/')[-1])
        toReturn.append(str(self.v))
        toReturn.append(str(self.widths[0].getWidth()))
        toReturn.append(str(self.widths[1].getWidth()))

        # signal 1
        toReturn.append(str(self.analysedSignals[0].hwLeft.idx))
        toReturn.append(str(self.analysedSignals[0].hwLeft.h /
                            self.sensitivity[0]))

        toReturn.append(str(self.analysedSignals[0].peak.idx))
        toReturn.append(str(self.analysedSignals[0].peak.h /
                            self.sensitivity[0]))


        toReturn.append(str(self.analysedSignals[0].hwRight.idx))
        toReturn.append(str(self.analysedSignals[0].hwRight.h /
                            self.sensitivity[0]))

        # signal 2
        toReturn.append(str(self.analysedSignals[1].hwLeft.idx))
        toReturn.append(str(self.analysedSignals[1].hwLeft.h /
                            self.sensitivity[1]))

        toReturn.append(str(self.analysedSignals[1].peak.idx))
        toReturn.append(str(self.analysedSignals[1].peak.h /
                            self.sensitivity[1]))

        toReturn.append(str(self.analysedSignals[1].hwRight.idx))
        toReturn.append(str(self.analysedSignals[1].hwRight.h /
                            self.sensitivity[1]))

        # low pass filter limit
        toReturn.append(str(self.filterCoreSize1))

        return ' '.join(toReturn)
