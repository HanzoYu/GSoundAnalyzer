# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'thesis/gsound/autoAnalyze/ui/bulk.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(622, 606)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mainVL = QtGui.QVBoxLayout()
        self.mainVL.setObjectName(_fromUtf8("mainVL"))
        self.dirLabel = QtGui.QLabel(self.centralwidget)
        self.dirLabel.setObjectName(_fromUtf8("dirLabel"))
        self.mainVL.addWidget(self.dirLabel)
        self.dirHL = QtGui.QHBoxLayout()
        self.dirHL.setObjectName(_fromUtf8("dirHL"))
        self.dirSelectBtn = QtGui.QPushButton(self.centralwidget)
        self.dirSelectBtn.setObjectName(_fromUtf8("dirSelectBtn"))
        self.dirHL.addWidget(self.dirSelectBtn)
        self.dirLE = QtGui.QLineEdit(self.centralwidget)
        self.dirLE.setObjectName(_fromUtf8("dirLE"))
        self.dirHL.addWidget(self.dirLE)
        self.mainVL.addLayout(self.dirHL)
        self.fileLabel = QtGui.QLabel(self.centralwidget)
        self.fileLabel.setObjectName(_fromUtf8("fileLabel"))
        self.mainVL.addWidget(self.fileLabel)
        self.fileHL = QtGui.QHBoxLayout()
        self.fileHL.setObjectName(_fromUtf8("fileHL"))
        self.fileSelectBtn = QtGui.QPushButton(self.centralwidget)
        self.fileSelectBtn.setObjectName(_fromUtf8("fileSelectBtn"))
        self.fileHL.addWidget(self.fileSelectBtn)
        self.fileLE = QtGui.QLineEdit(self.centralwidget)
        self.fileLE.setObjectName(_fromUtf8("fileLE"))
        self.fileHL.addWidget(self.fileLE)
        self.mainVL.addLayout(self.fileHL)
        self.kseparator = KSeparator(self.centralwidget)
        self.kseparator.setObjectName(_fromUtf8("kseparator"))
        self.mainVL.addWidget(self.kseparator)
        self.runHL = QtGui.QHBoxLayout()
        self.runHL.setObjectName(_fromUtf8("runHL"))
        self.runBtn = QtGui.QPushButton(self.centralwidget)
        self.runBtn.setObjectName(_fromUtf8("runBtn"))
        self.runHL.addWidget(self.runBtn)
        self.run1b1Btn = QtGui.QPushButton(self.centralwidget)
        self.run1b1Btn.setObjectName(_fromUtf8("run1b1Btn"))
        self.runHL.addWidget(self.run1b1Btn)
        self.mainVL.addLayout(self.runHL)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(False)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.mainVL.addWidget(self.progressBar)
        self.kseparator_2 = KSeparator(self.centralwidget)
        self.kseparator_2.setObjectName(_fromUtf8("kseparator_2"))
        self.mainVL.addWidget(self.kseparator_2)
        self.availableSelectedHL = QtGui.QHBoxLayout()
        self.availableSelectedHL.setObjectName(_fromUtf8("availableSelectedHL"))
        self.availableLabel = QtGui.QLabel(self.centralwidget)
        self.availableLabel.setObjectName(_fromUtf8("availableLabel"))
        self.availableSelectedHL.addWidget(self.availableLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.availableSelectedHL.addItem(spacerItem)
        self.selectedLabel = QtGui.QLabel(self.centralwidget)
        self.selectedLabel.setObjectName(_fromUtf8("selectedLabel"))
        self.availableSelectedHL.addWidget(self.selectedLabel)
        self.mainVL.addLayout(self.availableSelectedHL)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.filterLabel = QtGui.QLabel(self.centralwidget)
        self.filterLabel.setObjectName(_fromUtf8("filterLabel"))
        self.horizontalLayout.addWidget(self.filterLabel)
        self.filterCB = QtGui.QCheckBox(self.centralwidget)
        self.filterCB.setText(_fromUtf8(""))
        self.filterCB.setObjectName(_fromUtf8("filterCB"))
        self.horizontalLayout.addWidget(self.filterCB)
        self.filterLE = QtGui.QLineEdit(self.centralwidget)
        self.filterLE.setObjectName(_fromUtf8("filterLE"))
        self.horizontalLayout.addWidget(self.filterLE)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.mainVL.addLayout(self.horizontalLayout)
        self.listHL = QtGui.QHBoxLayout()
        self.listHL.setObjectName(_fromUtf8("listHL"))
        self.availableList = QtGui.QListWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.availableList.sizePolicy().hasHeightForWidth())
        self.availableList.setSizePolicy(sizePolicy)
        self.availableList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.availableList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.availableList.setObjectName(_fromUtf8("availableList"))
        self.listHL.addWidget(self.availableList)
        self.moveVL = QtGui.QVBoxLayout()
        self.moveVL.setObjectName(_fromUtf8("moveVL"))
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.moveVL.addItem(spacerItem2)
        self.rightBtn = QtGui.QPushButton(self.centralwidget)
        self.rightBtn.setObjectName(_fromUtf8("rightBtn"))
        self.moveVL.addWidget(self.rightBtn)
        self.leftBtn = QtGui.QPushButton(self.centralwidget)
        self.leftBtn.setObjectName(_fromUtf8("leftBtn"))
        self.moveVL.addWidget(self.leftBtn)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.moveVL.addItem(spacerItem3)
        self.listHL.addLayout(self.moveVL)
        self.selectedList = QtGui.QListWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectedList.sizePolicy().hasHeightForWidth())
        self.selectedList.setSizePolicy(sizePolicy)
        self.selectedList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.selectedList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.selectedList.setObjectName(_fromUtf8("selectedList"))
        self.listHL.addWidget(self.selectedList)
        self.mainVL.addLayout(self.listHL)
        self.moveAllHL = QtGui.QHBoxLayout()
        self.moveAllHL.setObjectName(_fromUtf8("moveAllHL"))
        self.allRightBtn = QtGui.QPushButton(self.centralwidget)
        self.allRightBtn.setObjectName(_fromUtf8("allRightBtn"))
        self.moveAllHL.addWidget(self.allRightBtn)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.moveAllHL.addItem(spacerItem4)
        self.allLeftBtn = QtGui.QPushButton(self.centralwidget)
        self.allLeftBtn.setObjectName(_fromUtf8("allLeftBtn"))
        self.moveAllHL.addWidget(self.allLeftBtn)
        self.mainVL.addLayout(self.moveAllHL)
        self.gridLayout.addLayout(self.mainVL, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "GSound Bulk Analyzer", None))
        self.dirLabel.setText(_translate("MainWindow", "Input directory", None))
        self.dirSelectBtn.setText(_translate("MainWindow", "Select Directory", None))
        self.fileLabel.setText(_translate("MainWindow", "Output file", None))
        self.fileSelectBtn.setText(_translate("MainWindow", "Select File", None))
        self.runBtn.setText(_translate("MainWindow", "Batch analysis", None))
        self.run1b1Btn.setText(_translate("MainWindow", "1 by 1 Analysis", None))
        self.availableLabel.setText(_translate("MainWindow", "Available files: 0", None))
        self.selectedLabel.setText(_translate("MainWindow", "Selected files: 0", None))
        self.filterLabel.setText(_translate("MainWindow", "Filter:", None))
        self.availableList.setSortingEnabled(True)
        self.rightBtn.setText(_translate("MainWindow", "Move right", None))
        self.leftBtn.setText(_translate("MainWindow", "Move left", None))
        self.selectedList.setSortingEnabled(True)
        self.allRightBtn.setText(_translate("MainWindow", "Move all right", None))
        self.allLeftBtn.setText(_translate("MainWindow", "Move all left", None))

from PyKDE4.kdeui import KSeparator
#import PyKDE4
