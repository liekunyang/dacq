# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\calib_dialog.ui'
#
# Created: Fri Aug 14 14:01:15 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import pandas as pd

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

class Ui_Calib_Dialog(QtGui.QDialog):
    def __init__(self, parent = None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
    def setupUi(self, Calib_Dialog):
        Calib_Dialog.setObjectName(_fromUtf8("Calib_Dialog"))
        Calib_Dialog.resize(350, 200)
        self.buttonBox = QtGui.QDialogButtonBox(Calib_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 150, 251, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.widget = QtGui.QWidget(Calib_Dialog)
        self.widget.setGeometry(QtCore.QRect(21, 20, 301, 111))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txt_volinject = QtGui.QLineEdit(self.widget)
        self.txt_volinject.setObjectName(_fromUtf8("txt_volinject"))
        self.gridLayout.addWidget(self.txt_volinject, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.txt_bicarb_cc = QtGui.QLineEdit(self.widget)
        self.txt_bicarb_cc.setObjectName(_fromUtf8("txt_bicarb_cc"))
        self.gridLayout.addWidget(self.txt_bicarb_cc, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)


        self.retranslateUi(Calib_Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Calib_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Calib_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Calib_Dialog)
        


    def retranslateUi(self, Calib_Dialog):
        Calib_Dialog.setWindowTitle(_translate("Calib_Dialog", "Calibration information", None))
        self.label.setText(_translate("Calib_Dialog", "Injection volume", None))
        self.txt_volinject.setText(_translate("Calib_Dialog", "3", None))
        self.label_5.setText(_translate("Calib_Dialog", "µL", None))
        self.label_2.setText(_translate("Calib_Dialog", "Bicarb concentration", None))
        self.txt_bicarb_cc.setText(_translate("Calib_Dialog", "10", None))
        self.label_6.setText(_translate("Calib_Dialog", "mM", None))




             
         

    @staticmethod
    def calib_infos(parent = None):
        dialog = Ui_Calib_Dialog(parent)
        result = dialog.exec_()

        #returns bicarb CC, vol injection, cuvette, membrane id
        return str(dialog.txt_bicarb_cc.text()), str(dialog.txt_volinject.text())