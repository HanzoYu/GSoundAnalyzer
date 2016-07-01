"""OBSOLETE! use modules in stead (for instance via bulk.py)
Starts analyzer for a single file"""
import io
from logs import log, logobject
from config import paths
from classes import AnalysedSignal, PointOnGraph, PeakWidth
from helpers import indexOfFirst
from helpers import intFrom

import os
import numpy as np
import operator

class Analyzer():
    def __init__(self, fname):
        # TODO get these settings from config file
        # settings for the analyzer
        self.toAnalyze = ['sens2', 'sens3']
        self.beginRange = [1, 500]  # some points containing only noise
        self.ROIsafety = 500  # position of ROI is moved this much to left
        self.sigmaFactor = 5  # set's what is a significant increase
        self.dt = float(1E-6)  # timestep size
        self.stdLength = 100  # length of interval after ROI
        self.distance = float(4.8E-2)  # distance between sensors (in m)

        log('Starting analyzer for : '+fname)

        # read the data from file
        self.data = io.readScopeFile(fname)

        # analyse the signals
        self.analysedSignals = self.analyseAll()

        # get speed
        self.v = self.calcSpeed(self.analysedSignals[0],
                                self.analysedSignals[1])

        # get widths
        self.widths = self.calcWidths()

    def calcWidths(self):
        widths = []
        for s in self.analysedSignals:
            w = PeakWidth(s.hwLeft, s.peak, s.hwRight)
            widths.append(w)
        return widths

    def calcSpeed(self, s1, s2):
        n = abs(s1.peak.idx - s2.peak.idx)
        tof = n * self.dt
        v = self.distance / tof
        return v

    def analyseAll(self):
        analysed = []
        for sens in self.toAnalyze:
            if type(getattr(self.data, sens, False)) is not bool:
                a = self.analyseSignal(getattr(self.data, sens, False))
                analysed.append(a)
        return analysed

    def analyseSignal(self, signal):
        # create object to store data
        # this reinitilizing is needed to remove links
        a = AnalysedSignal()

        # get standard deviation and average of beginning
        a.std = np.std(signal[self.beginRange[0]:self.beginRange[1]])
        avg = np.mean(signal[self.beginRange[0]:self.beginRange[1]])

        # calculates how much a value deviates (positive) from the threshold
        def devAboveThreshold(s): return s-avg-self.sigmaFactor*a.std
        # find first significant increase, subtract safety factor
        a.ROIleft = indexOfFirst(signal, devAboveThreshold) - self.ROIsafety

        # base average on roi rather then beginning of signal
        avg = np.mean(signal[a.ROIleft-len(self.beginRange):a.ROIleft])
        # integrate the signal
        a.v = intFrom(signal, a.ROIleft, avg, self.dt)
        stdInV = np.std(a.v[a.ROIleft:a.ROIleft+self.stdLength])

        # guess a value for the peak
        peakSearch = a.v[a.ROIleft:]
        peakIdx = self.findPeak(peakSearch, self.sigmaFactor*stdInV)\
            + a.ROIleft
        peakVal = a.v[peakIdx]

        hwVal = (peakVal + avg)/2  # guess value for halfway point

        # threshold for halway points (guess)
        def threshold(s): return (s < hwVal)
        rhwIdx = indexOfFirst(a.v[peakIdx:], threshold) + peakIdx
        lhwIdx = peakIdx - indexOfFirst(a.v[:peakIdx], threshold,
                                        inverse=True)

        # true peak
        peakSearch = a.v[lhwIdx:rhwIdx]
        peakIdx, peakVal = max(enumerate(peakSearch),
                               key=operator.itemgetter(1))
        a.peak = PointOnGraph(peakIdx+lhwIdx, peakVal)

        # true halfway points
        hwVal = (a.peak.h)/2

        def threshold(s): return (s < hwVal)
        rhwIdx = indexOfFirst(a.v[a.peak.idx:], threshold) + peakIdx
        lhwIdx = indexOfFirst(a.v[:a.peak.idx], threshold,
                              inverse=True)
        a.hwLeft = PointOnGraph(lhwIdx, a.v[lhwIdx])
        a.hwRight = PointOnGraph(rhwIdx, a.v[rhwIdx])

        return a

    def findPeak(self, signal, threshold):
        maxTillNow = -float('Inf')
        for idx, n in enumerate(signal):
            if n > maxTillNow:
                maxTillNow = n
                maxIdx = idx
            if n < (maxTillNow - threshold):
                break
        return maxIdx


class Iterator():
    def __init__(self):

        # gat the directory containing data from the paths module
        self.dataDir = paths.getDataDir()
        # get the directory containing data from the paths module
        self.outFile = paths.getOutFile()

        # TODO make this into a loop
        # get one scope file
        for fname in os.listdir(self.dataDir):
            if fname.endswith('.scope'):
                break
        an = Analyzer(self.dataDir+fname)
        logobject(an)

if __name__ == '__main__':
    it = Iterator()
