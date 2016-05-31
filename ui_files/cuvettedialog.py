# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\cuvetteDialog.ui'
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

class Ui_cuvetteDialog(QtGui.QDialog):
    def __init__(self, parent = None, cuvette=None):
        QtGui.QDialog.__init__(self, parent)
#        super(Ui_cuvetteDialog, self).__init__(parent)
        self.cuvette = cuvette
        self.setupUi(self)

        
    def setupUi(self, cuvetteDialog):
        cuvetteDialog.setObjectName(_fromUtf8("cuvetteDialog"))
        cuvetteDialog.resize(199, 99)
        self.lab_cuvette = QtGui.QLabel(cuvetteDialog)
        self.lab_cuvette.setGeometry(QtCore.QRect(20, 20, 40, 20))
        self.lab_cuvette.setObjectName(_fromUtf8("lab_cuvette"))
        self.box_cuvette = QtGui.QComboBox(cuvetteDialog)
        self.box_cuvette.setGeometry(QtCore.QRect(90, 20, 90, 20))
        self.box_cuvette.setObjectName(_fromUtf8("box_cuvette"))



        # OK and Cancel buttons
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.setGeometry(QtCore.QRect(80, 60, 100, 30))
        

        
        self.retranslateUi(cuvetteDialog)
        QtCore.QMetaObject.connectSlotsByName(cuvetteDialog)


        # self.check_dirs()

        #create cuvette list
        self.box_cuvette.addItem("600")
        self.box_cuvette.addItem("2000")
        self.box_cuvette.addItem("4000")

        if self.cuvette != "":
            self.box_cuvette.setCurrentIndex(self.box_cuvette.findText(str(self.cuvette)))



    def retranslateUi(self, cuvetteDialog):
        cuvetteDialog.setWindowTitle(_translate("cuvetteDialog", "Select cuvette for this session", None))
        self.lab_cuvette.setText(_translate("cuvetteDialog", "Cuvette: ", None))




    @staticmethod
    def getCuvette(parent = None, cuvette=None):
        dialog = Ui_cuvetteDialog(parent, cuvette=cuvette)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            ret = str(dialog.box_cuvette.currentText())

        else:
            ret = ''

        return(ret)


