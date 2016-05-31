# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'events.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from collections import *
from functools import *
import os, glob
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


class Ui_SamplesDialog(QtGui.QDialog):
    def __init__(self, parent=None, datafolder=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)

        self.datafolder = datafolder

        # labels font
        self.font_labels = QtGui.QFont("Arial", 12, QtGui.QFont.Bold)
        self.font_edits = QtGui.QFont("Arial", 12)
        self.font_buttons = QtGui.QFont("Arial", 10, QtGui.QFont.Bold)

        self.setupUi(self)
        self.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1000, 400)

        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        # list of Events
        self.prepare_form(Dialog)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def load_data(self):
        self.samplefile = glob.glob(os.path.join(self.datafolder, "*_SAMPLES.csv"))[0]
        if os.path.isfile(self.samplefile):
            self.samplesdf = pd.read_csv(self.samplefile, encoding='ISO-8859-1')
        else:
            print("File not found: ", self.samplefile)
            self.samplesdf = None

        self.combodefaults = {'cuvette': ['600', '2000', '4000']}


    def prepare_form(self, Dialog):
        # load or reload data
        self.load_data()

        # form dicts
        edit_list = ['date', 'time', 'samplename', 'filename', 'smoothing', 'cal32', 'cal44', 'cons32', 'cons44',
                     'zero44', 'zero45', 'zero46', 'zero47', 'zero49']
        combo_list = ['user', 'membrane', 'cuvette']

        self.labels = defaultdict(defaultdict)
        self.edits = defaultdict(defaultdict)
        self.radios = defaultdict(defaultdict)
        self.combobox = defaultdict(defaultdict)
        self.labs = defaultdict(defaultdict)

        self.labs = {"time": "Time",
                     "date": "Date",
                     "samplename": "Sample Name",
                     "filename": "File Name",
                     "smoothing": "Smoothing",
                     "cuvette": "Cuvette",
                     "user": "User",
                     "membrane": "Membrane",
                     "cal44": "Calibration 44",
                     "cal32": "Calibration 32",
                     "cons32": "Consumption 32",
                     "cons44": "Consumption 44",
                     "zero32": "Zero 32",
                     "zero44": "Zero 44",
                     "zero45": "Zero 45",
                     "zero46": "Zero 46",
                     "zero47": "Zero 47",
                     "zero49": "Zero 49"}

        self.buttons = OrderedDict(sorted({'Apply': defaultdict(object), 'Delete': defaultdict(object)}.items()))

        xpos, ypos = 1, 0
        for row in self.samplesdf.iterrows():
            row_index = row[0]
            r = row[1]

            self.radios[row_index] = QtGui.QRadioButton(Dialog)
            self.radios[row_index].setObjectName(_fromUtf8("_".join(["radio", str(row_index)])))
            self.gridLayout.addWidget(self.radios[row_index], ypos+1, 0, 1, 1)

            for k in ['samplename', 'date', 'time', 'cuvette']:
                # create labels
                if ypos == 0:
                    self.labels[k] = QtGui.QLabel(Dialog)
                    self.labels[k].setObjectName(_fromUtf8("_".join(["label", k])))
                    self.labels[k].setText(str(self.labs[k]))
                    self.labels[k].setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    self.labels[k].setFont(self.font_labels)
                    self.gridLayout.addWidget(self.labels[k], 0, xpos, 1, 1)

                if k in edit_list:
                    self.edits[k][row_index] = QtGui.QLineEdit(Dialog)
                    self.edits[k][row_index].setObjectName(_fromUtf8("_".join(["edit", k, str(row_index)])))
                    self.edits[k][row_index].setText(str(r[k]))
                    self.edits[k][row_index].setFont(self.font_edits)

                    if k in ['time', 'date']:
                        self.edits[k][row_index].setFixedWidth(80)

                    self.gridLayout.addWidget(self.edits[k][row_index], ypos+1, xpos, 1, 1)

                elif k in combo_list:
                    self.combobox[k][row_index] = QtGui.QComboBox(Dialog)
                    self.combobox[k][row_index].setObjectName(_fromUtf8("_".join(["combo", k, str(row_index)])))
                    self.combobox[k][row_index].addItems(self.combodefaults[k])
                    self.combobox[k][row_index].setCurrentIndex(self.combobox[k][row_index].findText(str(r[k]), QtCore.Qt.MatchFixedString))
                    self.combobox[k][row_index].setFont(self.font_edits)
                    self.gridLayout.addWidget(self.combobox[k][row_index], ypos+1, xpos, 1, 1)

                xpos += 1

            # create buttons
            for k in self.buttons.keys():
                # if ypos > 0:
                    self.buttons[k][row_index] = QtGui.QPushButton(Dialog)
                    self.buttons[k][row_index].setObjectName(_fromUtf8("_".join(["event", k, "button", str(row_index)])))
                    self.buttons[k][row_index].setText(_translate("Dialog", k + str(row_index), None))
                    self.buttons[k][row_index].setFont(self.font_buttons)

                    if k == 'Apply':
                        self.buttons[k][row_index].clicked.connect(partial(self.ask_apply_changes, [row_index, Dialog]))
                        self.buttons[k][row_index].setStyleSheet("background-color: #ffeedd")

                    elif k == 'Delete':
                        self.buttons[k][row_index].clicked.connect(partial(self.ask_delete_confirm1, [row_index, Dialog]))
                        self.buttons[k][row_index].setStyleSheet("background-color: #ffcddd")

                    self.gridLayout.addWidget(self.buttons[k][row_index], ypos+1, xpos, 1, 1)
                    xpos += 1

            # increments
            ypos += 1
            xpos = 1
        Dialog.resize(1000, 70 + (30 * ypos))


        # self.add_row(Dialog)

    def ask_delete_confirm1(self, args):
        sid = args[0]
        Dialog = args[1]

        # check if radio button is checked.
        if self.radios[sid].isChecked():
            msg = "Are you sure you want to delete the following sample :  \n\n"
            details = ""
            for c in self.samplesdf.columns:
                details += str(c) + ": " + str(self.samplesdf.at[sid, c]) + "\n"
            reply = QtGui.QMessageBox.warning(self, 'Confirmation #1',
                                           msg + details, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                msg2 = "Are you sure REALLY REALLY sure you want to delete the following sample ? \n\n" + \
                       "This is the last confirmation message. After confirming, the files will be PERMANENTLY deleted and the data WILL be lost ! \n\n"

                msgbox = QtGui.QMessageBox.critical(self, 'Confirmation #2',
                               msg2 + details, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)


                reply2 = msgbox

                if reply2 ==  QtGui.QMessageBox.Yes:
                    # deletion confirmed
                    self.delete_confirmed(sid)
                    self.update_form( Dialog)

        else:
            QtGui.QMessageBox.question(self, 'Error', 'Please select the sample you want to delete on the left',
                                       QtGui.QMessageBox.Ok)

    def delete_confirmed(self, sid):
        # sample file
        filename = self.samplesdf.loc[sid, 'filename']

        # delete row in samplesdf
        self.samplesdf = self.samplesdf.drop(self.samplesdf.index[sid])
        self.samplesdf.to_csv(self.samplefile, index=False, encoding='ISO-8859-1')

        # delete file in rawdata
        if os.path.isfile(os.path.join(self.datafolder, "rawdata", filename)):
            os.remove(os.path.join(self.datafolder, "rawdata", filename))
            # print(" delete: ", os.path.join(self.datafolder, "rawdata", filename))

        # delete file in data
        if os.path.isfile(os.path.join(self.datafolder, filename)):
            os.remove(os.path.join(self.datafolder, filename))
            # print(" delete: ", os.path.join(self.datafolder, filename))

    def ask_apply_changes(self, args):
        sid = args[0]
        Dialog = args[1]

        newdata=defaultdict(str)
        for k in self.edits.keys():
            newdata[k] = self.edits[k][sid].text()
        for k in self.combobox.keys():
            newdata[k] = self.combobox[k][sid].currentText()

        details = ""
        for k in newdata:
            details += str(self.samplesdf.at[sid, k]) + '\t --> \t' + str(newdata[k]) + "\n"

        msg = "Are you sure you want to apply the changes to sample " + str(self.samplesdf.at[sid, 'samplename']) + " ?\n\n"
        reply = QtGui.QMessageBox.question(self, 'Modify a sample', msg + details, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.apply_changes_confirmed(sid, newdata)
            self.update_form(Dialog)
        else:
            print('cancel modification')

    def apply_changes_confirmed(self, sid, newdata):
        # rename files
        newdata['filename'] = str(newdata['date']) + "_" + str(newdata['samplename']) + ".csv"
        os.rename(os.path.join(self.datafolder, str(self.samplesdf.at[sid, 'filename'])),
                  os.path.join(self.datafolder, str(newdata['filename'])))
        os.rename(os.path.join(self.datafolder, "rawdata", str(self.samplesdf.at[sid, 'filename'])),
                  os.path.join(self.datafolder, "rawdata", str(newdata['filename'])))

        for k in newdata.keys():
            self.samplesdf.at[sid, k] = newdata[k]
            self.samplesdf.to_csv(self.samplefile, index=False, encoding='ISO-8859-1')

    def update_form(self, Dialog):
        # empty variables
        self.edits = None
        self.combobox = None
        self.buttons = None
        self.radios = None
        self.labs = None
        self.labels = None

        # empty layout
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)


        self.prepare_form(Dialog)


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Samples Manager", None))
        # self.label.setText(_translate("Dialog", "File", None))
