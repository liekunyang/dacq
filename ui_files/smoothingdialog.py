# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\smoothingDialog.ui'
#
# Created: Wed Aug 12 10:56:58 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os, datetime

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

class Ui_smoothingDialog(QtGui.QDialog):
    def __init__(self, parent = None, smoothing=None):
        QtGui.QDialog.__init__(self, parent)
#        super(Ui_smoothingDialog, self).__init__(parent)
        self.smoothing = int(smoothing)
        self.setupUi(self)

        
    def setupUi(self, smoothingDialog):
        smoothingDialog.setObjectName(_fromUtf8("smoothingDialog"))
        smoothingDialog.resize(199, 99)
        self.lab_smoothing = QtGui.QLabel(smoothingDialog)
        self.lab_smoothing.setGeometry(QtCore.QRect(20, 20, 40, 20))
        self.lab_smoothing.setObjectName(_fromUtf8("lab_smoothing"))
        
        self.smoothing_value = QtGui.QSpinBox(smoothingDialog)
        self.smoothing_value.setGeometry(QtCore.QRect(90, 20, 90, 20))
        self.smoothing_value.setObjectName(_fromUtf8("smoothing_value"))
        self.smoothing_value.setProperty("value", self.smoothing)
        self.smoothing_value.setRange(1,999)



        
        
        

        # OK and Cancel buttons
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.setGeometry(QtCore.QRect(80, 60, 100, 30))
        

        
        self.retranslateUi(smoothingDialog)
        QtCore.QMetaObject.connectSlotsByName(smoothingDialog)


        # self.check_dirs()




    def retranslateUi(self, smoothingDialog):
        smoothingDialog.setWindowTitle(_translate("smoothingDialog", "Enter a value for smoothing (default = 60 = 6 seconds)", None))
        self.lab_smoothing.setText(_translate("smoothingDialog", "Smoothing: ", None))




    @staticmethod
    def getSmoothing(parent = None, smoothing=None):
        dialog = Ui_smoothingDialog(parent, smoothing=smoothing)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            ret = str(dialog.smoothing_value.value())

        else:
            ret = ''

        return(ret)


