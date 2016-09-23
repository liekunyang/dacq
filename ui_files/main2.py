# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main2.ui'
#
# Created: Sun Nov 22 22:59:02 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from pyqtgraph import PlotWidget
import os


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
        MainWindow.resize(1846, 1198)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        # Plot widgets
        self.graph_rawdata = PlotWidget(self.centralwidget, name='raw')
        self.graph_rawdata.setGeometry(QtCore.QRect(5, 5, 1400, 441))
        self.graph_rawdata.setObjectName(_fromUtf8("graph_rawdata"))
        
        self.graph_enrichrate = PlotWidget(self.centralwidget, name='rate')
        self.graph_enrichrate.setGeometry(QtCore.QRect(5, 465, 1400, 431))
        self.graph_enrichrate.setObjectName(_fromUtf8("graph_enrichrate"))

        self.graph_enrichrate.setXLink('raw')
        

            
        self.chk = {}
        
            
        # fonts
        consolas9 = QtGui.QFont()
        consolas9.setFamily(_fromUtf8("Consolas"))
        consolas9.setPointSize(9)
        
        consolas60 = QtGui.QFont()
        consolas60.setFamily(_fromUtf8("Consolas"))
        consolas60.setPointSize(48)
        
        
        # layoutwidgets
        # declarations
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget1 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget2 = QtGui.QWidget(self.centralwidget)
        
        
        # dimensions
        # x, y, width, height
        self.layoutWidget.setGeometry (QtCore.QRect(1410, 465, 280, 200)) # rates
        self.layoutWidget1.setGeometry(QtCore.QRect(1410, 10, 280, 190)) # rawdata
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 900, 1400, 50)) # events

        # set_names
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))



        #create spacers and separators for later use
        #spacer
        spacerItem1 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        #separator line
        


        
        
        
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        
        
        
        self.chk['enrichrate47'] = QtGui.QCheckBox(self.layoutWidget)
        self.chk['enrichrate47'].setFont(consolas9)
        self.chk['enrichrate47'].setChecked(False)
        self.chk['enrichrate47'].setObjectName(_fromUtf8("chk['enrichrate47']"))
        self.gridLayout.addWidget(self.chk['enrichrate47'], 0, 0, 1, 1)
        
        self.lab_ER47 = QtGui.QLabel(self.layoutWidget)
        self.lab_ER47.setFont(consolas9)
        self.lab_ER47.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_ER47.setObjectName(_fromUtf8("lab_ER47"))
        self.gridLayout.addWidget(self.lab_ER47, 0, 1, 1, 1)
        
        self.lab_ER47unit = QtGui.QLabel(self.layoutWidget)
        self.lab_ER47unit.setFont(consolas9)
        self.lab_ER47unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_ER47unit.setObjectName(_fromUtf8("lab_ER47unit"))
        self.gridLayout.addWidget(self.lab_ER47unit, 0, 2, 1, 1)
       
       
       
       
        self.chk['enrichrate49'] = QtGui.QCheckBox(self.layoutWidget)
        self.chk['enrichrate49'].setFont(consolas9)
        self.chk['enrichrate49'].setChecked(True)
        self.chk['enrichrate49'].setObjectName(_fromUtf8("chk['enrichrate49']"))
        self.gridLayout.addWidget(self.chk['enrichrate49'], 1, 0, 1, 1)
        
        self.lab_ER49 = QtGui.QLabel(self.layoutWidget)
        self.lab_ER49.setFont(consolas9)
        self.lab_ER49.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_ER49.setObjectName(_fromUtf8("lab_ER49"))
        self.gridLayout.addWidget(self.lab_ER49, 1, 1, 1, 1)
        
        self.lab_ER49unit = QtGui.QLabel(self.layoutWidget)
        self.lab_ER49unit.setFont(consolas9)
        self.lab_ER49unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_ER49unit.setObjectName(_fromUtf8("lab_ER49unit"))
        self.gridLayout.addWidget(self.lab_ER49unit, 1, 2, 1, 1)
        
        
        
        
        self.chk['d32dt'] = QtGui.QCheckBox(self.layoutWidget)
        self.chk['d32dt'].setFont(consolas9)
        self.chk['d32dt'].setChecked(True)
        self.chk['d32dt'].setObjectName(_fromUtf8("chk['d32dt']"))
        self.gridLayout.addWidget(self.chk['d32dt'], 2, 0, 1, 1)
        
        self.lab_d32dt = QtGui.QLabel(self.layoutWidget)
        self.lab_d32dt.setFont(consolas9)
        self.lab_d32dt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_d32dt.setObjectName(_fromUtf8("lab_d32dt"))
        self.gridLayout.addWidget(self.lab_d32dt, 2, 1, 1, 1)
        
        self.lab_d32dtunit = QtGui.QLabel(self.layoutWidget)
        self.lab_d32dtunit.setFont(consolas9)
        self.lab_d32dtunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_d32dtunit.setObjectName(_fromUtf8("lab_d32dtunit"))
        self.gridLayout.addWidget(self.lab_d32dtunit, 2, 2, 1, 1)
        
        
        
        
        self.chk['d40dt'] = QtGui.QCheckBox(self.layoutWidget)
        self.chk['d40dt'].setFont(consolas9)
        self.chk['d40dt'].setChecked(False)
        self.chk['d40dt'].setObjectName(_fromUtf8("chk['d40dt']"))
        self.gridLayout.addWidget(self.chk['d40dt'], 3, 0, 1, 1)
        
        self.lab_d40dt = QtGui.QLabel(self.layoutWidget)
        self.lab_d40dt.setFont(consolas9)
        self.lab_d40dt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_d40dt.setObjectName(_fromUtf8("lab_d40dt"))
        self.gridLayout.addWidget(self.lab_d40dt, 3, 1, 1, 1)
        
        self.lab_d40dtunit = QtGui.QLabel(self.layoutWidget)
        self.lab_d40dtunit.setFont(consolas9)
        self.lab_d40dtunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_d40dtunit.setObjectName(_fromUtf8("lab_d40dtunit"))
        self.gridLayout.addWidget(self.lab_d40dtunit, 3, 2, 1, 1)
        
        
        
        
        self.chk['d44dt'] = QtGui.QCheckBox(self.layoutWidget)
        self.chk['d44dt'].setFont(consolas9)
        self.chk['d44dt'].setChecked(True)
        self.chk['d44dt'].setObjectName(_fromUtf8("chk['d44dt']"))
        self.gridLayout.addWidget(self.chk['d44dt'], 4, 0, 1, 1)
        
        self.lab_d44dt = QtGui.QLabel(self.layoutWidget)
        self.lab_d44dt.setFont(consolas9)
        self.lab_d44dt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_d44dt.setObjectName(_fromUtf8("lab_d44dt"))
        self.gridLayout.addWidget(self.lab_d44dt, 4, 1, 1, 1)
        
        self.lab_d44dtunit = QtGui.QLabel(self.layoutWidget)
        self.lab_d44dtunit.setFont(consolas9)
        self.lab_d44dtunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_d44dtunit.setObjectName(_fromUtf8("lab_d44dtunit"))
        self.gridLayout.addWidget(self.lab_d44dtunit, 4, 2, 1, 1)
        
        
        
        
        self.chk['d45dt'] = QtGui.QCheckBox(self.layoutWidget)
        self.chk['d45dt'].setFont(consolas9)
        self.chk['d45dt'].setChecked(True)
        self.chk['d45dt'].setObjectName(_fromUtf8("chk['d45dt']"))
        self.gridLayout.addWidget(self.chk['d45dt'], 5, 0, 1, 1)
        
        self.lab_d45dt = QtGui.QLabel(self.layoutWidget)
        self.lab_d45dt.setFont(consolas9)
        self.lab_d45dt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_d45dt.setObjectName(_fromUtf8("lab_d45dt"))
        self.gridLayout.addWidget(self.lab_d45dt, 5, 1, 1, 1)
        
        self.lab_d45dtunit = QtGui.QLabel(self.layoutWidget)
        self.lab_d45dtunit.setFont(consolas9)
        self.lab_d45dtunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_d45dtunit.setObjectName(_fromUtf8("lab_d45dtunit"))
        self.gridLayout.addWidget(self.lab_d45dtunit, 5, 2, 1, 1)
        
        
        
        
        self.chk['d46dt'] = QtGui.QCheckBox(self.layoutWidget)
        self.chk['d46dt'].setFont(consolas9)
        self.chk['d46dt'].setChecked(True)
        self.chk['d46dt'].setObjectName(_fromUtf8("chk['d46dt']"))
        self.gridLayout.addWidget(self.chk['d46dt'], 6, 0, 1, 1)
        
        self.lab_d46dt = QtGui.QLabel(self.layoutWidget)
        self.lab_d46dt.setFont(consolas9)
        self.lab_d46dt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_d46dt.setObjectName(_fromUtf8("lab_d46dt"))
        self.gridLayout.addWidget(self.lab_d46dt, 6, 1, 1, 1)
        
        self.lab_d46dtunit = QtGui.QLabel(self.layoutWidget)
        self.lab_d46dtunit.setFont(consolas9)
        self.lab_d46dtunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_d46dtunit.setObjectName(_fromUtf8("lab_d46dtunit"))
        self.gridLayout.addWidget(self.lab_d46dtunit, 6, 2, 1, 1)




        self.chk['d47dt'] = QtGui.QCheckBox(self.layoutWidget)
        self.chk['d47dt'].setFont(consolas9)
        self.chk['d47dt'].setChecked(True)
        self.chk['d47dt'].setObjectName(_fromUtf8("chk['d47dt']"))
        self.gridLayout.addWidget(self.chk['d47dt'], 7, 0, 1, 1)

        self.lab_d47dt = QtGui.QLabel(self.layoutWidget)
        self.lab_d47dt.setFont(consolas9)
        self.lab_d47dt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_d47dt.setObjectName(_fromUtf8("lab_d47dt"))
        self.gridLayout.addWidget(self.lab_d47dt, 7, 1, 1, 1)

        self.lab_d47dtunit = QtGui.QLabel(self.layoutWidget)
        self.lab_d47dtunit.setFont(consolas9)
        self.lab_d47dtunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_d47dtunit.setObjectName(_fromUtf8("lab_d47dtunit"))
        self.gridLayout.addWidget(self.lab_d47dtunit, 7, 2, 1, 1)




        self.chk['d49dt'] = QtGui.QCheckBox(self.layoutWidget)
        self.chk['d49dt'].setFont(consolas9)
        self.chk['d49dt'].setChecked(True)
        self.chk['d49dt'].setObjectName(_fromUtf8("chk['d49dt']"))
        self.gridLayout.addWidget(self.chk['d49dt'], 8, 0, 1, 1)

        self.lab_d49dt = QtGui.QLabel(self.layoutWidget)
        self.lab_d49dt.setFont(consolas9)
        self.lab_d49dt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_d49dt.setObjectName(_fromUtf8("lab_d49dt"))
        self.gridLayout.addWidget(self.lab_d49dt, 8, 1, 1, 1)

        self.lab_d49dtunit = QtGui.QLabel(self.layoutWidget)
        self.lab_d49dtunit.setFont(consolas9)
        self.lab_d49dtunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_d49dtunit.setObjectName(_fromUtf8("lab_d49dtunit"))
        self.gridLayout.addWidget(self.lab_d49dtunit, 8, 2, 1, 1)




        self.chk['dtotalCO2dt'] = QtGui.QCheckBox(self.layoutWidget)
        self.chk['dtotalCO2dt'].setFont(consolas9)
        self.chk['dtotalCO2dt'].setChecked(True)
        self.chk['dtotalCO2dt'].setObjectName(_fromUtf8("chk['dtotalCO2dt']"))
        self.gridLayout.addWidget(self.chk['dtotalCO2dt'], 9, 0, 1, 1)

        self.lab_dtotalCO2dt = QtGui.QLabel(self.layoutWidget)
        self.lab_dtotalCO2dt.setFont(consolas9)
        self.lab_dtotalCO2dt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_dtotalCO2dt.setObjectName(_fromUtf8("lab_dtotalCO2dt"))
        self.gridLayout.addWidget(self.lab_dtotalCO2dt, 9, 1, 1, 1)

        self.lab_dtotalCO2dtunit = QtGui.QLabel(self.layoutWidget)
        self.lab_dtotalCO2dtunit.setFont(consolas9)
        self.lab_dtotalCO2dtunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_dtotalCO2dtunit.setObjectName(_fromUtf8("lab_dtotalCO2dtunit"))
        self.gridLayout.addWidget(self.lab_dtotalCO2dtunit, 9, 2, 1, 1)





        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        
        
        
        
        self.chk['Mass32'] = QtGui.QCheckBox(self.layoutWidget1)
        self.chk['Mass32'].setFont(consolas9)
        self.chk['Mass32'].setChecked(True)
        self.chk['Mass32'].setObjectName(_fromUtf8("chk['Mass32']"))
        self.gridLayout_3.addWidget(self.chk['Mass32'], 0, 0, 1, 1)
        
        self.lab_32 = QtGui.QLabel(self.layoutWidget1)
        self.lab_32.setFont(consolas9)
        self.lab_32.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_32.setObjectName(_fromUtf8("lab_32"))
        self.gridLayout_3.addWidget(self.lab_32, 0, 1, 1, 1)
        
        self.lab_M32unit = QtGui.QLabel(self.layoutWidget1)
        self.lab_M32unit.setFont(consolas9)
        self.lab_M32unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_M32unit.setObjectName(_fromUtf8("lab_M32unit"))
        self.gridLayout_3.addWidget(self.lab_M32unit, 0, 2, 1, 1)
        
        
        
        
        self.chk['Mass40'] = QtGui.QCheckBox(self.layoutWidget1)
        self.chk['Mass40'].setFont(consolas9)
        self.chk['Mass40'].setChecked(True)
        self.chk['Mass40'].setObjectName(_fromUtf8("chk['Mass40']"))
        self.gridLayout_3.addWidget(self.chk['Mass40'], 1, 0, 1, 1)
        
        self.lab_40 = QtGui.QLabel(self.layoutWidget1)
        self.lab_40.setFont(consolas9)
        self.lab_40.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_40.setObjectName(_fromUtf8("lab_40"))
        self.gridLayout_3.addWidget(self.lab_40, 1, 1, 1, 1)
        
        self.lab_M40unit = QtGui.QLabel(self.layoutWidget1)
        self.lab_M40unit.setFont(consolas9)
        self.lab_M40unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_M40unit.setObjectName(_fromUtf8("lab_M40unit"))
        self.gridLayout_3.addWidget(self.lab_M40unit, 1, 2, 1, 1)
        
        
        
        
        self.chk['Mass44'] = QtGui.QCheckBox(self.layoutWidget1)
        self.chk['Mass44'].setFont(consolas9)
        self.chk['Mass44'].setChecked(True)
        self.chk['Mass44'].setObjectName(_fromUtf8("chk['M44']"))
        self.gridLayout_3.addWidget(self.chk['Mass44'], 2, 0, 1, 1)
        
        self.lab_44 = QtGui.QLabel(self.layoutWidget1)
        self.lab_44.setFont(consolas9)
        self.lab_44.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_44.setObjectName(_fromUtf8("lab_44"))
        self.gridLayout_3.addWidget(self.lab_44, 2, 1, 1, 1)
        
        self.lab_M44unit = QtGui.QLabel(self.layoutWidget1)
        self.lab_M44unit.setFont(consolas9)
        self.lab_M44unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_M44unit.setObjectName(_fromUtf8("lab_M44unit"))
        self.gridLayout_3.addWidget(self.lab_M44unit, 2, 2, 1, 1)
        
        
        
        
        self.chk['Mass45'] = QtGui.QCheckBox(self.layoutWidget1)
        self.chk['Mass45'].setFont(consolas9)
        self.chk['Mass45'].setChecked(True)
        self.chk['Mass45'].setObjectName(_fromUtf8("chk['Mass45']"))
        self.gridLayout_3.addWidget(self.chk['Mass45'], 3, 0, 1, 1)
        
        self.lab_45 = QtGui.QLabel(self.layoutWidget1)
        self.lab_45.setFont(consolas9)
        self.lab_45.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_45.setObjectName(_fromUtf8("lab_45"))
        self.gridLayout_3.addWidget(self.lab_45, 3, 1, 1, 1)
        
        self.lab_M45unit = QtGui.QLabel(self.layoutWidget1)
        self.lab_M45unit.setFont(consolas9)
        self.lab_M45unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_M45unit.setObjectName(_fromUtf8("lab_M45unit"))
        self.gridLayout_3.addWidget(self.lab_M45unit, 3, 2, 1, 1)
        
        
        
        
        self.chk['Mass46'] = QtGui.QCheckBox(self.layoutWidget1)
        self.chk['Mass46'].setFont(consolas9)
        self.chk['Mass46'].setChecked(True)
        self.chk['Mass46'].setObjectName(_fromUtf8("chk['Mass46']"))
        self.gridLayout_3.addWidget(self.chk['Mass46'], 4, 0, 1, 1)
        
        self.lab_46 = QtGui.QLabel(self.layoutWidget1)
        self.lab_46.setFont(consolas9)
        self.lab_46.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_46.setObjectName(_fromUtf8("lab_46"))
        self.gridLayout_3.addWidget(self.lab_46, 4, 1, 1, 1)
        
        self.lab_M46unit = QtGui.QLabel(self.layoutWidget1)
        self.lab_M46unit.setFont(consolas9)
        self.lab_M46unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_M46unit.setObjectName(_fromUtf8("lab_M46unit"))
        self.gridLayout_3.addWidget(self.lab_M46unit, 4, 2, 1, 1)
        
        
        
        
        self.chk['Mass47'] = QtGui.QCheckBox(self.layoutWidget1)
        self.chk['Mass47'].setFont(consolas9)
        self.chk['Mass47'].setChecked(True)
        self.chk['Mass47'].setObjectName(_fromUtf8("chk['Mass47']"))
        self.gridLayout_3.addWidget(self.chk['Mass47'], 5, 0, 1, 1)
        
        self.lab_47 = QtGui.QLabel(self.layoutWidget1)
        self.lab_47.setFont(consolas9)
        self.lab_47.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_47.setObjectName(_fromUtf8("lab_47"))
        self.gridLayout_3.addWidget(self.lab_47, 5, 1, 1, 1)
        
        self.lab_M47unit = QtGui.QLabel(self.layoutWidget1)
        self.lab_M47unit.setFont(consolas9)
        self.lab_M47unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_M47unit.setObjectName(_fromUtf8("lab_M47unit"))
        self.gridLayout_3.addWidget(self.lab_M47unit, 5, 2, 1, 1)
        
        
        
        
        self.chk['Mass49'] = QtGui.QCheckBox(self.layoutWidget1)
        self.chk['Mass49'].setFont(consolas9)
        self.chk['Mass49'].setChecked(True)
        self.chk['Mass49'].setObjectName(_fromUtf8("chk['Mass49']"))
        self.gridLayout_3.addWidget(self.chk['Mass49'], 6, 0, 1, 1)
        
        self.lab_49 = QtGui.QLabel(self.layoutWidget1)
        self.lab_49.setFont(consolas9)
        self.lab_49.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_49.setObjectName(_fromUtf8("lab_49"))
        self.gridLayout_3.addWidget(self.lab_49, 6, 1, 1, 1)
        
        self.lab_M49unit = QtGui.QLabel(self.layoutWidget1)
        self.lab_M49unit.setFont(consolas9)
        self.lab_M49unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_M49unit.setObjectName(_fromUtf8("lab_M49unit"))
        self.gridLayout_3.addWidget(self.lab_M49unit, 6, 2, 1, 1)
        
        
        
        
        self.chk['totalCO2'] = QtGui.QCheckBox(self.layoutWidget1)
        self.chk['totalCO2'].setFont(consolas9)
        self.chk['totalCO2'].setChecked(True)
        self.chk['totalCO2'].setObjectName(_fromUtf8("chk['totalCO2']"))
        self.gridLayout_3.addWidget(self.chk['totalCO2'], 7, 0, 1, 1)
        
        self.lab_totalCO2 = QtGui.QLabel(self.layoutWidget1)
        self.lab_totalCO2.setFont(consolas9)
        self.lab_totalCO2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_totalCO2.setObjectName(_fromUtf8("lab_totalCO2"))
        self.gridLayout_3.addWidget(self.lab_totalCO2, 7, 1, 1, 1)
        
        self.lab_totCO2unit = QtGui.QLabel(self.layoutWidget1)
        self.lab_totCO2unit.setFont(consolas9)
        self.lab_totCO2unit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_totCO2unit.setObjectName(_fromUtf8("lab_totCO2unit"))
        self.gridLayout_3.addWidget(self.lab_totCO2unit, 7, 2, 1, 1)
        
        
        
        
        self.chk['logE49'] = QtGui.QCheckBox(self.layoutWidget1)
        self.chk['logE49'].setFont(consolas9)
        self.chk['logE49'].setChecked(True)
        self.chk['logE49'].setObjectName(_fromUtf8("chk['logE49']"))
        self.gridLayout_3.addWidget(self.chk['logE49'], 8, 0, 1, 1)
        
        self.lab_logE = QtGui.QLabel(self.layoutWidget1)
        self.lab_logE.setFont(consolas9)
        self.lab_logE.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_logE.setObjectName(_fromUtf8("lab_logE"))
        self.gridLayout_3.addWidget(self.lab_logE, 8, 1, 1, 1)

        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btn_bic = QtGui.QPushButton(self.layoutWidget2)
        
        


        self.btn_bic.setFont(consolas9)
        self.btn_bic.setObjectName(_fromUtf8("btn_bic"))
        self.gridLayout_2.addWidget(self.btn_bic, 0, 0, 1, 4)
        self.bic_vol = QtGui.QLineEdit(self.layoutWidget2)



        self.bic_vol.setFont(consolas9)
        self.bic_vol.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bic_vol.setObjectName(_fromUtf8("bic_vol"))
        self.gridLayout_2.addWidget(self.bic_vol, 1, 0, 1, 1)
        self.lab_bicvolunit = QtGui.QLabel(self.layoutWidget2)



        self.lab_bicvolunit.setFont(consolas9)
        self.lab_bicvolunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_bicvolunit.setObjectName(_fromUtf8("lab_bicvolunit"))
        self.gridLayout_2.addWidget(self.lab_bicvolunit, 1, 1, 1, 1)
        self.bic_cc = QtGui.QLineEdit(self.layoutWidget2)



        self.bic_cc.setFont(consolas9)
        self.bic_cc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bic_cc.setObjectName(_fromUtf8("bic_cc"))
        self.gridLayout_2.addWidget(self.bic_cc, 1, 2, 1, 1)
        self.lab_bicccunit = QtGui.QLabel(self.layoutWidget2)



        self.lab_bicccunit.setFont(consolas9)
        self.lab_bicccunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_bicccunit.setObjectName(_fromUtf8("lab_bicccunit"))
        self.gridLayout_2.addWidget(self.lab_bicccunit, 1, 3, 1, 1)
        self.btn_cells = QtGui.QPushButton(self.layoutWidget2)


        #vertical line
        self.sepline = QtGui.QFrame(self.layoutWidget2)
        self.sepline.setFrameShape(QtGui.QFrame.VLine)
        self.sepline.setObjectName(_fromUtf8("sepline"))
        self.gridLayout_2.addItem(spacerItem1, 0, 4, 2, 1)
        self.gridLayout_2.addWidget(self.sepline, 0, 5, 2, 1)
        self.gridLayout_2.addItem(spacerItem1, 0, 6, 2, 1)

        self.btn_cells.setFont(consolas9)
        self.btn_cells.setObjectName(_fromUtf8("btn_cells"))
        self.gridLayout_2.addWidget(self.btn_cells, 0, 7, 1, 4)
        self.cells_vol = QtGui.QLineEdit(self.layoutWidget2)



        self.cells_vol.setFont(consolas9)
        self.cells_vol.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cells_vol.setObjectName(_fromUtf8("cells_vol"))
        self.gridLayout_2.addWidget(self.cells_vol, 1, 7, 1, 1)
        self.lab_cellsvolunit = QtGui.QLabel(self.layoutWidget2)



        self.lab_cellsvolunit.setFont(consolas9)
        self.lab_cellsvolunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_cellsvolunit.setObjectName(_fromUtf8("lab_cellsvolunit"))
        self.gridLayout_2.addWidget(self.lab_cellsvolunit, 1, 8, 1, 1)
        self.cells_cc = QtGui.QLineEdit(self.layoutWidget2)



        self.cells_cc.setFont(consolas9)
        self.cells_cc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cells_cc.setObjectName(_fromUtf8("cells_cc"))
        self.gridLayout_2.addWidget(self.cells_cc, 1, 9, 1, 1)
        self.lab_cellsccunit = QtGui.QLabel(self.layoutWidget2)



        self.lab_cellsccunit.setFont(consolas9)
        self.lab_cellsccunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_cellsccunit.setObjectName(_fromUtf8("lab_cellsccunit"))
        self.gridLayout_2.addWidget(self.lab_cellsccunit, 1, 10, 1, 1)
        self.btn_az = QtGui.QPushButton(self.layoutWidget2)

        
        #vertical line
        self.sepline = QtGui.QFrame(self.layoutWidget2)
        self.sepline.setFrameShape(QtGui.QFrame.VLine)
        self.sepline.setObjectName(_fromUtf8("sepline"))
        self.gridLayout_2.addItem(spacerItem1, 0, 11, 2, 1)
        self.gridLayout_2.addWidget(self.sepline, 0, 12, 2, 1)
        self.gridLayout_2.addItem(spacerItem1, 0, 13, 2, 1)
        
        
        self.btn_az.setFont(consolas9)
        self.btn_az.setObjectName(_fromUtf8("btn_az"))
        self.gridLayout_2.addWidget(self.btn_az, 0, 14, 1, 4)
        self.az_vol = QtGui.QLineEdit(self.layoutWidget2)



        self.az_vol.setFont(consolas9)
        self.az_vol.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.az_vol.setObjectName(_fromUtf8("az_vol"))
        self.gridLayout_2.addWidget(self.az_vol, 1, 14, 1, 1)
        self.lab_azvolunit = QtGui.QLabel(self.layoutWidget2)



        self.lab_azvolunit.setFont(consolas9)
        self.lab_azvolunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_azvolunit.setObjectName(_fromUtf8("lab_azvolunit"))
        self.gridLayout_2.addWidget(self.lab_azvolunit, 1, 15, 1, 1)
        self.az_cc = QtGui.QLineEdit(self.layoutWidget2)



        self.az_cc.setFont(consolas9)
        self.az_cc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.az_cc.setObjectName(_fromUtf8("az_cc"))
        self.gridLayout_2.addWidget(self.az_cc, 1, 16, 1, 1)
        self.lab_azccunit = QtGui.QLabel(self.layoutWidget2)



        self.lab_azccunit.setFont(consolas9)
        self.lab_azccunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_azccunit.setObjectName(_fromUtf8("lab_azccunit"))
        self.gridLayout_2.addWidget(self.lab_azccunit, 1, 17, 1, 1)
        self.btn_ez = QtGui.QPushButton(self.layoutWidget2)


        #vertical line
        self.sepline = QtGui.QFrame(self.layoutWidget2)
        self.sepline.setFrameShape(QtGui.QFrame.VLine)
        self.sepline.setObjectName(_fromUtf8("sepline"))
        self.gridLayout_2.addItem(spacerItem1, 0, 18, 2, 1)
        self.gridLayout_2.addWidget(self.sepline, 0, 19, 2, 1)
        self.gridLayout_2.addItem(spacerItem1, 0, 20, 2, 1)
        
        
        self.btn_ez.setFont(consolas9)
        self.btn_ez.setObjectName(_fromUtf8("btn_ez"))
        self.gridLayout_2.addWidget(self.btn_ez, 0, 21, 1, 4)
        self.ez_vol = QtGui.QLineEdit(self.layoutWidget2)



        self.ez_vol.setFont(consolas9)
        self.ez_vol.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ez_vol.setObjectName(_fromUtf8("ez_vol"))
        self.gridLayout_2.addWidget(self.ez_vol, 1, 21, 1, 1)
        self.lab_ezvolunit = QtGui.QLabel(self.layoutWidget2)



        self.lab_ezvolunit.setFont(consolas9)
        self.lab_ezvolunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_ezvolunit.setObjectName(_fromUtf8("lab_ezvolunit"))
        self.gridLayout_2.addWidget(self.lab_ezvolunit, 1, 22, 1, 1)
        self.ez_cc = QtGui.QLineEdit(self.layoutWidget2)



        self.ez_cc.setFont(consolas9)
        self.ez_cc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ez_cc.setObjectName(_fromUtf8("ez_cc"))
        self.gridLayout_2.addWidget(self.ez_cc, 1, 23, 1, 1)
        self.lab_ezccunit = QtGui.QLabel(self.layoutWidget2)



        self.lab_ezccunit.setFont(consolas9)
        self.lab_ezccunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_ezccunit.setObjectName(_fromUtf8("lab_ezccunit"))
        self.gridLayout_2.addWidget(self.lab_ezccunit, 1, 24, 1, 1)
        self.btn_lighton = QtGui.QPushButton(self.layoutWidget2)


        #vertical line
        self.sepline = QtGui.QFrame(self.layoutWidget2)
        self.sepline.setFrameShape(QtGui.QFrame.VLine)
        self.sepline.setObjectName(_fromUtf8("sepline"))
        self.gridLayout_2.addItem(spacerItem1, 0, 25, 2, 1)
        self.gridLayout_2.addWidget(self.sepline, 0, 26, 2, 1)
        self.gridLayout_2.addItem(spacerItem1, 0, 27, 2, 1)
        
        self.btn_lighton.setFont(consolas9)
        self.btn_lighton.setObjectName(_fromUtf8("btn_lighton"))
        self.gridLayout_2.addWidget(self.btn_lighton, 0, 28, 1, 1)
        self.light_int = QtGui.QLineEdit(self.layoutWidget2)



        self.light_int.setFont(consolas9)
        self.light_int.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.light_int.setObjectName(_fromUtf8("light_int"))
        self.gridLayout_2.addWidget(self.light_int, 0, 29, 1, 1)
        self.lab_lightintunit = QtGui.QLabel(self.layoutWidget2)



        self.lab_lightintunit.setFont(consolas9)
        self.lab_lightintunit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_lightintunit.setObjectName(_fromUtf8("lab_lightintunit"))
        self.gridLayout_2.addWidget(self.lab_lightintunit, 0, 30, 1, 1)
        self.btn_lightoff = QtGui.QPushButton(self.layoutWidget2)


        self.btn_lightoff.setFont(consolas9)
        self.btn_lightoff.setObjectName(_fromUtf8("btn_lightoff"))
        self.gridLayout_2.addWidget(self.btn_lightoff, 1, 28, 1, 3)
        self.btn_custom = QtGui.QPushButton(self.layoutWidget2)

        #vertical line
        self.sepline = QtGui.QFrame(self.layoutWidget2)
        self.sepline.setFrameShape(QtGui.QFrame.VLine)
        self.sepline.setObjectName(_fromUtf8("sepline"))
        self.gridLayout_2.addItem(spacerItem1, 0, 31, 2, 1)
        self.gridLayout_2.addWidget(self.sepline, 0, 32, 2, 1)
        self.gridLayout_2.addItem(spacerItem1, 0, 33, 2, 1)
        
        self.btn_custom.setFont(consolas9)
        self.btn_custom.setObjectName(_fromUtf8("btn_custom"))
        self.gridLayout_2.addWidget(self.btn_custom, 0, 34, 1, 1)
        self.custom_text = QtGui.QLineEdit(self.layoutWidget2)



        self.custom_text.setFont(consolas9)
        self.custom_text.setText(_fromUtf8(""))
        self.custom_text.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.custom_text.setObjectName(_fromUtf8("custom_text"))
        self.gridLayout_2.addWidget(self.custom_text, 1, 34, 1, 1)
        
        
        #vertical line
        self.sepline = QtGui.QFrame(self.layoutWidget2)
        self.sepline.setFrameShape(QtGui.QFrame.VLine)
        self.sepline.setObjectName(_fromUtf8("sepline"))
        self.gridLayout_2.addItem(spacerItem1, 0, 35, 2, 1)
        self.gridLayout_2.addWidget(self.sepline, 0, 36, 2, 1)
        self.gridLayout_2.addItem(spacerItem1, 0, 37, 2, 1)
        
        
        
        


        # label timer
        self.lab_timer = QtGui.QLabel(self.centralwidget)
        self.lab_timer.setFont(consolas60)
        self.lab_timer.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_timer.setObjectName(_fromUtf8("lab_timer"))
        self.lab_timer.setGeometry(QtCore.QRect(1450, 720, 200, 100))
        self.lab_timer.setAlignment(QtCore.Qt.AlignRight)

        
                #column stretch
        for i in range(33):
            self.gridLayout_2.setColumnStretch(i, 1)
        #last column
        self.gridLayout_2.setColumnStretch(34,30)
        self.gridLayout_2.setColumnStretch(35,1)
        self.gridLayout_2.setColumnStretch(36,1)
        self.gridLayout_2.setColumnStretch(37,1)

      
        
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1846, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuStart = QtGui.QMenu(self.menubar)
        self.menuStart.setObjectName(_fromUtf8("menuStart"))

        self.menuSamples = QtGui.QMenu(self.menubar)
        self.menuSamples.setObjectName(_fromUtf8("menuSamples"))

        self.menuQuit = QtGui.QMenu(self.menubar)
        self.menuQuit.setObjectName(_fromUtf8("menuQuit"))
        
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        
        
        self.menuCalibrations = QtGui.QMenu(self.menubar)
        self.menuCalibrations.setObjectName(_fromUtf8("menuCalibrations"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionStart = QtGui.QAction(MainWindow)
        self.actionStart.setObjectName(_fromUtf8("actionStart"))
        self.actionTestmode = QtGui.QAction(MainWindow)
        self.actionTestmode.setObjectName(_fromUtf8("actionTestmode"))
        self.actionStop = QtGui.QAction(MainWindow)
        self.actionStop.setObjectName(_fromUtf8("actionStop"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionAdd_new_Membrane = QtGui.QAction(MainWindow)
        self.actionAdd_new_Membrane.setObjectName(_fromUtf8("actionAdd_new_Membrane"))
        self.actionAdd_CO2_Calibration = QtGui.QAction(MainWindow)
        self.actionAdd_CO2_Calibration.setObjectName(_fromUtf8("actionAdd_CO2_Calibration"))
        self.actionAdd_O2_Calibration = QtGui.QAction(MainWindow)
        self.actionAdd_O2_Calibration.setObjectName(_fromUtf8("actionAdd_O2_Calibration"))
        self.actionAdd_Electrical_Zeros = QtGui.QAction(MainWindow)
        self.actionAdd_Electrical_Zeros.setObjectName(_fromUtf8("actionAdd_Electrical_Zeros"))
        self.actionAdd_Consumptions = QtGui.QAction(MainWindow)
        self.actionAdd_Consumptions.setObjectName(_fromUtf8("actionAdd_Consumptions"))

        self.actionSamples = QtGui.QAction(MainWindow)
        self.actionSamples.setObjectName(_fromUtf8("actionSamples"))

        self.menuStart.addAction(self.actionStart)
        self.menuStart.addSeparator()
        self.menuStart.addAction(self.actionStop)
        self.menuStart.addSeparator()
        self.menuStart.addAction(self.actionTestmode)

        self.menuSamples.addAction(self.actionSamples)

        self.menuQuit.addAction(self.actionQuit)
        self.menuCalibrations.addAction(self.actionAdd_new_Membrane)
        self.menuCalibrations.addSeparator()
        self.menuCalibrations.addAction(self.actionAdd_CO2_Calibration)
        self.menuCalibrations.addAction(self.actionAdd_O2_Calibration)
        self.menuCalibrations.addSeparator()
        self.menuCalibrations.addAction(self.actionAdd_Electrical_Zeros)
        self.menuCalibrations.addSeparator()
        self.menuCalibrations.addAction(self.actionAdd_Consumptions)
        self.menubar.addAction(self.menuStart.menuAction())
        self.menubar.addAction(self.menuCalibrations.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuSamples.menuAction())
        self.menubar.addAction(self.menuQuit.menuAction())

    
        # SETTINGS > Data_folder
        self.actionDatafolder = QtGui.QAction(MainWindow)
        self.actionDatafolder.setObjectName(_fromUtf8("actionUser"))
        self.actionDatafolder.setCheckable(False)
        self.actionDatafolder.setEnabled(False) 
        self.actionDatafolder.setText("DataFolder: " + str(self.datafolder))
        self.menuSettings.addAction(self.actionDatafolder)
                
        # SETTINGS > User
        self.actionUser = QtGui.QAction(MainWindow)
        self.actionUser.setObjectName(_fromUtf8("actionUser"))
        self.actionUser.setCheckable(False)
        try:
            self.actionUser.setText(_translate("MainWindow", "User: " + self.user, None))
        except:
            self.actionUser.setText(_translate("MainWindow", "NO USER SELECTED !", None))
        self.menuSettings.addAction(self.actionUser)
        
        # SETTINGS > Cuvette
        self.actionCuvette = QtGui.QAction(MainWindow)
        self.actionCuvette.setObjectName(_fromUtf8("actionCuvette"))
        self.actionCuvette.setCheckable(False)
        try:
            self.actionCuvette.setText(_translate("MainWindow", "Cuvette: " + self.cuvette, None))
        except:
            self.actionCuvette.setText(_translate("MainWindow", "NO CUVETTE SELECTED !", None))
        self.menuSettings.addAction(self.actionCuvette)
        
        
        
        # SETTINGS > smoothing
        self.menuSettings.addSeparator()
        self.actionSmoothing = QtGui.QAction(MainWindow)
        self.actionSmoothing.setObjectName(_fromUtf8("actionCuvette"))
        self.actionSmoothing.setCheckable(False)
        try:
            self.actionSmoothing.setText(_translate("MainWindow", "Smoothing: " + self.smoothing, None))
        except:
            self.actionSmoothing.setText(_translate("MainWindow", "Smoothing: 60" , None))
        self.menuSettings.addAction(self.actionSmoothing)
        
        
        
        
        
       
                
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


       
                
                
                
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "dAcq", None))
        self.chk['enrichrate47'].setText(_translate("MainWindow", "EnrichRate(47)", None))
        self.lab_ER47.setText(_translate("MainWindow", "0", None))
        self.lab_ER47unit.setText(_translate("MainWindow", "min-1", None))
        self.chk['enrichrate49'].setText(_translate("MainWindow", "EnrichRate(49)", None))
        self.lab_ER49.setText(_translate("MainWindow", "0", None))
        self.lab_ER49unit.setText(_translate("MainWindow", "min-1", None))
        self.chk['d32dt'].setText(_translate("MainWindow", "O2 Evolution", None))
        self.lab_d32dt.setText(_translate("MainWindow", "0", None))
        self.lab_d32dtunit.setText(_translate("MainWindow", "µM.min-1", None))
        self.chk['d40dt'].setText(_translate("MainWindow", "dM40dt", None))
        self.lab_d40dt.setText(_translate("MainWindow", "0", None))
        self.lab_d40dtunit.setText(_translate("MainWindow", "µM.min-1", None))
        self.chk['d44dt'].setText(_translate("MainWindow", "dM44dt", None))
        self.lab_d44dt.setText(_translate("MainWindow", "0", None))
        self.lab_d44dtunit.setText(_translate("MainWindow", "µM.min-1", None))
        self.chk['d45dt'].setText(_translate("MainWindow", "dM45dt", None))
        self.lab_d45dt.setText(_translate("MainWindow", "0", None))
        self.lab_d45dtunit.setText(_translate("MainWindow", "µM.min-1", None))
        self.chk['d46dt'].setText(_translate("MainWindow", "dM46dt", None))
        self.lab_d46dt.setText(_translate("MainWindow", "0", None))
        self.lab_d46dtunit.setText(_translate("MainWindow", "µM.min-1", None))
        self.chk['d47dt'].setText(_translate("MainWindow", "dM47dt", None))
        self.lab_d47dt.setText(_translate("MainWindow", "0", None))
        self.lab_d47dtunit.setText(_translate("MainWindow", "µM.min-1", None))
        self.chk['d49dt'].setText(_translate("MainWindow", "dM49dt", None))
        self.chk['dtotalCO2dt'].setText(_translate("MainWindow", "dtotalCO2dt", None))
        self.lab_d49dt.setText(_translate("MainWindow", "0", None))
        self.lab_d49dtunit.setText(_translate("MainWindow", "µM.min-1", None))
        self.lab_dtotalCO2dt.setText(_translate("MainWindow", "0", None))
        self.lab_dtotalCO2dtunit.setText(_translate("MainWindow", "µM.min-1", None))
        self.chk['Mass32'].setText(_translate("MainWindow", "Mass32: ", None))
        self.lab_32.setText(_translate("MainWindow", "0", None))
        self.lab_M32unit.setText(_translate("MainWindow", "V", None))
        self.chk['Mass40'].setText(_translate("MainWindow", "Mass40: ", None))
        self.lab_40.setText(_translate("MainWindow", "0", None))
        self.lab_M40unit.setText(_translate("MainWindow", "V", None))
        self.chk['Mass44'].setText(_translate("MainWindow", "Mass44: ", None))
        self.lab_44.setText(_translate("MainWindow", "0", None))
        self.lab_M44unit.setText(_translate("MainWindow", "V", None))
        self.chk['Mass45'].setText(_translate("MainWindow", "Mass45: ", None))
        self.lab_45.setText(_translate("MainWindow", "0", None))
        self.lab_M45unit.setText(_translate("MainWindow", "V", None))
        self.chk['Mass46'].setText(_translate("MainWindow", "Mass46:", None))
        self.lab_46.setText(_translate("MainWindow", "0", None))
        self.lab_M46unit.setText(_translate("MainWindow", "V", None))
        self.chk['Mass47'].setText(_translate("MainWindow", "Mass47: ", None))
        self.lab_47.setText(_translate("MainWindow", "0", None))
        self.lab_M47unit.setText(_translate("MainWindow", "V", None))
        self.chk['Mass49'].setText(_translate("MainWindow", "Mass49: ", None))
        self.lab_49.setText(_translate("MainWindow", "0", None))
        self.lab_M49unit.setText(_translate("MainWindow", "V", None))
        self.chk['totalCO2'].setText(_translate("MainWindow", "Total CO2", None))
        self.lab_totalCO2.setText(_translate("MainWindow", "0", None))
        self.lab_totCO2unit.setText(_translate("MainWindow", "V", None))
        self.chk['logE49'].setText(_translate("MainWindow", "LogEnrich", None))
        self.lab_logE.setText(_translate("MainWindow", "0", None))
        self.btn_bic.setText(_translate("MainWindow", "BIC [0]", None))
        self.bic_vol.setText(_translate("MainWindow", "1", None))
        self.lab_bicvolunit.setText(_translate("MainWindow", "µL", None))
        self.bic_cc.setText(_translate("MainWindow", "0.5", None))
        self.lab_bicccunit.setText(_translate("MainWindow", "M", None))
        self.btn_cells.setText(_translate("MainWindow", "Cells [3]", None))
        self.cells_vol.setText(_translate("MainWindow", "10", None))
        self.lab_cellsvolunit.setText(_translate("MainWindow", "µL", None))
        self.cells_cc.setText(_translate("MainWindow", "0", None))
        self.lab_cellsccunit.setText(_translate("MainWindow", "X", None))
        self.btn_az.setText(_translate("MainWindow", "AZ [1]", None))
        self.az_vol.setText(_translate("MainWindow", "1", None))
        self.lab_azvolunit.setText(_translate("MainWindow", "µL", None))
        self.az_cc.setText(_translate("MainWindow", "1200", None))
        self.lab_azccunit.setText(_translate("MainWindow", "µM", None))
        self.btn_ez.setText(_translate("MainWindow", "EZ [7]", None))
        self.ez_vol.setText(_translate("MainWindow", "1", None))
        self.lab_ezvolunit.setText(_translate("MainWindow", "µL", None))
        self.ez_cc.setText(_translate("MainWindow", "1200", None))
        self.lab_ezccunit.setText(_translate("MainWindow", "µM", None))
        self.btn_lighton.setText(_translate("MainWindow", "Light ON [4]", None))
        self.light_int.setText(_translate("MainWindow", "400", None))
        self.lab_lightintunit.setText(_translate("MainWindow", "µE", None))
        self.btn_lightoff.setText(_translate("MainWindow", "Light OFF [6]", None))
        self.btn_custom.setText(_translate("MainWindow", "Custom [9]", None))
        self.menuStart.setTitle(_translate("MainWindow", "Acquire", None))
        self.menuQuit.setTitle(_translate("MainWindow", "Quit", None))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings", None))
        self.menuCalibrations.setTitle(_translate("MainWindow", "Calibrations", None))
        self.menuSamples.setTitle(_translate("MainWindow", "Samples", None))
        self.actionStart.setText(_translate("MainWindow", "Start", None))
        self.actionSamples.setText(_translate("MainWindow", "Samples manager", None))
        self.actionStart.setShortcut(_translate("MainWindow", "Ctrl+F1", None))
        self.actionTestmode.setText(_translate("MainWindow", "Start Testmode", None))
        self.actionTestmode.setShortcut(_translate("MainWindow", "Ctrl+F3", None))
        
        self.actionStop.setText(_translate("MainWindow", "Stop", None))
        self.actionStop.setShortcut(_translate("MainWindow", "Ctrl+F2", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionAdd_new_Membrane.setText(_translate("MainWindow", "Add new Membrane", None))
        self.actionAdd_CO2_Calibration.setText(_translate("MainWindow", "Add CO2 Calibration", None))
        self.actionAdd_O2_Calibration.setText(_translate("MainWindow", "Add O2 Calibration", None))
        self.actionAdd_Electrical_Zeros.setText(_translate("MainWindow", "Add Electrical Zeros", None))
        self.actionAdd_Consumptions.setText(_translate("MainWindow", "Add Consumptions", None))
        
        #colors
        self.chk['Mass32'].setStyleSheet("color:rgb(250,0,0)")
        self.chk['Mass40'].setStyleSheet("color:rgb(200,150,0)")
        self.chk['Mass44'].setStyleSheet("color:rgb(0,250,0)")
        self.chk['Mass45'].setStyleSheet("color:rgb(50,200,250)")
        self.chk['Mass46'].setStyleSheet("color:rgb(250,150,250)")
        self.chk['Mass47'].setStyleSheet("color:rgb(0,100,250)")
        self.chk['Mass49'].setStyleSheet("color:rgb(100,0,250)")
        self.chk['totalCO2'].setStyleSheet("color:rgb(0,0,0)")
        self.chk['logE49'].setStyleSheet("color:rgb(150,150,150)")
        
        self.chk['enrichrate47'].setStyleSheet("color:rgb(0,100,250)")
        self.chk['enrichrate49'].setStyleSheet("color:rgb(100,0,250)")
        self.chk['d32dt'].setStyleSheet("color:rgb(250,0,0)")
        self.chk['d40dt'].setStyleSheet("color:rgb(200,150,0)")
        self.chk['d44dt'].setStyleSheet("color:rgb(0,250,0)")
        self.chk['d45dt'].setStyleSheet("color:rgb(50,200,250)")
        self.chk['d46dt'].setStyleSheet("color:rgb(250,150,250)")
        self.chk['d47dt'].setStyleSheet("color:rgb(0,100,250)")
        self.chk['d49dt'].setStyleSheet("color:rgb(100,0,250)")
        self.chk['dtotalCO2dt'].setStyleSheet("color:rgb(0,0,0)")
        

      