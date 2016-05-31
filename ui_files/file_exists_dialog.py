# -*- coding: utf-8 -*-


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


class newsample_dialog(QtGui.QWidget):
    
    def __init__(self):
        super(newsample_dialog, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.btn = QtGui.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)
        
        self.le = QtGui.QLineEdit(self)
        self.le.move(130, 22)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def setupUi(self, Calib_Dialog):
        self.btn = QtGui.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QtGui.QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()


        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Calib_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Calib_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Calib_Dialog)
        
    def showDialog(self):
        
        text, ok = QtGui.QInputDialog.getText(self, 'Sample already exists',
            'Suggested new sample name:')
        
        if ok:
            self.le.setText(str(text))
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = newsample_dialog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


    # @staticmethod
    # def calib_infos(parent = None):
    #     dialog = Ui_Calib_Dialog(parent)
    #     result = dialog.exec_()
    #
    #     membranefile = "C:\\Mass_Spec_Data\\_calibrations\\membranes.csv"
    #     membranedf = pd.read_csv(membranefile,index_col ='id')
    #     query="cuvette == " + dialog.box_cuvette.currentText()
    #     # print(query)
    #     # print(membranedf.query(query).sort('date', ascending=False).head(1).index[0])
    #     membraneid = membranedf.query(query).sort('date', ascending=False).head(1).index[0]
    #
    #     #returns bicarb CC, vol injection, cuvette, membrane id
    #     return str(dialog.txt_bicarb_cc.text()), str(dialog.txt_volinject.text()) , str(dialog.box_cuvette.currentText()),  membraneid