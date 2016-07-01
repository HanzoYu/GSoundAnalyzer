"""
This python script is used to analyze raw granular sound propagation data.
This python script uses pyqt and pyqtgraph for interactiely plotting the data.
This script is modified based on a pyqtgraph example program "Plotting.py".

adapted to use the autoAnalyzer

-- Peidong Yu, Alex Kamphuis, 11/2015
"""

import os
import sys

# add paths to modules of autoanalyzer
# you need to change this on your system!
# TODO: make these paths relative
sys.path.append('/home/gg/Programming/GSoundAnalyzer/')
sys.path.append('/home/gg/Programming/GSoundAnalyzer/autoAnalyze')
sys.path.append('/home/gg/Programming/GSoundAnalyzer/autoAnalyze/helpers')
sys.path.append('/home/gg/Programming/GSoundAnalyzer/autoAnalyze/IO')
sys.path.append('/home/gg/Programming/GSoundAnalyzer/autoAnalyze/logs')

from classes import Analyzer
from logs import log, logobject

import numpy as np
from scipy import signal
import pyqtgraph as pg
import sys
from pyqtgraph.Qt import QtGui
from PyQt4 import QtCore
import argparse
import pyqtgraph.exporters

aYMin=-0.8
aYMax=0.8
vYMin= -0.00005
vYMax= 0.00005

