# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\datafolderDialog.ui'
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

class Ui_datafolderDialog(QtGui.QDialog):
    def __init__(self, parent = None, datafolder=None):
        QtGui.QDialog.__init__(self, parent)
#        super(Ui_datafolderDialog, self).__init__(parent)
        self.datafolder = datafolder
        self.setupUi(self)

        
    def setupUi(self, datafolderDialog):
        datafolderDialog.setObjectName(_fromUtf8("datafolderDialog"))
        datafolderDialog.resize(299, 120)
        self.change_folder = QtGui.QPushButton(datafolderDialog)
        self.change_folder.setEnabled(False)
        self.change_folder.setGeometry(QtCore.QRect(290, 26, 93, 28))
        self.change_folder.setObjectName(_fromUtf8("change_folder"))
        self.txt_datafolder = QtGui.QLineEdit(datafolderDialog)
        self.txt_datafolder.setEnabled(False)
        self.txt_datafolder.setGeometry(QtCore.QRect(10, 30, 271, 22))
        self.txt_datafolder.setObjectName(_fromUtf8("txt_datafolder"))
        self.lab_datafolder = QtGui.QLabel(datafolderDialog)
        self.lab_datafolder.setGeometry(QtCore.QRect(10, 10, 111, 16))

        # OK and Cancel buttons
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.setGeometry(QtCore.QRect(100, 80, 108, 30))
        

        
        self.retranslateUi(datafolderDialog)
        QtCore.QMetaObject.connectSlotsByName(datafolderDialog)


        # self.check_dirs()

        #create datafolder list
        self.box_datafolder.addItem("600")
        self.box_datafolder.addItem("2000")
        self.box_datafolder.addItem("4000")

        if self.datafolder != "":
            self.box_datafolder.setCurrentIndex(self.box_datafolder.findText(str(self.datafolder)))



    def retranslateUi(self, datafolderDialog):
        datafolderDialog.setWindowTitle(_translate("datafolderDialog", "Select datafolder for this session", None))
        self.lab_datafolder.setText(_translate("datafolderDialog", "datafolder: ", None))




    @staticmethod
    def getdatafolder(parent = None, datafolder=None):
        dialog = Ui_datafolderDialog(parent, datafolder=datafolder)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            ret = str(dialog.box_datafolder.currentText())

        else:
            ret = ''

        return(ret)


