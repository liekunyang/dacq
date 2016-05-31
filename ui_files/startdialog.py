# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\startdialog.ui'
#
# Created: Wed Aug 12 10:56:58 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os, datetime, glob
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

class Ui_StartDialog(QtGui.QDialog):
    def __init__(self, parent = None, user=None, datafolder="C:\\Mass_Spec_Data\\"):
        QtGui.QDialog.__init__(self, parent)
#        super(Ui_StartDialog, self).__init__(parent)
        self.user = user
        self.datafolder = datafolder
        self.setupUi(self)
        

        
    def setupUi(self, StartDialog):
        StartDialog.setObjectName(_fromUtf8("StartDialog"))
        StartDialog.resize(399, 420)
        
        
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(True)
        
        
        self.lab_samplename = QtGui.QLabel(StartDialog)
        self.lab_samplename.setGeometry(QtCore.QRect(20, 300, 120, 22))
        self.lab_samplename.setFont(font)
        self.lab_samplename.setObjectName(_fromUtf8("lab_samplename"))

        self.txt_samplename = QtGui.QLineEdit(StartDialog)
        self.txt_samplename.setGeometry(QtCore.QRect(20, 323, 220, 22))
        self.txt_samplename.setObjectName(_fromUtf8("txt_samplename"))

        self.samples_today = QtGui.QLabel(StartDialog)
        self.samples_today.setGeometry(QtCore.QRect(20, 5, 120, 22))
        self.samples_today.setFont(font)
        self.samples_today.setObjectName(_fromUtf8("samples_today"))


        self.samplelist = QtGui.QListWidget(StartDialog)
        self.samplelist.setGeometry(QtCore.QRect(20, 27, 320, 250)) 
        self.populate_filelist()


        # OK and Cancel buttons
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.setGeometry(QtCore.QRect(200, 370, 158, 30))
        self.samplelist.itemSelectionChanged.connect(self.lastsample)
        
        
        self.retranslateUi(StartDialog)
        QtCore.QMetaObject.connectSlotsByName(StartDialog)



    def retranslateUi(self, StartDialog):
        StartDialog.setWindowTitle(_translate("StartDialog", "Start new acquisition", None))
        self.lab_samplename.setText(_translate("StartDialog", "Next Sample's Name: ", None))
        self.samples_today.setText(_translate("StartDialog", "Today's samples: ", None))


    def lastsample(self):
        self.txt_samplename.setText(self.samplelist.selectedItems()[0].text())
        
        
        
    def populate_filelist(self):
        
        self.samplelist.clear()
        self.today = datetime.date.today().strftime('%Y%m%d')
        samplelist_file = os.path.join(self.datafolder, self.user, self.today) + "\\" + self.today + "_SAMPLES.csv"
        
        #open SAMPLE file 
        if os.path.isdir(os.path.join(self.datafolder, self.user, self.today)) and os.path.isfile(samplelist_file):   
            samples = pd.read_csv(samplelist_file, encoding='ISO-8859-1')
            samples.sort(columns =  ['date', 'time'], ascending=[False, False], inplace=True)
            self.filelist = list(map(lambda x : x.split("\\")[-1].lstrip(self.today + "_").rstrip(".csv"), samples.filename))
            if len(self.filelist) > 0:
                self.samplelist.addItems(self.filelist)
                self.txt_samplename.setText(self.filelist[0])
            
        
#        
#        if os.path.isdir(os.path.join(self.datafolder, self.user, self.today)):    
#            pathlist = glob.glob(os.path.join(self.datafolder, self.user, self.today) + "\\*.csv")
#            self.pathlist = [x for x in pathlist if x.find("SAMPLES") == -1]
#            
#            self.filelist=list(map(lambda x : x.split("\\")[-1].lstrip(self.today + "_").rstrip(".csv"), self.pathlist))
#            self.samplelist.addItems(self.filelist)
#        
#        #select first file of list
#        self.samplelist.setCurrentRow(0)
#        

    @staticmethod
    def getStartData(parent=None, user=None, datafolder="C:\\Mass_Spec_Data\\"):
        
        dialog = Ui_StartDialog(parent, user=user, datafolder = datafolder)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            today = datetime.date.today().strftime('%Y%m%d')

             #check for data folder
            if not os.path.exists(os.path.normpath(datafolder)):
                os.makedirs(os.path.normpath(datafolder))
                print("Created folder: ", (os.path.normpath(datafolder)))

            #check for user folder
            if not os.path.exists(os.path.normpath(os.path.join(datafolder, user))):
                os.makedirs(os.path.normpath(os.path.join(datafolder, user)))
                print("Created folder: ", (os.path.normpath(os.path.join(datafolder, user))))

            #check for user folder
            if not os.path.exists(os.path.normpath(os.path.join(datafolder, user, today))):
                os.makedirs(os.path.normpath(os.path.join(datafolder, user, today)))
                print("Created folder: ", (os.path.normpath(os.path.join(datafolder, user, today))))


            #check for rawdata folder
            if not os.path.exists(os.path.normpath(os.path.join(datafolder, user, today, "rawdata"))):
                os.makedirs(os.path.normpath(os.path.join(datafolder, user, today, "rawdata")))
                print("Created folder: ", (os.path.normpath(os.path.join(datafolder, user, today, "rawdata"))))

            ret = str(dialog.txt_samplename.text())

        else:
            ret = ''

        return(ret)