# main class
class analyzerMainWindow(QtGui.QMainWindow):
    """Main window that includes all information needed to visualy analyze a scope file
    
    Attributes:
        an (Analyzer): Analyzer class used to get the automatically analized data
        analyzeButton1 (QPushButton): Analyze signal 1
        analyzeButton2 (QPushButton): Analyze signal 2
        anPlot1 (pyqtgraph.Qt.plot): Plot of data returned by analyzer
        anPlot2 (pyqtgraph.Qt.plot): Plot of data returned by analyzer
        anROI1 (TYPE): Region of interest (ROI) for signal 1
        anROI2 (TYPE): Region of interest (ROI) for signal 2
        Ap1 (float): Height of peak of signal 1
        Ap2 (float): Height of peak of signal 2
        ApBox1 (QtGui.QLineEdit): Placeholder for amplitude of peak
        ApBox2 (QtGui.QLineEdit): Placholder for amplitude of peak
        avg1 (float): Average value over region of interest
        avg2 (float): Average value over region of interest
        cw (QtGui.QWidget): Main widget
        D (float): Distance between sensors
        dataFileName (str): Name of file to be analyzed
        DBox (QtGui.QLineEdit): Placeholder for distance
        diffButton (QtGui.QPushButton): Button to perform differentiation
        DLabel (QtGui.QLabel): Label for distance
        exportButton (QtGui.QPushButton): Button to export
        exportLayout (QtGui.QVBoxLayout): Layout containex export and skip buttons
        f (float): Sample rate
        fBox (QtGui.QLineEdit): Box for sample rate
        filterCoreSize1 (int): size of lowpass (average) filter for signal 1
        filterCoreSize2 (int): size of lowpass (average) filter for signal 2
        filterCoreSizeBox1 (QtGui.QPushButton): Placeholder for filtersize
        filterCoreSizeBox2 (QtGui.QPushButton): Placeholder for filtersize
        filterLabel1 (QtGui.QLabel): label for filtersize
        filterLabel2 (QtGui.QLabel): Label for filtersize
        fLabel (QtGui.QLabel): Label for frequency
        generalLayout (Qlayout): Large layout over whole window
        glayout1 (Qlayout): Description
        glayout2 (Qlayout): Description
        glayoutInt (QtGui.QVBoxLayout): layout for integration/differentiation buttons
        groupBox1 (QtGui.QGroupBox): box for buttons
        groupBox2 (QtGui.QGroupBox): box for buttons
        groupBox3 (QtGui.QGroupBox): box for buttons
        groupBoxInt (QtGui.QGroupBox): Box for integration buttons
        groupBoxSave (QtGui.QGroupBox): box for save and export buttons
        hlayout0 (Qlayout): layout
        hlayout1 (Qlayout): layout
        hlayout2 (Qlayout): layout
        hlayout3 (Qlayout): layout
        hlayout4 (Qlayout): layout
        iBackHM1 (int): index of last halfway point of signal 1
        iBackHM2 (int): index of last halfway point of signal 2
        iFrontHM1 (int): index of first halfway point of signal 1
        iFrontHM2 (int): index of first halfway point of signal 2
        imax1 (int): index of selected ROI
        imax2 (int): index of selected ROI
        imin1 (int): index of selected ROI
        imin2 (int): index of selected ROI
        instructionLabel (QtGui.QLabel): label for instruction
        intButton (QtGui.QPushButton): Integration button
        intLevelBox (QtGui.QLineEdit): box contianing integration level
        intLevelLabel (QtGui.QLabel) label showing integration level
        intLevelNames (list): list of names of integration levels
        intLevelNo (int): level of integration
        ipeak1 (int): index of peak of signal 1
        ipeak2 (int): index of peak of signal 2
        keepPeakToggle1 (QtGui.QCheckBox): checkbox to lock a peak
        keepPeakToggle2 (QtGui.QCheckBox): checkbox to lock a peak
        label1 (TYPE): Description
        label10 (TYPE): Description
        label11 (TYPE): Description
        label12 (TYPE): Description
        label2 (TYPE): Description
        label3 (TYPE): Description
        label4 (TYPE): Description
        label5 (TYPE): Description
        label6 (TYPE): Description
        label7 (TYPE): Description
        label8 (TYPE): Description
        label9 (TYPE): Description
        loadButton (QtGui.QPushButton): Button to load a file
        loadedFileNameBox (QtGui.QLineEdit): Box that lists inputfile
        lr1 (LinearRegionItem): Region in graph 1
        lr2 (LinearRegionItem): Region on graph 2
        n (int): length of signal
        n01 (int): Description
        n02 (int): Description
        n0Box1 (TYPE): Description
        n0Box2 (TYPE): Description
        originalData1 (arrayLike): Data as read from file
        originalData2 (arrayLike): data as read from file
        outFile (TYPE): Output file (opened)
        plot1 (TYPE): Description
        plot10 (TYPE): Description
        plot2 (TYPE): Description
        plot3 (TYPE): Description
        plot4 (TYPE): Description
        plot5 (TYPE): Description
        plot6 (TYPE): Description
        plot7 (TYPE): Description
        plot8 (TYPE): Description
        plot9 (TYPE): Description
        pos1 (TYPE): Description
        pos2 (TYPE): Description
        pw1 (TYPE): Plot window 1
        pw2 (TYPE): Plot window 2
        rawA1 (arrayLike): Signal data to work with (most of the time this is plotted)
        rawA2 (arrayLike): Signal data to work with (most of the time this is plotted)
        regionBoundBox1 (TYPE): Description
        regionBoundBox2 (TYPE): Description
        ROILabel1 (TYPE): Description
        ROILabel2 (TYPE): Description
        s1 (float): Description
        s2 (float): Description
        sBox1 (TYPE): Description
        sBox2 (TYPE): Description
        section01 (TYPE): Description
        section02 (TYPE): Description
        section1 (TYPE): Description
        section2 (TYPE): Description
        skipButton (QtGui.QPushButton): Button to skip 
        speedAnalyzeButton (QtGui.QPushButton): Button to analyze speed
        t (arrayLike): time vector
        tf (float): Description
        tfBox (TYPE): Description
        tp1 (float): Description
        tp2 (float): Description
        tpBox1 (TYPE): Description
        tpBox2 (TYPE): Description
        vel1 (arrayLike): 1-time integrated signal
        vel2 (arrayLike): 1-time integrated signal
        vlayout1 (TYPE): Description
        vlayout2 (TYPE): Description
        vlayout3 (TYPE): Description
        vlayout4 (TYPE): Description
        vlayout5 (TYPE): Description
        vlayout6 (TYPE): Description
        vs (float): Description
        vsBox (TYPE): Description
        wp1 (float): width of peak 1
        wp2 (float): width of peak 2
        wpBox1 (TYPE): Box to keep width
        wpBox2 (TYPE): Box to keep width
    """
    def __init__(self, inFile=None, outFile=None, imgFile=None):
        """Starts the analyzer
        
        Args:
            inFile (string, optional): Name of input file
            outFile (string, optional): Name of output file
        """
        super().__init__()
        self.initUI()

        if ((inFile is not None) and (outFile is not None) and (imgFile is not None)):
            self.loadFile(inFile)
            self.setOutputFile(outFile)
            self.setImgFileName(imgFile)
            self.imgFileFromArugumentFlag = True
        else:
            self.imgFileFromArugumentFlag = False

    def initUI(self):
        """Create the GUI
        
        Returns:
            TYPE: UI object
        """
        self.resize(1000, 1000)
        self.setWindowTitle('Granular Sound Data Analyzer')
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        pg.setConfigOptions(antialias=True)

        # Defining variables
        self.section1 = np.zeros(1)
        self.section01 = np.zeros(1)
        self.D = 4.85  # Distance between two sensors
        self.avg1 = 0.0  # Zero level
        self.avg2 = 0.0
        self.ipeak1 = -1  # -1 flags that peak has not been detected 
        self.ipeak2 = -1  # -1 flags that peak has not been detected 
        self.iFrontHM1 = 0
        self.iFrontHM2 = 0
        self.iBackHM1 = 0
        self.iBackHM2 = 0
        self.Ap1 = 0.0
        self.wp1 = 0.0
        self.tp1 = 0.0
        self.Ap2 = 0.0
        self.wp2 = 0.0
        self.tp2 = 0.0
        self.filterCoreSize1 = 1
        self.filterCoreSize2 = 1
        self.tf = 0.0
        self.vs = 0.0
        self.plotYMax = 1.0
        self.plotYMin = 0.0

        # Defining layouts and groups
        self.generalLayout = QtGui.QVBoxLayout()
        self.cw.setLayout(self.generalLayout)
        self.hlayout0 = QtGui.QHBoxLayout()
        self.generalLayout.addLayout(self.hlayout0)
        self.hlayout1 = QtGui.QHBoxLayout()
        self.generalLayout.addLayout(self.hlayout1)
        self.hlayout2 = QtGui.QHBoxLayout()
        self.generalLayout.addLayout(self.hlayout2)
        self.hlayout3 = QtGui.QHBoxLayout()
        self.generalLayout.addLayout(self.hlayout3)
        self.hlayout4 = QtGui.QHBoxLayout()
        self.generalLayout.addLayout(self.hlayout4)
        self.vlayout1 = QtGui.QVBoxLayout()
        self.vlayout2 = QtGui.QVBoxLayout()
        self.vlayout3 = QtGui.QVBoxLayout()
        self.vlayout4 = QtGui.QVBoxLayout()
        self.vlayout5 = QtGui.QVBoxLayout()
        self.groupBox1 = QtGui.QGroupBox('Sensor #1')
        self.groupBox2 = QtGui.QGroupBox('Sensor #2')
        self.groupBox3 = QtGui.QGroupBox('1 to 2')
        self.groupBoxInt = QtGui.QGroupBox('Int./diff.')  # int. container
        self.groupBoxSave = QtGui.QGroupBox('Export Data')  # save container
        self.groupBoxImgSave = QtGui.QGroupBox('Export Images')  # export images
        self.glayout1 = QtGui.QGridLayout()
        self.glayout2 = QtGui.QGridLayout()
        self.glayoutInt = QtGui.QGridLayout()  # int. grid layout
        self.vlayout6 = QtGui.QVBoxLayout()  # save/int splitter
        self.vlayout7 = QtGui.QVBoxLayout()  # Export images

        # Defining widgets on different layers
        # Layer1
        self.instructionLabel = QtGui.QLabel('Instruction: ...')
        self.hlayout0.addWidget(self.instructionLabel)
        self.loadButton = QtGui.QPushButton('Load Data', self.cw)
        self.hlayout1.addWidget(self.loadButton)
        self.loadedFileNameBox = QtGui.QLineEdit('Data Filename')
        self.loadedFileNameBox.setReadOnly(True)
        self.hlayout1.addWidget(self.loadedFileNameBox)
        self.ROILabel1 = QtGui.QLabel('ROI in plot1')
        self.ROILabel2 = QtGui.QLabel('ROI in plot2')
        self.regionBoundBox1 = QtGui.QLineEdit('')
        self.regionBoundBox2 = QtGui.QLineEdit('')
        self.f = 1e6
        self.fLabel = QtGui.QLabel('Sampling Rate')
        self.fBox = QtGui.QLineEdit('%d' % self.f)
        self.DLabel = QtGui.QLabel('Distance (cm):')
        self.DBox = QtGui.QLineEdit('%f' % self.D)

        # Layer2
        self.keepPeakToggle1 = QtGui.QCheckBox('Lock peak 1', self)
        self.analyzeButton1 = QtGui.QPushButton('Analyze peak 1', self)
        self.filterLabel1 = QtGui.QLabel('medfilt core size')
        self.filterCoreSizeBox1 = QtGui.QLineEdit(
            ('%d' % self.filterCoreSize1))
        self.label1 = QtGui.QLabel('s1 (mV/m*s^-2):')
        self.s1 = 9.645
        self.sBox1 = QtGui.QLineEdit(('%f' % self.s1))
        self.label2 = QtGui.QLabel('n01:')
        self.n01 = 50
        self.n0Box1 = QtGui.QLineEdit(('%d' % self.n01))
        self.label3 = QtGui.QLabel('Ap1 (V):')
        self.ApBox1 = QtGui.QLineEdit('%f' % self.Ap1)
        self.ApBox1.setReadOnly(True)
        self.label4 = QtGui.QLabel('wp1 (ms):')
        self.wpBox1 = QtGui.QLineEdit(('%f' % self.wp1))
        self.wpBox1.setReadOnly(True)
        self.label5 = QtGui.QLabel('tp1 (ms):')
        self.tpBox1 = QtGui.QLineEdit(('%f' % self.tp1))
        self.tpBox1.setReadOnly(True)

        self.keepPeakToggle2 = QtGui.QCheckBox('Lock peak 2', self)
        self.analyzeButton2 = QtGui.QPushButton('Analyze peak 2', self)
        self.filterLabel2 = QtGui.QLabel('medfilt core size')
        self.filterCoreSizeBox2 = QtGui.QLineEdit((
            '%d' % self.filterCoreSize2))
        self.label6 = QtGui.QLabel('s2 (mV/m*s^-2):')
        self.s2 = 99.65
        self.sBox2 = QtGui.QLineEdit(('%f' % self.s2))
        self.label7 = QtGui.QLabel('n02:')
        self.n02 = 50
        self.n0Box2 = QtGui.QLineEdit(('%d' % self.n02))
        self.label8 = QtGui.QLabel('Ap2 (V):')
        self.ApBox2 = QtGui.QLineEdit('%f' % self.Ap2)
        self.ApBox2.setReadOnly(True)
        self.label9 = QtGui.QLabel('wp2 (ms):')
        self.wpBox2 = QtGui.QLineEdit(('%f' % self.wp2))
        self.wpBox2.setReadOnly(True)
        self.label10 = QtGui.QLabel('tp2 (ms):')
        self.tpBox2 = QtGui.QLineEdit(('%f' % self.tp2))
        self.tpBox2.setReadOnly(True)

        self.speedAnalyzeButton = QtGui.QPushButton('Analyze Speed', self.cw)
        self.label11 = QtGui.QLabel('time of flight (ms):')
        self.tf = 0.0
        self.tfBox = QtGui.QLineEdit(('%f' % self.tf))
        self.tfBox.setReadOnly(True)
        self.vs = 0.0
        self.vsBox = QtGui.QLineEdit(('%f' % self.vs))
        self.vsBox.setReadOnly(True)
        self.label12 = QtGui.QLabel('speed of sound (m/s):')
        # integration part
        self.intLevelLabel = QtGui.QLabel('Current level:')  # lbl with lvl
        self.intLevelBox = QtGui.QLineEdit('Original Data')  # print level here
        self.intLevelBox.setReadOnly(True)  # set level box uneditable
        self.intButton = QtGui.QPushButton(  # integration button
            'Integrate', self.cw)
        self.diffButton = QtGui.QPushButton(  # differentiation button
            'Diff. (undo Int.)',
            self.cw
            )
        self.diffButton.setEnabled(False)  # start with diff butten disabled
        self.intLevelNames = ['Original Data',  # list of level names
                              'Velocity (1 time int)',
                              'Position (2 times int)']
        self.intLevelNo = 0  # number of current integration level
        # export button
        self.exportButton = QtGui.QPushButton('Export and exit', self.cw)
        self.skipButton = QtGui.QPushButton('Skip and exit', self.cw)
        self.exportLayout = QtGui.QGridLayout()

        # image export buttons
        self.imgExportButton = QtGui.QPushButton('Export the Plot', self.cw)
        self.label13 = QtGui.QLabel('ymax on lower plot')
        self.plotYMaxBox = QtGui.QLineEdit('%f' % self.plotYMax)
        self.label14 = QtGui.QLabel('ymin on lower plot')
        self.plotYMinBox = QtGui.QLineEdit('%f' % self.plotYMin)
        self.imgExportLayout = QtGui.QGridLayout()
        

        # Arranging widgets and layouts
        self.hlayout1.addWidget(self.ROILabel1)
        self.hlayout1.addWidget(self.regionBoundBox1)
        self.hlayout1.addWidget(self.ROILabel2)
        self.hlayout1.addWidget(self.regionBoundBox2)
        self.hlayout1.addWidget(self.fLabel)
        self.hlayout1.addWidget(self.fBox)

        self.hlayout2.addWidget(self.groupBox1)
        self.hlayout2.addWidget(self.groupBox2)
        self.hlayout2.addWidget(self.groupBox3)
        self.hlayout2.addLayout(self.vlayout6)
        self.hlayout2.addLayout(self.vlayout7)
        self.vlayout6.addWidget(self.groupBoxInt)
        self.vlayout6.addWidget(self.groupBoxSave)
        self.vlayout7.addWidget(self.groupBoxImgSave)

        self.glayout1.addWidget(self.keepPeakToggle1, 0, 0)
        self.glayout1.addWidget(self.filterLabel1, 1, 0)
        self.glayout1.addWidget(self.filterCoreSizeBox1, 2, 0)
        self.glayout1.addWidget(self.label1, 3, 0)
        self.glayout1.addWidget(self.sBox1, 4, 0)
        self.glayout1.addWidget(self.label2, 5, 0)
        self.glayout1.addWidget(self.n0Box1, 6, 0)

        self.glayout1.addWidget(self.analyzeButton1, 0, 1)
        self.glayout1.addWidget(self.label3, 1, 1)
        self.glayout1.addWidget(self.ApBox1, 2, 1)
        self.glayout1.addWidget(self.label4, 3, 1)
        self.glayout1.addWidget(self.wpBox1, 4, 1)
        self.glayout1.addWidget(self.label5, 5, 1)
        self.glayout1.addWidget(self.tpBox1, 6, 1)
        self.groupBox1.setLayout(self.glayout1)

        self.glayout2.addWidget(self.keepPeakToggle2, 0, 0)
        self.glayout2.addWidget(self.filterLabel2, 1, 0)
        self.glayout2.addWidget(self.filterCoreSizeBox2, 2, 0)
        self.glayout2.addWidget(self.label6, 3, 0)
        self.glayout2.addWidget(self.sBox2, 4, 0)
        self.glayout2.addWidget(self.label7, 5, 0)
        self.glayout2.addWidget(self.n0Box2, 6, 0)

        self.glayout2.addWidget(self.analyzeButton2, 0, 1)
        self.glayout2.addWidget(self.label8, 1, 1)
        self.glayout2.addWidget(self.ApBox2, 2, 1)
        self.glayout2.addWidget(self.label9, 3, 1)
        self.glayout2.addWidget(self.wpBox2, 4, 1)
        self.glayout2.addWidget(self.label10, 5, 1)
        self.glayout2.addWidget(self.tpBox2, 6, 1)
        self.groupBox2.setLayout(self.glayout2)

        self.vlayout1.addWidget(self.speedAnalyzeButton)
        self.vlayout1.addWidget(self.DLabel)
        self.vlayout1.addWidget(self.DBox)
        self.vlayout1.addWidget(self.label11)
        self.vlayout1.addWidget(self.tfBox)
        self.vlayout1.addWidget(self.label12)
        self.vlayout1.addWidget(self.vsBox)
        self.groupBox3.setLayout(self.vlayout1)

        # integration layout
        self.glayoutInt.addWidget(self.intButton, 1, 1, 1, 2)
        self.glayoutInt.addWidget(self.intLevelLabel, 2, 1, 1, 1)
        self.glayoutInt.addWidget(self.intLevelBox, 2, 2, 1, 1)
        self.glayoutInt.addWidget(self.diffButton, 3, 1, 1, 2)
        self.groupBoxInt.setLayout(self.glayoutInt)

        # save button layout
        self.groupBoxSave.setLayout(self.exportLayout)
        self.exportLayout.addWidget(self.exportButton, 0, 0)
        self.exportLayout.addWidget(self.skipButton, 2, 0)

        # image export layout
        self.groupBoxImgSave.setLayout(self.imgExportLayout)
        self.imgExportLayout.addWidget(self.imgExportButton)
        self.imgExportLayout.addWidget(self.label13)
        self.imgExportLayout.addWidget(self.plotYMaxBox)
        self.imgExportLayout.addWidget(self.label14)
        self.imgExportLayout.addWidget(self.plotYMinBox)
        

        # Defining graph widget
        self.pw1 = pg.PlotWidget(name='Plot1')
        self.generalLayout.addWidget(self.pw1)
        self.pw2 = pg.PlotWidget(name='Plot2')
        self.generalLayout.addWidget(self.pw2)
        self.lr1 = pg.LinearRegionItem([4.0, 6.5])
        self.lr2 = pg.LinearRegionItem([5.0, 5.5])
        self.lr1.setZValue(-10)
        self.pw1.addItem(self.lr1)
        self.pw2.addItem(self.lr2)

        # Defining plots
        self.plot1 = self.pw1.plot(np.linspace(0, 25, 25000), np.ones(25000),
                                   pen=pg.mkPen('w'))
        self.plot2 = self.pw1.plot(np.linspace(0, 25, 25000), np.zeros(25000),
                                   pen=pg.mkPen('r'))
        self.plot3 = self.pw2.plot(np.linspace(0, 25, 25000), np.ones(25000),
                                   pen=pg.mkPen('w'))
        self.plot4 = self.pw2.plot(np.linspace(0, 25, 25000), np.zeros(25000),
                                   pen=pg.mkPen('r'))
        self.plot5 = self.pw2.plot(np.linspace(0, 25, 25000), np.ones(25000),
                                   pen=pg.mkPen('c'))
        self.plot7 = self.pw2.plot(np.linspace(0, 25, 25000), np.zeros(25000),
                                   pen=pg.mkPen('y'))
        self.plot6 = self.pw2.plot(np.linspace(0, 25, 25000), np.ones(25000),
                                   pen=pg.mkPen('b'))
        self.plot8 = self.pw2.plot(np.linspace(0, 25, 25000), np.zeros(25000),
                                   pen=pg.mkPen('m'))
        self.plot9 = self.pw2.plot([5.25], [0.5], symbolBrush=('w'),
                                   symbolSize=5)
        self.plot10 = self.pw2.plot([5.25], [0.3], symbolBrush=('r'),
                                    symbolSize=5)

        self.min1, self.max1 = self.lr1.getRegion()
        self.min2, self.max2 = self.lr2.getRegion()
        self.regionBoundBox1.setText("(%f, %f) ms" % (self.min1, self.max1))
        self.regionBoundBox2.setText("(%f, %f) ms" % (self.min2, self.max2))

        self.show()

        # defining events
        self.loadButton.clicked.connect(self.showLoadFileDialog)
        self.sBox1.editingFinished.connect(self.updateS1)
        self.sBox2.editingFinished.connect(self.updateS2)
        self.n0Box1.editingFinished.connect(self.updateN01)
        self.n0Box2.editingFinished.connect(self.updateN02)
        self.fBox.editingFinished.connect(self.updateF)
        self.DBox.editingFinished.connect(self.updateD)
        self.filterCoreSizeBox1.editingFinished.connect(
            self.updateFilterCoreSize1)
        self.filterCoreSizeBox2.editingFinished.connect(
            self.updateFilterCoreSize2)
        self.speedAnalyzeButton.clicked.connect(self.analyzeSpeed)

        self.analyzeButton1.clicked.connect(self.analyzePeak1)
        self.analyzeButton2.clicked.connect(self.analyzePeak2)

        # for integration (AK)
        self.intButton.clicked.connect(self.integrate)
        self.diffButton.clicked.connect(self.differentiate)

        # save/export/check
        self.exportButton.clicked.connect(self.writeOut)
        self.skipButton.clicked.connect(self.skipOutput)

        # image export
        self.imgExportButton.clicked.connect(self.imgExport)
        self.plotYMaxBox.editingFinished.connect(self.updatePlotYMax)
        self.plotYMinBox.editingFinished.connect(self.updatePlotYMin)
        

    def keyPressEvent(self, e):
        """Handler for keypressed events, used for making keyboard shortcuts
        
        Args:
            e (keyPressEvent): event
        
        Returns:
            None: Nonetype
        """
        # Q does skip
        if e.key() == QtCore.Qt.Key_Q:
            # QtGui.QMessageBox.about(self, "Q key pressed", "its pressed")
            self.skipOutput()

        # F writes output
        if e.key() == QtCore.Qt.Key_F:
            # QtGui.QMessageBox.about(self, "F key pressed", "f")
            self.writeOut()
            self.checkOutput()

        # E integrates
        if e.key() == QtCore.Qt.Key_E:
            self.integrate()

        # D differentiates
        if e.key() == QtCore.Qt.Key_D:
            self.differentiate()

        # S export image
        if e.key() == QtCore.Qt.Key_S:
            self.imgExport()

    def loadFile(self, inFile):
        """Load a file (using the showLoadFileDialog function)
        
        Args:
            inFile (str): name of file to load
        
        Returns:
            None: Description
        """
        path = os.path.abspath(inFile)
        print('checking for file:', path)
        if os.path.exists(path):
            self.showLoadFileDialog(path)

            self.an = Analyzer(inFile)
            self.plotAnalyzer()
            begin = self.an.analysedSignals[0].ROIleft/1000
            end = (self.an.analysedSignals[1].hwRight.idx + 50)/1000
            self.lr2.setRegion([begin, end])
            self.integrate()
        else:
            QtGui.QMessageBox.about(self, "Input file does not exist.", "Specified input file: %s does not exist. Data not read." % (inFile))

    def setOutputFile(self, outFile):
        """Open a file for writing output
        
        Args:
            outFile (str): Name of output file
        
        Returns:
            None: Description
        """
        path = os.path.abspath(outFile)
        self.outFile = open(path, 'a')

    def setImgFileName(self, imgFile):
        """setting image filename for exporting the plot
        
        Args:
            imgFile (str): Name of the image file
        
        Returns:
            None: Description
        """
        path = os.path.abspath(imgFile)
        self.imgFileFlag = open(path, 'w')    


    def imgExport(self):       
        """Export Images with predefined filename and yrange
        
        Returns:
            None: Description
        """
        """
        if not hasattr(self, 'imgFileFlag'):
            imgFile = QtGui.QFileDialog.getOpenFileName(
                self, 'Open file',
                '/home/gg/GraSound/PFC2015/Analysis/')
            #self.setImgFileName(imgFile)"""

        if self.intLevelNo is 0:
            self.plotYMin = aYMin
            self.plotYMax = aYMax
            self.plotYMinBox.setText('%f' % self.plotYMin)
            self.plotYMaxBox.setText('%f' % self.plotYMax)
            self.updatePlotYMin()
            self.updatePlotYMax()
            #imgFile.replace(".png", "_a.png")
        if self.intLevelNo is 1:
            self.plotYMin = vYMin
            self.plotYMax = vYMax
            self.plotYMinBox.setText('%f' % self.plotYMin)
            self.plotYMaxBox.setText('%f' % self.plotYMax)
            self.updatePlotYMin()
            self.updatePlotYMax()
            #imgFile=imgFile.replace(".png", "_v.png")

        print ("Exporting to %s" % imgFile)
        imgExporter = pg.exporters.ImageExporter(self.pw2.plotItem)
        if self.intLevelNo is 0:
            imgExporter.export(imgFile.replace(".png", "_a.png"))
        if self.intLevelNo is 1:
            imgExporter.export(imgFile.replace(".png", "_v.png"))

        #if self.intLevelNo is 0

    def writeOut(self):
        """Write the information to file and exit
        
        Returns:
            None: Description
        """
        if not hasattr(self, 'outFile'):            
            outFileName = QtGui.QFileDialog.getOpenFileName(
                self, 'Open file',
                '/home/gg/GraSound/PFC2015/Data/')
            self.setOutputFile(outFileName)

        # replace data in analyzer
        self.an.analysedSignals[0].hwLeft.idx = self.iFrontHM1 + int(self.min2*1000)
        self.an.analysedSignals[0].hwLeft.h = self.rawA1[self.iFrontHM1 + int(self.min2*1000)]

        self.an.analysedSignals[0].peak.idx = self.ipeak1 + self.imin1
        self.an.analysedSignals[0].peak.h = self.Ap1

        self.an.analysedSignals[0].hwRight.idx = self.iBackHM1 + int(self.min2*1000)
        self.an.analysedSignals[0].hwRight.h = self.rawA1[self.iBackHM1 + int(self.min2*1000)]

        self.an.analysedSignals[1].hwLeft.idx = self.iFrontHM2 + int(self.min2*1000)
        self.an.analysedSignals[1].hwLeft.h = self.rawA2[self.iFrontHM2 + int(self.min2*1000)]

        self.an.analysedSignals[1].peak.idx = self.ipeak2 + self.imin2
        self.an.analysedSignals[1].peak.h = self.Ap2

        self.an.analysedSignals[1].hwRight.idx = self.iBackHM2 + int(self.min2*1000)
        self.an.analysedSignals[1].hwRight.h = self.rawA2[self.iBackHM2 + int(self.min2*1000)]

        # mage analyzer update speed and widths
        self.an.widths = self.an.calcWidths()
        self.an.v = self.an.calcSpeed(self.an.analysedSignals[0], self.an.analysedSignals[1])

        #toWrite = self.an.writeOut() + '\n'
        toWrite = self.an.writeOut() + ' '

        # write to file
        self.outFile.write(toWrite)

        # feedback
        # QtGui.QMessageBox.about(self, "Done!", "Data is written.")

        # exit
        #sys.exit(app.exec_())

    def skipOutput(self):
        """Exit without writing
        
        Returns:
            None: Description
        """
        self.outFile.write('\n')
        sys.exit(app.exec_())

    def getIntegratedData(self, data, dt):
        """Integrates data once and returns the running integral
        currently uses a 2nd order accurate approximation
        may be improved later
        
        Args:
            data (arrayLike): Vector to integrate
            dt (float): timestep size
        """
        intContributions = (data[:-1]+data[1:])*dt/2
        intContributions = np.insert(intContributions, 0, 0)
        runningInt = np.cumsum(intContributions)
        return runningInt

    # method to integrate raw acceleration data
    def integrate(self):
        """Calls integration function, keeps track of integration level
        
        Returns:
            None: Description
        """
        if self.intLevelNo is 0:
            # refuse if peaks are not set
            if (self.ipeak1 == -1) or (self.ipeak2 == -1):
                QtGui.QMessageBox.about(self, "Set peaks first.",
                                        "Analyze peaks for both signals first."
                                        "The data is needed to find the "
                                        "integration constant.")
                return

            # keep track of integration level
            self.intLevelNo = self.intLevelNo + 1
            self.diffButton.setEnabled(True)
            self.updateIntLevelLabel()
            # remove detected peak data
            self.ipeak1 = -1
            self.ipeak2 = -1

            # integration - signal 1
            dt = 1/self.f  # timestep size
            beginIdx = int(self.min2*1000+0.5)  # begin index of signal
            # self.n01 -> position of begin
            # self.avg1 -> 0-heigth 
            secToIntegrate = self.rawA1[beginIdx:] - self.avg1
            intI1 = self.getIntegratedData(secToIntegrate, dt)
            tempInt = np.linspace(0, 0, num=(self.n - len(intI1)))
            intI1 = np.concatenate((tempInt, intI1))

            # plotting
            self.clearAllPlots()

            self.plot1 = self.pw1.plot(self.t, intI1, pen=pg.mkPen('w'))
            self.plot3 = self.pw2.plot(self.t, intI1, pen=pg.mkPen('w'))

            # integration - signal 2
            secToIntegrate = self.rawA2[beginIdx:] - self.avg2
            intI2 = self.getIntegratedData(secToIntegrate, dt)
            tempInt = np.linspace(0, 0, num=(self.n - len(intI2)))
            intI2 = np.concatenate((tempInt, intI2))

            # plotting
            self.plot2 = self.pw1.plot(self.t, intI2, pen=pg.mkPen('r'))
            self.plot4 = self.pw2.plot(self.t, intI2, pen=pg.mkPen('r'))

            # save data
            self.originalData1 = self.rawA1
            self.originalData2 = self.rawA2
            # replace with new integrated data
            self.rawA1 = intI1
            self.rawA2 = intI2
            # save velocity data as well
            self.vel1 = intI1
            self.vel2 = intI2

            # update y scale
            self.autoScaleY()

            # auto calc peaks
            self.updateAnalyzer()

        elif self.intLevelNo is 1:
            # keep track of integration level
            self.intLevelNo = self.intLevelNo + 1
            self.intButton.setEnabled(False)
            self.updateIntLevelLabel()

            # integration
            dt = 1/self.f
            intI1 = self.getIntegratedData(self.rawA1, dt)
            intI2 = self.getIntegratedData(self.rawA2, dt)

            # plotting
            self.clearAllPlots()
            self.plot1 = self.pw1.plot(self.t, intI1, pen=pg.mkPen('w'))
            self.plot3 = self.pw2.plot(self.t, intI1, pen=pg.mkPen('w'))
            self.plot2 = self.pw1.plot(self.t, intI2, pen=pg.mkPen('r'))
            self.plot4 = self.pw2.plot(self.t, intI2, pen=pg.mkPen('r'))

            # save data
            self.pos1 = intI1
            self.pos2 = intI2
            # update working data
            self.rawA1 = intI1
            self.rawA2 = intI2

            # update y scale
            self.autoScaleY()

            # auto calc peaks
            self.updateAnalyzer()

        else:  # error message for testing, should never be thrown
            QtGui.QMessageBox.about(self, "Max. integration level reached",
                                    "Integration beyond position (two times"
                                    " integration) is not implemented.")

    def differentiate(self):
        """Undo integration (places back original data)
        
        Returns:
            None: Description
        """
        if self.intLevelNo is 2:
            # keep track of integration level
            self.intLevelNo = self.intLevelNo - 1
            self.intButton.setEnabled(True)
            self.updateIntLevelLabel()

            # in stead of differentiation we just set back the original velocity data,
            self.rawA1 = self.vel1
            self.rawA2 = self.vel2
            # plotting
            self.clearAllPlots()
            self.plot1 = self.pw1.plot(self.t, self.rawA1, pen=pg.mkPen('w'))
            self.plot2 = self.pw1.plot(self.t, self.rawA2, pen=pg.mkPen('r'))
            self.plot3 = self.pw2.plot(self.t, self.rawA1, pen=pg.mkPen('w'))
            self.plot4 = self.pw2.plot(self.t, self.rawA2, pen=pg.mkPen('r'))
            self.autoScaleY()

            # auto calc peaks
            self.updateAnalyzer()

        elif self.intLevelNo is 1:
            # keep track of integration level
            self.intLevelNo = self.intLevelNo -1
            self.diffButton.setEnabled(False)
            self.updateIntLevelLabel()

            # in stead of differentiation we just set back original data
            self.rawA1 = self.originalData1
            self.rawA2 = self.originalData2
            # plotting
            self.clearAllPlots()
            self.plot1 = self.pw1.plot(self.t, self.rawA1, pen=pg.mkPen('w'))
            self.plot2 = self.pw1.plot(self.t, self.rawA2, pen=pg.mkPen('r'))
            self.plot3 = self.pw2.plot(self.t, self.rawA1, pen=pg.mkPen('w'))
            self.plot4 = self.pw2.plot(self.t, self.rawA2, pen=pg.mkPen('r'))
            self.autoScaleY()

            # auto calc peaks
            self.updateAnalyzer()

        else:  # error message for testing, should never be thrown
            QtGui.QMessageBox.about(self, "Max. differentiation level reache",
                                    "Differentation beyond original data"
                                    "is not implemented.")

    def clearAllPlots(self):
        """Clear all plots of data (not analyzer plots)
        
        Returns:
            None: Description
        """
        self.pw1.removeItem(self.plot1)
        self.pw1.removeItem(self.plot2)

        self.pw2.removeItem(self.plot3)
        self.pw2.removeItem(self.plot4)
        self.pw2.removeItem(self.plot5)
        self.pw2.removeItem(self.plot6)
        self.pw2.removeItem(self.plot7)
        self.pw2.removeItem(self.plot8)
        self.pw2.removeItem(self.plot9)
        self.pw2.removeItem(self.plot10)

    def updateIntLevelLabel(self, updateAllLabels=True):
        """Check the integration level and put it in the label
        
        Args:
            updateAllLabels (bool, optional): Toggle to only update the level label, or also unit labels
        
        Returns:
            None: Description
        """
        self.intLevelBox.setText(self.intLevelNames[self.intLevelNo])

        # update other labels in requested

        if updateAllLabels:
            # create dictionaries
            dicts = []
            intlvl = {'Ap1': 'V', 'Ap2': 'V'}
            dicts.append(intlvl)
            intlvl = {'Ap1': '~V.s', 'Ap2': '~V.s'}
            dicts.append(intlvl)
            intlvl = {'Ap1': '~V.s^2', 'Ap2': '~V.s^2'}
            dicts.append(intlvl)
            currentDict = dicts[self.intLevelNo]
            self.label3.setText('Ap1 (' + currentDict['Ap1'] + ')')
            self.label8.setText('Ap2 (' + currentDict['Ap2'] + ')')

    # methods to update values from text boxes
    def updateS1(self):
        """Read S1
        
        Returns:
            None: Description
        """
        self.s1 = float(self.sBox1.text())

    def updateS2(self):
        """Read S2
        
        Returns:
            None: Description
        """
        self.s2 = float(self.sBox2.text())

    def updateN01(self):
        """Update region N01
        
        Returns:
            None: Description
        """
        self.n01 = float(self.n0Box1.text())

    def updateN02(self):
        """update region N02
        
        Returns:
            None: Description
        """
        self.n02 = float(self.n0Box2.text())

    def updateF(self):
        """Update the frequency
        
        Returns:
            None: Description
        """
        self.f = float(self.fBox.text())

    def updateD(self):
        """Update the distance
        
        Returns:
            None: Description
        """
        self.D = float(self.DBox.text())
        
    def updatePlotYMax(self):
        """Update plotYMax
        
        Returns:
            None: Description
        """
        self.plotYMax = float(self.plotYMaxBox.text())
        self.updatePlotYRange()

    def updatePlotYMin(self):
        """Update plotYMin
        
        Returns:
            None: Description
        """
        self.plotYMin = float(self.plotYMinBox.text())
        self.updatePlotYRange()

    def updateFilterCoreSize1(self):
        """Update filter size of signal 1
        
        Returns:
            None: Description
        """
        if float(self.filterCoreSizeBox1.text()) % 2 == 0:
            self.filterCoreSize1 = int(float(self.filterCoreSizeBox1.text()))-1
            self.filterCoreSizeBox1.setText('%d' % self.filterCoreSize1)
        else:
            self.filterCoreSize1 = int(float(self.filterCoreSizeBox1.text()))

    def updateFilterCoreSize2(self):
        """pdat filter size of signal 2
        
        Returns:
            None: Description
        """
        if float(self.filterCoreSizeBox2.text()) % 2 == 0:
            self.filterCoreSize2 = int(float(self.filterCoreSizeBox2.text()))-1
            self.filterCoreSizeBox2.setText('%d' % self.filterCoreSize2)
        else:
            self.filterCoreSize2 = int((self.filterCoreSizeBox2.text()))

    def updatePlot(self):
        """method to update the xrange of plot2 whenever ROI is changed in the plot1
        
        Returns:
            None: Description
        """
        self.pw2.setXRange(*self.lr1.getRegion(), padding=0)
        self.min1, self.max1 = self.lr1.getRegion()
        self.regionBoundBox1.setText("(%f, %f) ms" % (self.min1, self.max1))

    def updatePlotYRange(self):        
        """method to update the yrange of plot2 whenever the plotYMax and plotYMin changed, used mainly for exporting plots
        
        Returns:
            None: Description
        """
        
        self.pw2.setYRange(self.plotYMin, self.plotYMax, padding = 0, update = True)


    def updateRegion(self):
        """method to update the plot1 whenever xrange is changed in the plot2
        
        Returns:
            None: Description
        """
        self.lr1.setRegion(self.pw2.getViewBox().viewRange()[0])

    def updateAnalyzer(self):
        """Update the region of interest
        
        Returns:
            None: Description
        """
        self.min2, self.max2 = self.lr2.getRegion()
        self.regionBoundBox2.setText("(%f, %f) ms" % (self.min2, self.max2))

        # auto analyze peaks when region changes
        if not self.keepPeakToggle1.isChecked():
            self.analyzePeak1()
        if not self.keepPeakToggle2.isChecked():
            self.analyzePeak2()
        # auto calc wavespeed if peaks are set
        if not ((self.ipeak1 == -1) or (self.ipeak2 == -1) ):
            self.analyzeSpeed()


    def autoScaleY(self):
        """Autoscale only the y-axis
        
        Returns:
            None: Description
        """
        ymin = min(min(self.rawA1), min(self.rawA2))
        ymax = max(max(self.rawA1), max(self.rawA2))
        self.pw1.setYRange(ymin, ymax)
        self.pw2.setYRange(ymin, ymax)

    def analyzePeak1(self):
        """Analyze the peak in the selected region for signal 1
        
        Returns:
            None: Description
        """
        # Retrieving ROI data
        self.imin1 = int(self.min2*1000+0.5)
        self.imax1 = int(self.max2*1000+0.5)
        self.pw2.removeItem(self.plot5)
        self.pw2.removeItem(self.plot6)
        self.pw2.removeItem(self.plot9)
        if self.filterCoreSize1 <= 1:
            self.section1 = self.rawA1[self.imin1:self.imax1]
        else:
            self.section1 = signal.medfilt(self.rawA1[self.imin1:self.imax1],
                                           self.filterCoreSize1)

        # Finding zero point
        self.section01 = self.section1[0:self.n01]
        self.avg1 = np.mean(self.section01)
        self.plot5 = self.pw2.plot(np.linspace(self.min2,
                                   self.min2+self.n01/self.f*1000,
                                   self.n01), np.ones(self.n01)*self.avg1,
                                   pen=pg.mkPen('c', width=2))

        # Finding maximum point
        self.ipeak1 = np.argmax(self.section1)
        self.Ap1 = np.amax(self.section1) - self.avg1

        # Finding half maximum points
        for i in range(0, self.ipeak1):
            if self.section1[i] >= self.Ap1*0.5+self.avg1:
                break
        self.iFrontHM1 = i
        self.tp1 = self.iFrontHM1/1000.0+self.min2

        for i in range(self.ipeak1, self.imax1-self.imin1):
            if self.section1[i] <= self.Ap1*0.5+self.avg1:
                break
        self.iBackHM1 = i
        self.wp1 = (self.iBackHM1-self.iFrontHM1)/1000.0

        # Visualization
        self.plot6 = self.pw2.plot(np.linspace(self.tp1, self.tp1+self.wp1, self.iBackHM1-self.iFrontHM1), self.section1[self.iFrontHM1:self.iBackHM1], pen=pg.mkPen('b',width=2))
        self.plot9 = self.pw2.plot([self.tp1, self.ipeak1/1000.0+self.min2, self.tp1+self.wp1],[self.Ap1*0.5+self.avg1, self.Ap1+self.avg1, self.Ap1*0.5+self.avg1], pen=None, symbolBrush=('b'), symbolSize=7)

        # Updating results in the TextBoxs
        self.ApBox1.setText("%f" % self.Ap1)
        self.wpBox1.setText("%f" % self.wp1)
        self.tpBox1.setText("%f" % self.tp1)

    def analyzePeak2(self):
        """Analyze the peak in selected region of signal 2
        
        Returns:
            None: Description
        """
        self.imin2 = int(self.min2*1000+0.5)
        self.imax2 = int(self.max2*1000+0.5)
        self.pw2.removeItem(self.plot7)
        self.pw2.removeItem(self.plot8)
        self.pw2.removeItem(self.plot10)
        if self.filterCoreSize1 <= 1:
            self.section2 = self.rawA2[self.imin2:self.imax2]
        else:
            self.section2 = signal.medfilt(self.rawA2[self.imin2:self.imax2],
                                           self.filterCoreSize2)

        # Finding zero point
        self.section02 = self.section2[0:self.n02]
        self.avg2 = np.mean(self.section02)
        self.plot7 = self.pw2.plot(np.linspace(self.min2, self.min2+self.n02/self.f*1000, self.n01), np.ones(self.n01)*self.avg2 , pen=pg.mkPen('y',width=2))

        # Finding maximum point
        self.ipeak2 = np.argmax(self.section2)
        self.Ap2 = np.amax(self.section2) - self.avg2

        # Finding half maximum points
        for i in range(0, self.ipeak2):
            if self.section2[i] >= self.Ap2*0.5+self.avg2:
                break
        self.iFrontHM2 = i
        self.tp2 = self.iFrontHM2/1000.0+self.min2

        for i in range(self.ipeak2, self.imax2-self.imin2):
            if self.section2[i] <= self.Ap2*0.5+self.avg2:
                break
        self.iBackHM2 = i
        self.wp2 = (self.iBackHM2-self.iFrontHM2)/1000.0

        # Visualization
        self.plot8 = self.pw2.plot(np.linspace(self.tp2, self.tp2+self.wp2, self.iBackHM2-self.iFrontHM2), self.section2[self.iFrontHM2:self.iBackHM2], pen=pg.mkPen('m',width=2))
        self.plot10 = self.pw2.plot([self.tp2, self.ipeak2/1000.0+self.min2, self.tp2+self.wp2],[self.Ap2*0.5+self.avg2, self.Ap2+self.avg2, self.Ap2*0.5+self.avg2], pen=None, symbolBrush=('m'), symbolSize=7)

        # Updating results in the TextBoxs
        self.ApBox2.setText("%f" % self.Ap2)
        self.wpBox2.setText("%f" % self.wp2)
        self.tpBox2.setText("%f" % self.tp2)

    def analyzeSpeed(self):
        """Calcualting speed of the sound using analyzed p1 and p2
        
        Returns:
            None: Description
        """
        self.tf = self.tp2-self.tp1
        self.vs = self.D*10/self.tf
        self.tfBox.setText('%f' % self.tf)
        self.vsBox.setText('%f' % self.vs)

    def showLoadFileDialog(self, fileFromCmdLine=None):
        """Open the file dialog to select an input file,
        does not open the dialog if a filename is provided as argument

        Args:
            fileFromCmdLine (str, optional): File to open
        
        Returns:
            None: Description
        """
        if fileFromCmdLine:
            # import file (error checking is done in loadFile() )
            self.dataFileName = fileFromCmdLine
        else:
            self.dataFileName = QtGui.QFileDialog.getOpenFileName(
                self, 'Open file',
                '/home/gg/GraSound/PFC2015/Data/',
                "Scope Files (*.scope)")

        self.loadedFileNameBox.setText(self.dataFileName)
        self.rawA1 = np.loadtxt(self.dataFileName, usecols=(3,))
        self.rawA2 = np.loadtxt(self.dataFileName, usecols=(4,))
        self.n = self.rawA1.__len__() # total number of data points
        self.t = np.linspace(0, self.n/1000, self.n)

        # Remove old data
        self.clearAllPlots()
        self.avg1 = 0.0  # Zero level
        self.avg2 = 0.0
        self.ipeak1 = -1  # -1 flags that peak has not been detected 
        self.ipeak2 = -1  # -1 flags that peak has not been detected 
        self.iFrontHM1 = 0
        self.iFrontHM2 = 0
        self.iBackHM1 = 0
        self.iBackHM2 = 0
        self.Ap1 = 0.0
        self.wp1 = 0.0
        self.tp1 = 0.0
        self.Ap2 = 0.0
        self.wp2 = 0.0
        self.tp2 = 0.0
        self.tf = 0.0
        self.vs = 0.0

        # Add new loaded data
        self.plot1 = self.pw1.plot(self.t, self.rawA1, pen=pg.mkPen('w'))
        self.plot2 = self.pw1.plot(self.t, self.rawA2, pen=pg.mkPen('r'))
        self.plot3 = self.pw2.plot(self.t, self.rawA1, pen=pg.mkPen('w'))
        self.plot4 = self.pw2.plot(self.t, self.rawA2, pen=pg.mkPen('r'))
        self.lr1.sigRegionChanged.connect(self.updatePlot)
        self.lr2.sigRegionChanged.connect(self.updateAnalyzer)
        self.pw2.sigXRangeChanged.connect(self.updateRegion)

        # update the second plot to immediately show only the ROI
        # fixes the weird behaviour when ROI1 is not equal to Xrange of graph 2
        self.updatePlot()

    def plotAnalyzer(self):
        """Visualize the points found by the auto analyzer
        
        Returns:
            None: Description
        """
        if hasattr(self, 'an'):
            s1 = self.an.analysedSignals[0]
            s2 = self.an.analysedSignals[1]

            # signal 1
            # ROI
            self.anROI1 = self.pw2.plot(np.linspace(s1.ROIleft-100, s1.ROIleft)/1000,
                                       np.ones(50)*s1.avg,
                                       pen=pg.mkPen('w',width=2))
            # points
            self.anPlot1 = self.pw2.plot([s1.peak.idx/1000],
                                         [s1.peak.h], symbolBrush=('w'), symbolSize=5)
            self.anPlot1 = self.pw2.plot([s1.hwLeft.idx/1000],
                                         [s1.hwLeft.h], symbolBrush=('w'), symbolSize=5)
            self.anPlot1 = self.pw2.plot([s1.hwRight.idx/1000],
                                         [s1.hwRight.h], symbolBrush=('w'), symbolSize=5)

            # signal 2
            # ROI
            self.anROI2 = self.pw2.plot(np.linspace(s2.ROIleft-100, s2.ROIleft)/1000,
                                       np.ones(50)*s2.avg,
                                       pen=pg.mkPen('r',width=2))
            # points
            self.anPlot2 = self.pw2.plot([s2.peak.idx/1000],
                                         [s2.peak.h], symbolBrush=('r'), symbolSize=5)
            self.anPlot2 = self.pw2.plot([s2.hwLeft.idx/1000],
                                         [s2.hwLeft.h], symbolBrush=('r'), symbolSize=5)
            self.anPlot2 = self.pw2.plot([s2.hwRight.idx/1000],
                                         [s2.hwRight.h], symbolBrush=('r'), symbolSize=5)

app = QtGui.QApplication(sys.argv)
if __name__ == '__main__':
    # check if arguments exist
    parser = argparse.ArgumentParser(description='Add input and output file.')
    parser.add_argument('-i', '--inFile', type=str)
    parser.add_argument('-o', '--outFile', type=str)
    parser.add_argument('-e', '--imgFile', type=str)
    args = parser.parse_args()

    if args.inFile:
        inFile = args.inFile
    else:
        inFile = None

    if args.outFile:
        outFile = args.outFile
    else:
        outFile = None

    if args.imgFile:
        imgFile = args.imgFile
    else:
        imgFile = None

    # call with in and output file (if files are none, nothing is done)
    w = analyzerMainWindow(inFile, outFile, imgFile)
    sys.exit(app.exec_())
