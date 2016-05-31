# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\userDialog.ui'
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

class Ui_userDialog(QtGui.QDialog):
    def __init__(self, parent = None, user=None):
        QtGui.QDialog.__init__(self, parent)
#        super(Ui_userDialog, self).__init__(parent)
        self.user = user
        self.setupUi(self)

        
    def setupUi(self, userDialog):
        userDialog.setObjectName(_fromUtf8("userDialog"))
        userDialog.resize(399, 150)
        self.lab_user = QtGui.QLabel(userDialog)
        self.lab_user.setGeometry(QtCore.QRect(12, 50, 38, 16))
        self.lab_user.setObjectName(_fromUtf8("lab_user"))
        self.box_user = QtGui.QComboBox(userDialog)
        self.box_user.setGeometry(QtCore.QRect(113, 50, 100, 22))
        self.box_user.setObjectName(_fromUtf8("box_user"))



        # OK and Cancel buttons
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.setGeometry(QtCore.QRect(200, 100, 158, 30))
        
        

        
        
        self.retranslateUi(userDialog)
        QtCore.QMetaObject.connectSlotsByName(userDialog)


        # self.check_dirs()

        #create user list
        self.user_list()
 

    def retranslateUi(self, userDialog):
        userDialog.setWindowTitle(_translate("userDialog", "Start new acquisition", None))
        self.lab_user.setText(_translate("userDialog", "User: ", None))



    # get list of users
    def user_list(self):
        self.datafolder = "C:\\Mass_Spec_Data\\"

        for folder in [ name for name in os.listdir(self.datafolder) if os.path.isdir(os.path.join(self.datafolder, name))]:
            if folder != os.path.normpath(self.datafolder) and folder != "_calibrations" and folder != "" and folder != None:
                self.box_user.addItem(str(folder.split("\\")[-1]))


        if self.user != "":
            self.box_user.setCurrentIndex(self.box_user.findText(str(self.user)))





    @staticmethod
    def getStartData(parent = None, user=None):
        dialog = Ui_userDialog(parent, user=user)
        if dialog.exec_() == QtGui.QDialog.Accepted:
#            today = datetime.date.today().strftime('%Y%m%d')

#             #check for data folder
#            if not os.path.exists(os.path.normpath(dialog.txt_datafolder.text())):
#                os.makedirs(os.path.normpath(dialog.txt_datafolder.text()))
#                print("Created folder: ", (os.path.normpath(dialog.txt_datafolder.text())))
#
#            #check for user folder
#            if not os.path.exists(os.path.normpath(os.path.join(dialog.txt_datafolder.text(), dialog.box_user.currentText()))):
#                os.makedirs(os.path.normpath(os.path.join(dialog.txt_datafolder.text(), dialog.box_user.currentText())))
#                print("Created folder: ", (os.path.normpath(os.path.join(dialog.txt_datafolder.text(), dialog.box_user.currentText()))))
#
#            #check for user folder
#            if not os.path.exists(os.path.normpath(os.path.join(dialog.txt_datafolder.text(), dialog.box_user.currentText(), today))):
#                os.makedirs(os.path.normpath(os.path.join(dialog.txt_datafolder.text(), dialog.box_user.currentText(), today)))
#                print("Created folder: ", (os.path.normpath(os.path.join(dialog.txt_datafolder.text(), dialog.box_user.currentText(), today))))
#
#
#            #check for rawdata folder
#            if not os.path.exists(os.path.normpath(os.path.join(dialog.txt_datafolder.text(), dialog.box_user.currentText(), today, "rawdata"))):
#                os.makedirs(os.path.normpath(os.path.join(dialog.txt_datafolder.text(), dialog.box_user.currentText(), today, "rawdata")))
#                print("Created folder: ", (os.path.normpath(os.path.join(dialog.txt_datafolder.text(), dialog.box_user.currentText(), today, "rawdata"))))

            ret = str(dialog.box_user.currentText())

        else:
            ret = ''

        return(ret)


