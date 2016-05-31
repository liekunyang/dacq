# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\membrane_dialog.ui'
#
# Created: Fri Aug 14 14:01:35 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os, datetime
import pandas as pd
import numpy as np


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

class Ui_Membrane_Dialog(QtGui.QDialog):
    def __init__(self, parent = None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
    def setupUi(self, Membrane_Dialog):
        Membrane_Dialog.setObjectName(_fromUtf8("Membrane_Dialog"))
        Membrane_Dialog.resize(350, 200)
        self.buttonBox = QtGui.QDialogButtonBox(Membrane_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 150, 251, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.box_cuvette = QtGui.QComboBox(Membrane_Dialog)
        self.box_cuvette.setGeometry(QtCore.QRect(137, 73, 73, 22))
        self.box_cuvette.setObjectName(_fromUtf8("box_cuvette"))
        self.box_cuvette.addItem(_fromUtf8(""))
        self.box_cuvette.addItem(_fromUtf8(""))
        self.box_cuvette.addItem(_fromUtf8(""))
        self.txt_date = QtGui.QLineEdit(Membrane_Dialog)
        self.txt_date.setGeometry(QtCore.QRect(137, 21, 137, 22))
        self.txt_date.setObjectName(_fromUtf8("txt_date"))
        self.label_2 = QtGui.QLabel(Membrane_Dialog)
        self.label_2.setGeometry(QtCore.QRect(41, 21, 78, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Membrane_Dialog)
        self.label_3.setGeometry(QtCore.QRect(41, 73, 43, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Membrane_Dialog)
        self.label_4.setGeometry(QtCore.QRect(41, 102, 89, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.box_membrane = QtGui.QComboBox(Membrane_Dialog)
        self.box_membrane.setGeometry(QtCore.QRect(137, 102, 73, 22))
        self.box_membrane.setObjectName(_fromUtf8("box_membrane"))
        self.box_membrane.addItem(_fromUtf8(""))
        self.box_membrane.addItem(_fromUtf8(""))
        self.box_membrane.addItem(_fromUtf8(""))
        self.label_6 = QtGui.QLabel(Membrane_Dialog)
        self.label_6.setGeometry(QtCore.QRect(41, 50, 75, 16))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))

        self.retranslateUi(Membrane_Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Membrane_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Membrane_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Membrane_Dialog)
        
        self.populate_fields()

    def retranslateUi(self, Membrane_Dialog):
        Membrane_Dialog.setWindowTitle(_translate("Membrane_Dialog", "Membrane information", None))
        self.box_cuvette.setItemText(0, _translate("Membrane_Dialog", "600", None))
        self.box_cuvette.setItemText(1, _translate("Membrane_Dialog", "2000", None))
        self.box_cuvette.setItemText(2, _translate("Membrane_Dialog", "4000", None))
        self.txt_date.setText(_translate("Membrane_Dialog", "10", None))
        self.label_2.setText(_translate("Membrane_Dialog", "Date changed", None))
        self.label_3.setText(_translate("Membrane_Dialog", "Cuvette", None))
        self.label_4.setText(_translate("Membrane_Dialog", "Membrane type", None))
        self.box_membrane.setItemText(0, _translate("Membrane_Dialog", "Plastic Bag", None))
        self.box_membrane.setItemText(1, _translate("Membrane_Dialog", "Teflon", None))
        self.box_membrane.setItemText(2, _translate("Membrane_Dialog", "Thick Teflon", None))
        self.label_6.setText(_translate("Membrane_Dialog", "(YYYYMMDD)", None))
    
    
    
    def populate_fields(self):
        #date
        self.txt_date.setText(datetime.date.today().strftime('%Y%m%d'))
        

    @staticmethod
    def add_membrane(parent = None):
        dialog = Ui_Membrane_Dialog(parent)
        result = dialog.exec_()
        
        date = str(dialog.txt_date.text())
        cuvette = str(dialog.box_cuvette.currentText())
        membrane_type = str(dialog.box_membrane.currentText())
        membranefile = "C:\\Mass_Spec_Data\\_calibrations\\membranes.csv"
        if os.path.isfile(membranefile):
            membranedf = pd.read_csv(membranefile)

            if len(membranedf.query("date == " + date + " & cuvette == '" + cuvette + "' & type == '" + membrane_type +"'" )) == 0: #check if membrane change already recorded
                newmembraneid = str(max(membranedf['id']) +1)
                with open(membranefile, "a") as f:
                    f.write(",".join([newmembraneid, date, cuvette, membrane_type]) + "\n")

                    print("Added: \n" ,",".join([newmembraneid, date, cuvette, membrane_type])+"\n")
            else:
                print("Membrane already recorded")

        else:
            with open(membranefile, "w") as f:
                    newmembraneid = "1"
                    f.write("id,date,cuvette,type\n")
                    f.write(",".join([newmembraneid, date, cuvette, membrane_type]) + "\n")

                    print("Added: \n" ,",".join([newmembraneid, date, cuvette, membrane_type])+"\n")

