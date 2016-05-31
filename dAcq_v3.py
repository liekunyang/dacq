# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 16:59:00 2015

@author: Vincent Chochois / u5040252









####################################################################################################
INSTRUCTIONS:
####################################################################################################


 1. Select dAcq_v3 in top right corner of this window if not already selected
 2. Hit the play (green triangle) button next to it.

####################################################################################################



























"""




















































#from ui_files.main_ui import *
from ui_files.main2 import *

#dialog windows
from ui_files.userdialog import *
from ui_files.cuvettedialog import *
from ui_files.startdialog import *
from ui_files.calib_dialog import *
from ui_files.membrane_dialog import *
from ui_files.smoothingdialog import *


from PyQt4.QtGui import *
from PyQt4.QtCore import *  # inclut QTimer..
import pyqtgraph as pg # pour accès à certaines constantes pyqtgraph, widget, etc...))

from scipy import stats
import pandas as pd
import numpy as np
import peakutils
from functools import *



import sys, serial, array, time,  os, datetime



class pyMS(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        
        #configuration
        self.precision = 4  # decimal precision
        self.xscale = "sec" #x-axis scale
        self.last = ""

        self.datafolder = "C:\\Mass_Spec_Data\\"
        self.user = "Vincent"
        self.cuvette = "2000"
        self.smoothing = 60
        
        self.user = Ui_userDialog.getUser(user = self.user)
        if self.user == "":
            sys.exit("You have to select a username. Please create an empty folder in "+ self.datafolder + " if not in list.")

        self.cuvette = Ui_cuvetteDialog.getCuvette(cuvette = self.cuvette)
        if self.cuvette == "":
            sys.exit("You have to select a cuvette.")

        
        QMainWindow.__init__(self, parent)
        self.setupUi(parent) # Obligatoire

       

        #initialize variables
        self.sampledf = None
        self.exp_type = None
        self.reportmsg = ""
        self.ts={}
        self.ts['buffer_time'] = 1 #update rate in s

        self.today = datetime.date.today().strftime('%Y%m%d')
        self.ch = {32: 6, 34: 5, 36: 7,  40: 10, 44: 2, 45: 0, 46: 3, 47: 1, 49: 4}
        self.z = {32: 0,  34: 48, 36: 64, 40: 128, 44: 80, 45: 96, 46: 144, 47: 112, 49: 16}
        self.carbon_masses=[44,45,46,47,49]
        self.x_axisfactor={"sec": 1, "min":60}

        
        #deactivate events
        self.deactivate_events()

        self.actionAdd_O2_Calibration.setEnabled(False)
        self.actionAdd_Consumptions.setEnabled(False)

        # connect actions
        self.actionStart.triggered.connect(self.start)
        self.actionTestmode.triggered.connect(self.testmode)
        self.actionStop.triggered.connect(self.stop)
        self.actionAdd_new_Membrane.triggered.connect(self.set_membrane)
        self.actionAdd_CO2_Calibration.triggered.connect(self.set_CO2calibration)
        # self.actionAdd_O2_Calibration.triggered.connect(self.set_O2calibration)
        self.actionAdd_Electrical_Zeros.triggered.connect(self.set_zeros)
        # self.actionAdd_Consumptions.triggered.connect(self.set_consumption)
        self.actionUser.triggered.connect(self.change_user)
        self.actionCuvette.triggered.connect(self.change_cuvette)
        self.actionDatafolder.triggered.connect(self.change_datafolder)
        self.actionSmoothing.triggered.connect(self.change_smoothing)
       
#        self.btn_bic.clicked.connect(self.event_bic)
#        self.btn_cells.clicked.connect(self.event_cells)
#        self.btn_lighton.clicked.connect(self.event_lightON)
#        self.btn_lightoff.clicked.connect(self.event_lightOFF)
#        self.btn_az.clicked.connect(self.event_az)
#        self.btn_ez.clicked.connect(self.event_ez)
#        self.btn_custom.clicked.connect(self.event_custom)
        
        self.btn_bic.clicked.connect(partial(self.event_add, "BIC"))
        self.btn_cells.clicked.connect(partial(self.event_add, "CELLS"))
        self.btn_lighton.clicked.connect(partial(self.event_add, "LIGHT ON"))
        self.btn_lightoff.clicked.connect(partial(self.event_add, "LIGHT OFF"))
        self.btn_az.clicked.connect(partial(self.event_add, "AZ"))
        self.btn_ez.clicked.connect(partial(self.event_add, "EZ"))  
        self.btn_custom.clicked.connect(partial(self.event_add, "CUSTOM"))
 

        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Insert), self.btn_bic, partial(self.event_add, "BIC"))
        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_PageDown), self.btn_cells,  partial(self.event_add, "CELLS"))
        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_PageUp), self.btn_custom,  partial(self.event_add, "CUSTOM"))

        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Left), self.btn_lighton,  partial(self.event_add, "LIGHT ON"))
        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Right), self.btn_lightoff,  partial(self.event_add, "LIGHT OFF"))

        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_End), self.btn_az,  partial(self.event_add, "AZ"))
        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Home), self.btn_ez,  partial(self.event_add, "EZ"))

        self.__init__graphs()

        # open serial port
        self.ser = serial.Serial(0)


    def __init__graphs(self):
        # general graph config
        labelStyle = {'color': '#555', 'font-size': '10pt'} # propriétés CSS à utiliser pour le label
        pg.setConfigOptions(antialias=True)
        
        
        # RAWDATA GRAPH
        self.graph_rawdata.setBackgroundBrush(QBrush(QColor(Qt.white))) # la classe PlotWidget est un GraphicsWidget qui est un QGraphics View
        self.graph_rawdata.showGrid(x=True, y=True)  # affiche la grille
        self.graph_rawdata.getAxis('bottom').setPen(pg.mkPen(150,150,150)) # couleur de l'axe + grille
        self.graph_rawdata.getAxis('left').setPen(pg.mkPen(150,150,150)) # couleur de l'axe + grille

        self.graph_rawdata.getAxis('bottom').setLabel('Time', units=self.xscale, **labelStyle) # label de l'axe
        self.graph_rawdata.getAxis('left').setLabel('Concentration', units='micromole/L', **labelStyle) # label de l'axe

        # self.graph_rawdata.getViewBox().setMouseMode(pg.ViewBox.RectMode)  # fonction ViewBox pas accessible depuis PlotWidget : fixe selection par zone
        self.graph_rawdata.setMouseEnabled(x=True, y=True)

        #ENRICHRATE GRAPH
        self.graph_enrichrate.setBackgroundBrush(QBrush(QColor(Qt.white))) # la classe PlotWidget est un GraphicsWidget qui est un QGraphics View
        self.graph_enrichrate.showGrid(x=True, y=True)  # affiche la grille
        self.graph_enrichrate.getAxis('bottom').setPen(pg.mkPen(150,150,150)) # couleur de l'axe + grille
        self.graph_enrichrate.getAxis('left').setPen(pg.mkPen(150,100,150)) # couleur de l'axe + grille

        self.graph_enrichrate.getAxis('bottom').setLabel('Time', units=self.xscale, **labelStyle) # label de l'axe
        self.graph_enrichrate.getAxis('left').setLabel('Rate', units='min-1', **labelStyle) # label de l'axe

        # self.graph_enrichrate.getViewBox().setMouseMode(pg.ViewBox.RectMode)  # fonction ViewBox pas accessible depuis PlotWidget : fixe selection par zone
        self.graph_enrichrate.setMouseEnabled(x=True, y=True)

        #Create empty curves
        linewidth = 1
        self.Courbe_Mass32 = self.graph_rawdata.plot(pen=pg.mkPen([250,0,0], width=linewidth), name='Mass32')
        self.Courbe_Mass40 = self.graph_rawdata.plot(pen=pg.mkPen([200,150,0], width=linewidth), name='Mass40')
        self.Courbe_Mass44 = self.graph_rawdata.plot(pen=pg.mkPen([0,250,0], width=linewidth), name='Mass44')
        self.Courbe_Mass45 = self.graph_rawdata.plot(pen=pg.mkPen([50,200,250], width=linewidth), name='Mass45')
        self.Courbe_Mass46 = self.graph_rawdata.plot(pen=pg.mkPen([250,150,250], width=linewidth), name='Mass46')
        self.Courbe_Mass47 = self.graph_rawdata.plot(pen=pg.mkPen([0,100,250], width=linewidth), name='Mass47')
        self.Courbe_Mass49 = self.graph_rawdata.plot(pen=pg.mkPen([100,0,250], width=linewidth), name='Mass49')
        self.Courbe_totalCO2 = self.graph_rawdata.plot(pen=pg.mkPen([0,0,0], width=linewidth), name='TotalCO2')# DashDotline DashLine DashDotDotLine ...
        self.Courbe_logE49 = self.graph_rawdata.plot(pen=pg.mkPen([150,150,150], width=linewidth, style=QtCore.Qt.DashLine), name='LogEnrich')

        self.Courbe_enrichrate47=self.graph_enrichrate.plot(pen=pg.mkPen([0,100,250], width=linewidth, style=QtCore.Qt.DashLine), name='ER47')
        self.Courbe_enrichrate49=self.graph_enrichrate.plot(pen=pg.mkPen([100,0,250], width=linewidth, style=QtCore.Qt.DashLine), name='ER49')
        self.Courbe_O2evol=self.graph_enrichrate.plot(pen=pg.mkPen([250,0,0], width=linewidth), name='O2evol')
        self.Courbe_d40dt=self.graph_enrichrate.plot(pen=pg.mkPen([200,150,0], width=linewidth), name='dM40dt')
        self.Courbe_d44dt=self.graph_enrichrate.plot(pen=pg.mkPen([0,250,0], width=linewidth), name='dM44dt')
        self.Courbe_d45dt=self.graph_enrichrate.plot(pen=pg.mkPen([50,200,250], width=linewidth), name='dM45dt')
        self.Courbe_d46dt=self.graph_enrichrate.plot(pen=pg.mkPen([250,150,250], width=linewidth), name='dM46dt')
        self.Courbe_d47dt=self.graph_enrichrate.plot(pen=pg.mkPen([0,100,250], width=linewidth), name='dM47dt')
        self.Courbe_d49dt=self.graph_enrichrate.plot(pen=pg.mkPen([100,0,250], width=linewidth), name='dM49dt')
        self.Courbe_dtotalCO2dt=self.graph_enrichrate.plot(pen=pg.mkPen([0,0,0], width=linewidth), name='dtotalCO2dt')





    def start(self):
        print("start... ", self.exp_type)
        
        #change units to volts
        self.lab_M32unit.setText(" µM")
        self.lab_M40unit.setText(" V")
        self.lab_M44unit.setText(" µM")
        self.lab_M45unit.setText(" µM")
        self.lab_M46unit.setText(" µM")
        self.lab_M47unit.setText(" µM")
        self.lab_M49unit.setText(" µM")
        self.lab_totCO2unit.setText(" µM")
        
        self.lab_ER47unit.setText(" min-1")
        self.lab_ER49unit.setText(" min-1")
        self.lab_O2evolunit.setText(" µM.min-1")
        self.lab_d40dtunit.setText(" µM.min-1")
        self.lab_d44dtunit.setText(" µM.min-1")
        self.lab_d45dtunit.setText(" µM.min-1")
        self.lab_d46dtunit.setText(" µM.min-1")
        self.lab_d47dtunit.setText(" µM.min-1")
        self.lab_d49dtunit.setText(" µM.min-1")
        self.lab_dtotalCO2dtunit.setText(" µM.min-1")



        # get infos from startDialog
        self.samplename = Ui_StartDialog.getStartData(user = self.user, datafolder = self.datafolder)

        if self.samplename!='':
            self.today = datetime.date.today().strftime('%Y%m%d')

            #clear graphs
            self.graph_rawdata.clear()
            self.graph_enrichrate.clear()
            self.__init__graphs()

            #disable menus
            self.actionAdd_CO2_Calibration.setEnabled(False)
            self.actionStart.setEnabled(False)
            self.actionAdd_O2_Calibration.setEnabled(False)
            self.actionAdd_Consumptions.setEnabled(False)
            self.actionAdd_Electrical_Zeros.setEnabled(False)

            #activate events
            self.activate_events()


            #build filenames
            self.dffilename = os.path.join(self.datafolder, self.user, self.today, "rawdata", self.today + "_" + str(self.samplename) + ".csv")
            self.dfccfilename = os.path.join(self.datafolder, self.user, self.today, self.today + "_" + str(self.samplename) + ".csv")
            self.membranefile = os.path.join(str(self.datafolder),  "_calibrations", "membranes.csv")
            self.calfile = os.path.join(str(self.datafolder),  "_calibrations", "cal.csv")
            self.targetfolder = os.path.join(self.datafolder, self.user, self.today)

            #check if file exists
            self.check_file_exists()


            # get membrane
            membranedf = pd.read_csv(self.membranefile)
            q="date < " + self.today + " & cuvette==" + str(self.cuvette)
            self.membraneid = int(membranedf.query(q).sort('date', ascending=False).reset_index().head(1)['id'][0])
            membranedf = None


            # calibration (includes membraneid)

            if self.exp_type != "CO2calib" and self.exp_type != "O2calib" and self.exp_type != "zeros" and self.exp_type != "consumption":
                self.cal = self.get_calibration()
                print(self.cal)

            #samplefile
            self.create_samplefile()

            #initialize timer
            self.exp_start = time.time()
            self.packet_start = time.time()

            # initialise variables
            self.dfcolumns = ['time', 'Mass32', 'Mass40', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49','eventtype','eventdetails']
            self.dfcccolumns = ['time', 'Mass32', 'Mass40', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49','eventtype','eventdetails','totalCO2','logE47','logE49','O2evol','enrichrate47','enrichrate49', 'd40dt', 'd44dt', 'd45dt', 'd46dt', 'd47dt', 'd49dt','dtotalCO2dt']
            self.df = pd.DataFrame(data=np.zeros((0,len(self.dfcolumns))), columns=self.dfcolumns)
            self.dfcc=pd.DataFrame(data=np.zeros((0,len(self.dfcccolumns))), columns=self.dfcccolumns)
            self.total_time = 0
            self.total_packets = 0

            # flush buffer
            self.ser.flushInput()

            # start timer
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.myupdate)
            self.timer.start(self.ts['buffer_time'] * 1000)

            #csv saving timer // saves CSV only every 5 seconds to save resources
            self.save_csv()
            self.timer2 = QtCore.QTimer(self)
            self.timer2.timeout.connect(self.save_csv)
            self.timer2.start(5000)

        else:
            print("dialog rejected, cancelling acquisition...")
            self.stop()

    def testmode(self):
        print("start testmode...")
        self.exp_type = "test"
        
        #change units to volts
        self.lab_M32unit.setText(" V")
        self.lab_M40unit.setText(" V")
        self.lab_M44unit.setText(" V")
        self.lab_M45unit.setText(" V")
        self.lab_M46unit.setText(" V")
        self.lab_M47unit.setText(" V")
        self.lab_M49unit.setText(" V")
        self.lab_totCO2unit.setText(" V")
        
        self.lab_ER47unit.setText(" min-1")
        self.lab_ER49unit.setText(" min-1")
        self.lab_O2evolunit.setText(" V.min-1")
        self.lab_d40dtunit.setText(" V.min-1")
        self.lab_d44dtunit.setText(" V.min-1")
        self.lab_d45dtunit.setText(" V.min-1")
        self.lab_d46dtunit.setText(" V.min-1")
        self.lab_d47dtunit.setText(" V.min-1")
        self.lab_d49dtunit.setText(" V.min-1")
        self.lab_dtotalCO2dtunit.setText(" V.min-1")


        self.today = datetime.date.today().strftime('%Y%m%d')

        #clear graphs
        self.graph_rawdata.clear()
        self.graph_enrichrate.clear()
        self.__init__graphs()

        #disable menus
        self.actionAdd_CO2_Calibration.setEnabled(False)
        self.actionStart.setEnabled(False)
        self.actionTestmode.setEnabled(False)
        self.actionAdd_O2_Calibration.setEnabled(False)
        self.actionAdd_Consumptions.setEnabled(False)
        self.actionAdd_Electrical_Zeros.setEnabled(False)

        #activate events
        self.activate_events()


        #initialize timer
        self.exp_start = time.time()
        self.packet_start = time.time()

        # initialise variables
        self.dfcolumns = ['time', 'Mass32', 'Mass40', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49','eventtype','eventdetails']
        self.dfcccolumns = ['time', 'Mass32', 'Mass40', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49','eventtype','eventdetails','totalCO2','logE47','logE49','O2evol','enrichrate47','enrichrate49', 'd40dt', 'd44dt', 'd45dt', 'd46dt', 'd47dt', 'd49dt','dtotalCO2dt']
        self.df = pd.DataFrame(data=np.zeros((0,len(self.dfcolumns))), columns=self.dfcolumns)
        self.dfcc=pd.DataFrame(data=np.zeros((0,len(self.dfcccolumns))), columns=self.dfcccolumns)
        self.total_time = 0
        self.total_packets = 0

        # flush buffer
        self.ser.flushInput()

        # start timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.myupdate_testmode)
        self.timer.start(self.ts['buffer_time'] * 1000)


    def check_file_exists(self):
        while os.path.exists(self.dffilename):

            sugsamplename=self.samplename

            # create suggested sample name
            while os.path.exists(self.dffilename):
                if "_" in sugsamplename:
                    try: #if there's already a number, try to increment it
                        incstr = sugsamplename.split("_")[-1]
                        inc=int(incstr)
                        inc+=1
                        sugsamplename = sugsamplename.rstrip("_" + incstr) + "_" + str(inc)


                    except ValueError: #else just add a number
                        sugsamplename = sugsamplename + "_2"
                else:
                    sugsamplename = sugsamplename + "_2"

                self.dffilename = os.path.join(self.datafolder, self.user, self.today, "rawdata", self.today + "_" + str(sugsamplename) + ".csv")


            #open a dialog to ask for a new sample name
            newsample, ok = QtGui.QInputDialog.getText(self, "Sample already exists",
                    "Suggested new sample name for '<b>"+ self.samplename + "</b>' :", QtGui.QLineEdit.Normal,
                    sugsamplename)


            #new name not empty and "OK" button clicked :
            if ok and newsample != '':
                self.samplename = str(newsample)
                self.dffilename   = os.path.join(self.datafolder, self.user, self.today, "rawdata", self.today + "_" + str(newsample) + ".csv")
                self.dfccfilename = os.path.join(self.datafolder, self.user, self.today, self.today + "_" + str(newsample) + ".csv")
                return str(newsample)







       
    def stop(self):
        print("STOP")
        self.timer.stop()

        if self.exp_type != "test":
            self.timer2.stop()

        #enable menus
        self.actionAdd_CO2_Calibration.setEnabled(True)
        self.actionStart.setEnabled(True)
        self.actionTestmode.setEnabled(True)

        self.actionAdd_O2_Calibration.setEnabled(False)
        self.actionAdd_Consumptions.setEnabled(False)
        self.actionAdd_Electrical_Zeros.setEnabled(True)

        #deactivate events
        self.deactivate_events()

        # if this is a calibration, then do calculations
        if self.exp_type == "CO2calib":
            #calculate CO2 calibration
            self.CO2_calibration()
            
        elif self.exp_type == "O2calib":
            #calculate O2 calibration
            self.calculate_O2calib()
            
            
        elif self.exp_type == "zeros":
            #calculate zeros
            self.zeros_calibration()
            
        elif self.exp_type == "consumption":
            #calculate Co2 calibration
            self.calculate_consumption()
            
        else:   #normal experiment
            pass

        #reset important variables
        self.exp_type = None
        self.exp_start = None
        self.df=None
        self.dfcc=None
        self.cal=None




    
    
    
    def create_samplefile(self):
        #Create or append to samples file
        self.samplefile = os.path.join(self.targetfolder, self.today + "_SAMPLES.csv" )
        
        self.sampleline = [self.today, str(time.strftime('%H:%M:%S')), self.user, self.samplename, self.today + "_" + self.samplename + ".csv", str(self.cuvette),  str(self.membraneid)]

        #append to dataframe
        try:
            self.sampledf = pd.read_csv(self.samplefile)
            self.sampledf.loc[len(self.sampledf.index)] = self.sampleline

        except OSError:
            columns = ['date','time','user','samplename','filename','cuvette','membraneid']
            self.sampledf = pd.DataFrame(data=np.zeros((0,len(columns))), columns=columns)
            self.sampledf.loc[len(self.sampledf.index)] = self.sampleline
            
        #save to file
        self.sampledf.to_csv(self.samplefile, index=False, encoding='ISO-8859-1')


    def set_membrane(self):
        Ui_Membrane_Dialog.add_membrane()
        pass




    def set_CO2calibration(self):
        self.exp_type = "CO2calib"
        self.calib_bicarb_cc, self.calib_volinject = Ui_Calib_Dialog.calib_infos()


        #find membrane id
        membranefile = "C:\\Mass_Spec_Data\\_calibrations\\membranes.csv"
        membranedf = pd.read_csv(membranefile,index_col ='id')
        query="cuvette == " + self.cuvette
        membraneid = membranedf.query(query).sort('date', ascending=False).head(1).index[0]
        print('membraneid = ', membraneid )

        # activate 44 only 
        self.chk_M32.setChecked(False)
        self.chk_M40.setChecked(False)
        self.chk['44'].setChecked(True)
        self.chk_M45.setChecked(False)
        self.chk_M46.setChecked(False)
        self.chk_M47.setChecked(False)
        self.chk_M49.setChecked(False)
        self.chk_totalCO2.setChecked(False)

        self.chk_logE.setChecked(False)
        self.chk_O2evol.setChecked(False)
        self.chk_ER47.setChecked(False)
        self.chk_ER49.setChecked(False)
        self.chk_d40dt.setChecked(False)
        self.chk_d44dt.setChecked(True)
        self.chk_d45dt.setChecked(False)
        self.chk_d46dt.setChecked(False)
        self.chk_d47dt.setChecked(False)
        self.chk_d49dt.setChecked(False)
        self.chk_dtotalCO2dt.setChecked(False)
        
        #change units to volts
        self.lab_M32unit.setText(" V")
        self.lab_M40unit.setText(" V")
        self.lab_M44unit.setText(" V")
        self.lab_M45unit.setText(" V")
        self.lab_M46unit.setText(" V")
        self.lab_M47unit.setText(" V")
        self.lab_M49unit.setText(" V")
        self.lab_totCO2unit.setText(" V")
        
        self.lab_ER47unit.setText(" min-1")
        self.lab_ER49unit.setText(" min-1")
        self.lab_O2evolunit.setText(" V.min-1")
        self.lab_d40dtunit.setText(" V.min-1")
        self.lab_d44dtunit.setText(" V.min-1")
        self.lab_d45dtunit.setText(" V.min-1")
        self.lab_d46dtunit.setText(" V.min-1")
        self.lab_d47dtunit.setText(" V.min-1")
        self.lab_d49dtunit.setText(" V.min-1")
        self.lab_dtotalCO2dtunit.setText(" V.min-1")

        self.start()
        pass    
    
    
    
    
    def set_zeros(self):
        self.exp_type = "zeros"

        # activate 44 only
        self.chk_M32.setChecked(False)
        self.chk_M40.setChecked(False)
        self.chk['44'].setChecked(True)
        self.chk_M45.setChecked(True)
        self.chk_M46.setChecked(True)
        self.chk_M47.setChecked(True)
        self.chk_M49.setChecked(True)
        self.chk_totalCO2.setChecked(True)

        self.chk_logE.setChecked(False)
        self.chk_O2evol.setChecked(False)
        self.chk_ER47.setChecked(False)
        self.chk_ER49.setChecked(False)
        self.chk_d40dt.setChecked(False)
        self.chk_d44dt.setChecked(True)
        self.chk_d45dt.setChecked(True)
        self.chk_d46dt.setChecked(True)
        self.chk_d47dt.setChecked(True)
        self.chk_d49dt.setChecked(True)
        self.chk_dtotalCO2dt.setChecked(True)
        
        #change units to volts
        self.lab_M32unit.setText(" V")
        self.lab_M40unit.setText(" V")
        self.lab_M44unit.setText(" V")
        self.lab_M45unit.setText(" V")
        self.lab_M46unit.setText(" V")
        self.lab_M47unit.setText(" V")
        self.lab_M49unit.setText(" V")
        self.lab_totCO2unit.setText(" V")
        
        self.lab_ER47unit.setText(" min-1")
        self.lab_ER49unit.setText(" min-1")
        self.lab_O2evolunit.setText(" V.min-1")
        self.lab_d40dtunit.setText(" V.min-1")
        self.lab_d44dtunit.setText(" V.min-1")
        self.lab_d45dtunit.setText(" V.min-1")
        self.lab_d46dtunit.setText(" V.min-1")
        self.lab_d47dtunit.setText(" V.min-1")
        self.lab_d49dtunit.setText(" V.min-1")
        self.lab_dtotalCO2dtunit.setText(" V.min-1")

        self.start()

        pass   
    
    
    
    
    def set_O2calibration(self):
        self.exp_type = "O2calib"

        self.chk_M32.setChecked(True)
        self.chk_M40.setChecked(False)
        self.chk['44'].setChecked(False)
        self.chk_M45.setChecked(False)
        self.chk_M46.setChecked(False)
        self.chk_M47.setChecked(False)
        self.chk_M49.setChecked(False)
        self.chk_totalCO2.setChecked(False)

        self.chk_logE.setChecked(False)
        self.chk_O2evol.setChecked(True)
        self.chk_ER47.setChecked(False)
        self.chk_ER49.setChecked(False)
        self.chk_d40dt.setChecked(False)
        self.chk_d44dt.setChecked(False)
        self.chk_d45dt.setChecked(False)
        self.chk_d46dt.setChecked(False)
        self.chk_d47dt.setChecked(False)
        self.chk_d49dt.setChecked(False)
        self.chk_dtotalCO2dt.setChecked(False)
        # self.start()

        pass  
    
    
    
    
    def set_consumption(self):
        self.exp_type = "consumption"
        # self.start()

        pass    





    def get_calibration(self):

        # load calibration file path
        caldf = pd.read_csv(self.calfile)
        
        calibration = {'membraneid':self.membraneid,
                       'calfile':self.calfile}

        for what in ['cal32','cal44','zero32','zero40','zero44','zero45','zero46','zero47','zero49','cons32','cons44']:
            q="date <= {} & cuvette=={} & type=='{}'".format(self.today, str(self.cuvette), what)
            calibration[what] = float(caldf.query(q).sort('date', ascending=False).head(1)['value'])

        return calibration
                             

        
        
    def myupdate(self):
        #check if events are activated:
        if not self.btn_bic.isEnabled():
            self.activate_events()

        self.previous_packet = self.packet_start
        self.packet_start  = time.time()
        u=array.array("B", self.ser.read(self.ser.inWaiting()))

        # split packets
        self.newdata = "-".join(map(str, u)).split("255-255-255-255")
        
        #how many packets in the buffeR ?
        self.ts['npackets'] = len(self.newdata)-1

        if self.total_packets > 0: 
            #stick first packet with last packet of previous buffer
            self.newdata[0] = self.last + "-" + self.newdata[0]
        else:
            #remove first packet
            self.newdata = self.newdata[1:len(self.newdata)]
        
        self.last =  self.newdata[-1]

        # calculate time between 2 packets

        if self.ts['npackets'] > 0:
            self.getvolts2()
            self.df = self.df.append(self.lastdf, ignore_index=True)
            self.dfcc = self.dfcc.append(self.lastdf, ignore_index=True)

        #calculate concentrations and deriavatives
        self.update_data()

        # update graphs
        self.update_graph()

        # update UI
        self.update_UI()





    def save_csv(self):
        if self.exp_type!='test':
            self.df.to_csv(self.dffilename, index=False, encoding='ISO-8859-1')

            if self.exp_type==None:
                self.dfcc.to_csv(self.dfccfilename, index=False, encoding='ISO-8859-1')






    def myupdate_testmode(self):
        #check if events are activated:
        if not self.btn_bic.isEnabled():
            self.activate_events()

        self.previous_packet = self.packet_start
        self.packet_start  = time.time()

        # get data from buffer and put it into a bytearray
        u=array.array("B", self.ser.read(self.ser.inWaiting()))

        # split packets
        self.newdata = "-".join(map(str, u)).split("255-255-255-255")

        # count full packets in buffer, excluding 1st and last which may be incomplete
        self.ts['npackets'] = len(self.newdata)-1


        
        if self.total_packets > 0: 
            #stick first packet with last packet of previous buffer
            self.newdata[0] = self.last + "-" + self.newdata[0]
        else:
            #remove first packet
            self.newdata = self.newdata[1:len(self.newdata)]
        
        
        self.last =  self.newdata[-1]
        
        
        # calculate time between 2 packets
        self.ts['packet_time'] = (self.packet_start-self.previous_packet) / self.ts['npackets']

        if self.ts['npackets'] > 0:
            self.getvolts2()
            self.df = self.df.append(self.lastdf, ignore_index=True)
            self.dfcc = self.dfcc.append(self.lastdf, ignore_index=True)

        #calculate concentrations and slopes
        self.update_data()

        # update UI
        self.update_UI()

        # update graphs
        self.update_graph()





    def update_data(self):
        if self.exp_type == None: #calculate concentrations and enrichrate
            #oxygen
            self.dfcc.loc[:,'Mass32'] = (self.df['Mass32'] - self.cal['zero32']) * self.cal['cal32']
            
            #Carbon
            for mass in [44,45,46,47,49]:
                self.dfcc.loc[:,'Mass' + str(mass)] = (self.df['Mass' + str(mass)] - self.cal['zero' + str(mass)]) * self.cal['cal44']
            

        else:
            for mass in [44,45,46,47,49,32]:
                self.dfcc.loc[:,'Mass' + str(mass)] = self.df['Mass' + str(mass)]


        self.dfcc['avgdt'] = self.dfcc.time.diff().mean()
        self.dfcc['time2'] = self.dfcc.avgdt.cumsum().apply(lambda x: round(x, 1))
        self.dfcc.loc[:,'totalCO2'] = self.dfcc.Mass44 + self.dfcc.Mass45 + self.dfcc.Mass46 + self.dfcc.Mass47 + self.dfcc.Mass49
        
        
        self.dfcc.loc[:, 'logE47'] = np.log10(100*self.dfcc.Mass47 / (self.dfcc.Mass45 + self.dfcc.Mass47 + self.dfcc.Mass49))
        self.dfcc.loc[:, 'logE49'] = np.log10(100*self.dfcc.Mass49 / (self.dfcc.Mass45 + self.dfcc.Mass47 + self.dfcc.Mass49))


        
        if self.total_packets > int(self.smoothing): 
            
            self.smoothing_window  =  int(self.smoothing) + len(self.lastdf)     
            self.regdf = self.dfcc.tail(self.smoothing_window).copy()

            # calculate enrichment
            self.regdf.loc[:,'O2evol']          = pd.rolling_apply(self.regdf.time2, int(self.smoothing), self.linearRegSlope, center = True, kwargs = {'col':"Mass32"})
            self.regdf.loc[:,'enrichrate47']    = pd.rolling_apply(self.regdf.time2, int(self.smoothing), self.linearRegSlope, center = True, kwargs = {'col':"logE47"})
            self.regdf.loc[:,'enrichrate49']    = pd.rolling_apply(self.regdf.time2, int(self.smoothing), self.linearRegSlope, center = True, kwargs = {'col':"logE49"})
            self.regdf.loc[:,'d40dt']           = pd.rolling_apply(self.regdf.time2, int(self.smoothing), self.linearRegSlope, center = True, kwargs = {'col':"Mass40"})
            self.regdf.loc[:,'d44dt']           = pd.rolling_apply(self.regdf.time2, int(self.smoothing), self.linearRegSlope, center = True, kwargs = {'col':"Mass44"})
            self.regdf.loc[:,'d45dt']           = pd.rolling_apply(self.regdf.time2, int(self.smoothing), self.linearRegSlope, center = True, kwargs = {'col':"Mass45"})
            self.regdf.loc[:,'d46dt']           = pd.rolling_apply(self.regdf.time2, int(self.smoothing), self.linearRegSlope, center = True, kwargs = {'col':"Mass46"})
            self.regdf.loc[:,'d47dt']           = pd.rolling_apply(self.regdf.time2, int(self.smoothing), self.linearRegSlope, center = True, kwargs = {'col':"Mass47"})
            self.regdf.loc[:,'d49dt']           = pd.rolling_apply(self.regdf.time2, int(self.smoothing), self.linearRegSlope, center = True, kwargs = {'col':"Mass49"})
            self.regdf.loc[:,'dtotalCO2dt']     = pd.rolling_apply(self.regdf.time2, int(self.smoothing), self.linearRegSlope, center = True, kwargs = {'col':"totalCO2"})
            
            self.dfcc.ix[self.dfcc.time.isin(self.regdf.loc[self.regdf.O2evol.notnull(),'time'].values),['O2evol','enrichrate47','enrichrate49', 'd40dt', 'd44dt', 'd45dt', 'd46dt', 'd47dt', 'd49dt','dtotalCO2dt','time2']] = self.regdf.ix[self.regdf.O2evol.notnull(),['O2evol','enrichrate47','enrichrate49', 'd40dt', 'd44dt', 'd45dt', 'd46dt', 'd47dt', 'd49dt','dtotalCO2dt','time2']]

        else:
            self.dfcc.loc[:,'O2evol']          = 0
            self.dfcc.loc[:,'enrichrate47']    = 0
            self.dfcc.loc[:,'enrichrate49']    = 0
            self.dfcc.loc[:,'d40dt']           = 0
            self.dfcc.loc[:,'d44dt']           = 0
            self.dfcc.loc[:,'d45dt']           = 0
            self.dfcc.loc[:,'d46dt']           = 0
            self.dfcc.loc[:,'d47dt']           = 0
            self.dfcc.loc[:,'d49dt']           = 0
            self.dfcc.loc[:,'dtotalCO2dt']     = 0
     




    def update_UI(self):
        self.lab_40.setText(str(round(self.dfcc.ix[len(self.dfcc.time)-1,'Mass40'],self.precision)))
        self.lab_32.setText(str(round(self.dfcc.ix[len(self.dfcc.time)-1,'Mass32'],self.precision)))
        self.lab_45.setText(str(round(self.dfcc.ix[len(self.dfcc.time)-1,'Mass45'],self.precision)))  
        self.lab_44.setText(str(round(self.dfcc.ix[len(self.dfcc.time)-1,'Mass44'],self.precision)))     
        self.lab_47.setText(str(round(self.dfcc.ix[len(self.dfcc.time)-1,'Mass47'],self.precision)))     
        self.lab_46.setText(str(round(self.dfcc.ix[len(self.dfcc.time)-1,'Mass46'],self.precision)))
        self.lab_49.setText(str(round(self.dfcc.ix[len(self.dfcc.time)-1,'Mass49'],self.precision)))
        self.lab_totalCO2.setText(str(round(self.dfcc.ix[len(self.dfcc.time)-1,'totalCO2'],self.precision)))
        self.lab_logE.setText(str(round(self.dfcc.ix[len(self.dfcc.time)-1,'logE49'],self.precision)))
            
        if self.total_packets > self.smoothing:
            self.lab_d40dt.setText(str(round(self.dfcc.loc[self.dfcc.d40dt.notnull(),'d40dt'].values[-1],self.precision)))
            self.lab_d44dt.setText(str(round(self.dfcc.loc[self.dfcc.d44dt.notnull(),'d44dt'].values[-1],self.precision)))
            self.lab_d45dt.setText(str(round(self.dfcc.loc[self.dfcc.d45dt.notnull(),'d45dt'].values[-1],self.precision)))
            self.lab_d46dt.setText(str(round(self.dfcc.loc[self.dfcc.d46dt.notnull(),'d46dt'].values[-1],self.precision)))
            self.lab_d47dt.setText(str(round(self.dfcc.loc[self.dfcc.d47dt.notnull(),'d47dt'].values[-1],self.precision)))
            self.lab_d49dt.setText(str(round(self.dfcc.loc[self.dfcc.d49dt.notnull(),'d49dt'].values[-1],self.precision)))
            self.lab_dtotalCO2dt.setText(str(round(self.dfcc.loc[self.dfcc.dtotalCO2dt.notnull(),'dtotalCO2dt'].values[-1],self.precision)))
    
            self.lab_O2evol.setText(str(round(self.dfcc.loc[self.dfcc.O2evol.notnull(),'O2evol'].values[-1],self.precision)))
            self.lab_ER47.setText(str(round(self.dfcc.loc[self.dfcc.enrichrate47.notnull(),'enrichrate47'].values[-1],self.precision)))
            self.lab_ER49.setText(str(round(self.dfcc.loc[self.dfcc.enrichrate49.notnull(),'enrichrate49'].values[-1],self.precision)))


          
          
          
    def update_graph(self):
        #update rawdata graph
        if self.chk_M32.isChecked():
            self.Courbe_Mass32.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['Mass32']))
        else:
            self.Courbe_Mass32.clear()


        if self.chk_M40.isChecked():
            self.Courbe_Mass40.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['Mass40']))
        else:
            self.Courbe_Mass40.clear()
            

        if self.chk['44'].isChecked():
            self.Courbe_Mass44.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['Mass44']))
        else:
            self.Courbe_Mass44.clear()
            

        if self.chk_M45.isChecked():
            self.Courbe_Mass45.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['Mass45']))
        else:
            self.Courbe_Mass45.clear()
            

        if self.chk_M46.isChecked():
            self.Courbe_Mass46.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['Mass46']))
        else:
            self.Courbe_Mass46.clear()
            

        if self.chk_M47.isChecked():
            self.Courbe_Mass47.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['Mass47']))
        else:
            self.Courbe_Mass47.clear()
            

        if self.chk_M49.isChecked():
            self.Courbe_Mass49.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['Mass49']))
        else:
            self.Courbe_Mass49.clear()
            

        if self.chk_logE.isChecked():
            self.Courbe_logE49.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['logE49']))
        else:
            self.Courbe_logE49.clear()
            

        if self.chk_totalCO2.isChecked():
            self.Courbe_totalCO2.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['totalCO2']))
        else:
            self.Courbe_totalCO2.clear()






        if self.total_packets >= self.smoothing: 
            # update rates graph
            if self.chk_O2evol.isChecked():
                self.Courbe_O2evol.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['O2evol']))
            else:
                self.Courbe_O2evol.clear()
    
            if self.chk_ER47.isChecked():
                self.Courbe_enrichrate47.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['enrichrate47']))
            else:
                self.Courbe_enrichrate47.clear()
    
            if self.chk_ER49.isChecked():
                self.Courbe_enrichrate49.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['enrichrate49']))
            else:
                self.Courbe_enrichrate49.clear()
    
            if self.chk_d40dt.isChecked():
                self.Courbe_d40dt.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['d40dt']))
            else:
                self.Courbe_d40dt.clear()
    
            if self.chk_d44dt.isChecked():
                self.Courbe_d44dt.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['d44dt']))
            else:
                self.Courbe_d44dt.clear()
    
            if self.chk_d45dt.isChecked():
                self.Courbe_d45dt.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['d45dt']))
            else:
                self.Courbe_d45dt.clear()
    
            if self.chk_d46dt.isChecked():
                self.Courbe_d46dt.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['d46dt']))
            else:
                self.Courbe_d46dt.clear()
    
            if self.chk_d47dt.isChecked():
                self.Courbe_d47dt.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['d47dt']))
            else:
                self.Courbe_d47dt.clear()
    
            if self.chk_d49dt.isChecked():
                self.Courbe_d49dt.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['d49dt']))
            else:
                self.Courbe_d49dt.clear()
    
            if self.chk_dtotalCO2dt.isChecked():
                self.Courbe_dtotalCO2dt.setData(np.array(self.dfcc['time2']/self.x_axisfactor[self.xscale]), np.array(self.dfcc['dtotalCO2dt']))
            else:
                self.Courbe_dtotalCO2dt.clear()
    


      
    def getvolts2(self):
        """
        get value for each mass and convert it from hex to dec
        """
        self.lastdf = pd.DataFrame(data=np.zeros((0,len(self.dfcolumns))), columns=self.dfcolumns)

        #counter for timestamp
        c=0 
        
        # timestamp start
        self.st = self.previous_packet - self.exp_start
        
        #average time between each packet
        self.ts['packet_time'] = (self.packet_start-self.previous_packet) / self.ts['npackets']
       

        for d in self.newdata[0:-1]: #remove last packet which may be incomplete
            ret=None
            # print(d)
      
            #set timestamp value
            ret=[round(self.st + (float(c) * float(self.ts['packet_time'])), self.precision)]
            c = c + 1
           
            for m in [32, 40, 44, 45, 46, 47, 49]:
                #e = filter(None, d.split("-")) 
                e = [x for x in d.split("-") if x != '']
                
                # index
                i = len(e) - 50 + (self.ch[m]*4)
                
                # decimal
                dec = (int(e[i]) - self.z[m] ) * 256 * 256 * 256 +\
                        int(e[i+1]) * 256 * 256 +\
                        int(e[i+2]) * 256 +\
                        int(e[i+3])
                ret.append(round((float(dec)/4)/587202 - 1, self.precision))

            #add empty event columns
            ret.append('')
            ret.append('')

            #append to dataframe
            try:
                self.lastdf.loc[len(self.lastdf)] = ret

            except AttributeError:
                #create dataframe with only the most recent rawdata
                self.lastdf = pd.DataFrame(data=np.zeros((0,len(dfcolumns))), columns=self.dfcolumns)


        # update statusbar with last value
        self.total_time = int(time.time() - self.exp_start)
        self.total_packets = int(self.total_packets) + self.ts['npackets']

        self.lab_timer.setText(str(self.total_time) + " s")
        if self.exp_type != "test":
            statusmessage = "Acquiring: " + self.dffilename + \
                        "  |  " + str(self.total_time) + " s  |  " +\
                        str(self.total_packets) + " packets |  "
            self.statusbar.showMessage(statusmessage)
        return self.lastdf












    def CO2_calibration(self):
        # look for calibration folder
        bicarb_vol = float(self.calib_volinject)
        bicarb_cc = float(self.calib_bicarb_cc)
        cuvette = int(self.cuvette)

        #open list of past calibrations
#        cals = pd.read_csv(self.calfile)
#        q="(cuvette == " + str(cuvette) + ") & (type='cal44')"
        dfcal = self.df.loc[:, ['time', 'Mass44']]

        # deriv
        dM44dt = dfcal.Mass44.diff().fillna(0) / dfcal.time.diff().fillna(1)
        M44=dfcal.Mass44

        #find injections
        #rescale data from 0 to 1 to find indices
        z = peakutils.prepare.scale(dM44dt, new_range=(0.0, 1.0), eps=1e-09)

        #finds indices of peaks
        indexes = peakutils.indexes(z[0], thres=0.7, min_dist=300)

        #interpolate
        # peaks = peakutils.interpolate(dfcal.time, z[0], ind=indexes)
#        peaks=indexes
        peaks = list(map(int,indexes))

        #add first and last indices
        peaks.insert(0,0)
        peaks.append(max(dfcal.index))

        # print("peaks=",peaks)

        plateaux=[]
        for c in range(len(peaks)-1): # for each injection
            tmp = dM44dt[peaks[c]:peaks[c+1]]

            #i = segment x | I = global x
            i = np.where(tmp == min(tmp))[0]
            I = i + peaks[c]

            plateaux.append(np.mean(M44[I-10:I]))


        jumps = np.diff(plateaux)

        print("plateaux =", plateaux)
        print("jumps=",jumps)

        # How much bic was added in injection
        c = 1000 * (bicarb_cc * bicarb_vol) / cuvette # 1000 * (millimole/Litre * microlitre) /  microlitre = micromole/Litre

        if len(jumps) > 4: #if enough values, we remove highest and lowest values
            jumps = np.setdiff1d(jumps, [min(jumps), max(jumps)])

        #calibration
        # c (micromole/litre) / jumps (volts)
        cal44 = round(np.mean(c/jumps), self.precision) #calibration in micromole/litre/volt

        #prepare new row to insert
        newrow=[str(self.today), str(cuvette), str(self.membraneid), 'cal44', str(cal44)]
        with open(self.calfile, 'a') as f:
            f.write(",".join(newrow) + "\n")

        self.reportmsg="date: <b><font color='red'>" + str(self.today) + "</font></b> <br>" + \
                "cuvette: <b><font color='red'>" + str(self.cuvette) + "</font></b><br>" + \
                "type: <b><font color='red'>cal44</font></b><br>" + \
                "value: <b><font color='red'>" + str(cal44) + "</font></b><br>"+\
            "--------------------------------------------------------------------\n"

        #display message box
        QMessageBox.about(self, "CO2 calibration", self.reportmsg)





    def zeros_calibration(self):
        #open list of past calibrations
#        cals = pd.read_csv(self.calfile)

        dfcal = self.df.loc[:, ['time', 'Mass44', 'Mass45', 'Mass46','Mass47', 'Mass49']]
        zero={}
        for mass in [44,45,46,47,49]:
            zero[str(mass)]=round(dfcal.loc[(max(dfcal.index)-10):, 'Mass' + str(mass)].mean(),self.precision)
#        zero['45']=round(dfcal.loc[(max(dfcal.index)-10):, 'Mass45'].mean(),self.precision)
#        zero['46']=round(dfcal.loc[(max(dfcal.index)-10):, 'Mass46'].mean(),self.precision)
#        zero['47']=round(dfcal.loc[(max(dfcal.index)-10):, 'Mass47'].mean(),self.precision)
#        zero['49']=round(dfcal.loc[(max(dfcal.index)-10):, 'Mass49'].mean(),self.precision)

        #prepare new row to insert
        for key in zero:
            lines=[",".join([str(self.today),str(self.cuvette), str(self.membraneid), 'zero' + key, str(zero[key])])]
            with open(self.calfile, 'a') as f:
                f.write(",".join(lines) + "\n")

        # print(zero)
    #
    # def O2_calibration(self):
    #     membrane = self.membranebox.currentText()
    #     cuvette = self.cuvettebox.currentText()
    #     sheet=self.O2calib.currentText()
    #
    #     calfolder = "C:\\Users\\u5040252\\My Documents\\Projects\\LCIB\\_calibrations\\"
    #     calfile = os.path.join(calfolder, "cal.csv")
    #     zerosfile = os.path.join(calfolder, "zeros.csv")
    #     smoothing_period = 3
    #
    #     self.reportmsg=self.reportmsg + "<br><br><b><u>O2 Calibration:</u></b><br>"
    #
    #     #open list of past calibrations
    #
    #     cals = pd.read_csv(calfile)
    #     if len(cals.query("(cuvette == " + str(cuvette) + ") & (file=='" + self.Myfolders['fichier']+ "') & (membrane=='" + membrane+ "') & (type == 'cal32')")) == 0:
    #
    #         dfcal = self.df.loc[self.df.sheet==sheet, ['ExptTime', 'Cycle', 'Mass32']]
    #
    #         dfcal.loc[:, 'M32s'] = pd.rolling_mean(dfcal.Mass32, smoothing_period)
    #
    #         zero32 = dfcal.M32s.min(skipna=True)
    #         max32 = dfcal.M32s.max(skipna=True)
    #
    #         cal32 = 257/(max32-zero32) # millimole / litre / volt
    #
    #          #prepare new row to insert
    #         #date
    #         d = re.compile('(\d{4})(\d{2})(\d{2})')
    #         caldate = '20' + self.Myfolders['fichier'] if self.Myfolders['fichier'][0:2] != '20' else self.Myfolders['fichier'] #converts from YYmmdd to YYYYmmdd
    #         m = d.match(caldate)
    #         caldate = m.group(3)+ "/"+ m.group(2)+ "/"+ m.group(1)
    #
    #         newcal=[str(caldate), str(self.Myfolders['fichier']), str(sheet), str(cuvette), str(membrane), 'cal32', str(cal32)]
    #         newzero=[str(caldate), str(self.Myfolders['fichier']), str(sheet), str(cuvette), str(membrane), str(zero32),'','','','','']
    #         with open(calfile, 'a') as f:
    #             f.write(",".join(newcal) + "\n")
    #         with open(zerosfile, 'a') as f:
    #             f.write(",".join(newzero) + "\n")
    #
    #         self.reportmsg = self.reportmsg + "<br>Entry added to \""+str(calfile)+"\":  " +"<br>" \
    #             "date: <b><font color='red'>" + str(caldate) + "</font></b> <br>" + \
    #             "file: <b><font color='red'>" + str(self.Myfolders['fichier']) + "</font></b><br>" + \
    #             "sheet: <b><font color='red'>" + str(sheet) + "</font></b><br>" + \
    #             "cuvette: <b><font color='red'>" + str(cuvette) + "</font></b><br>" + \
    #             "membrane: <b><font color='red'>" + str(membrane) + "</font></b><br>" + \
    #             "type: <b><font color='red'>cal32</font></b><br>" + \
    #             "value: <b><font color='red'>" + str(cal32) + "</font></b><br>" +\
    #             "<br>Entry added to \""+str(zerosfile)+"\":  " +"<br>" \
    #             "date: <b><font color='red'>" + str(caldate) + "</font></b> <br>" + \
    #             "file: <b><font color='red'>" + str(self.Myfolders['fichier']) + "</font></b><br>" + \
    #             "sheet: <b><font color='red'>" + str(sheet) + "</font></b><br>" + \
    #             "cuvette: <b><font color='red'>" + str(cuvette) + "</font></b><br>" + \
    #             "membrane: <b><font color='red'>" + str(membrane) + "</font></b><br>" + \
    #             "zero32: <b><font color='red'>"+ str(zero32) +"</font></b><br>" +\
    #             "--------------------------------------------------------------------"
    #
    #     else:
    #          self.reportmsg = self.reportmsg + "<br><b>This O2 calibration is already in datafile.<br>Nothing has been saved</b>"+\
    #             "--------------------------------------------------------------------"
    #     self.report()

    def event_add(self, eventtype):
        
        self.deactivate_events()
        
        self.eventcolors={"CUSTOM":[0,0,0],
                  "BIC":[0,0,0],
                  "CELLS":[0,200,0],
                  "LIGHT ON":[100,100,0],
                  "LIGHT OFF":[100,100,0],
                  "AZ":[200,0,0],
                  "EZ":[0,0,200] }

        self.eventdetails={"CUSTOM":str(self.custom_text.text()),
                  "BIC":"Added " + str(self.bic_vol.text()) + " " + str(self.lab_bicvolunit.text()) + " of " + str(self.bic_cc.text()) + " " + str(self.lab_bicccunit.text()) + " bicarbonate",
                  "CELLS":"Added " + str(self.cells_vol.text()) + " " +  str(self.lab_cellsvolunit.text()) +" of cells at " + str(self.cells_cc.text()) + " " + str(self.lab_cellsccunit.text()) + " chlorophyll (" + str(round(float(self.cells_vol.text()) * float(self.cells_cc.text()) / float(self.cuvette), self.precision)) + " " + str(self.lab_cellsccunit.text()) + " final)",
                  "LIGHT ON":"Light ON (" + str(self.light_int.text()) + " µmol/m2/s)",
                  "LIGHT OFF":"Light OFF",
                  "AZ":"Added " + str(self.az_vol.text()) + " µL of " + str(self.az_cc.text()) + " " + str(self.lab_azccunit.text()) + " AZ (" + str(round(float(self.az_vol.text()) * float(self.az_cc.text()) / float(self.cuvette), self.precision)) + " " + str(self.lab_azccunit.text()) + " final)",
                  "EZ":"Added " + str(self.ez_vol.text()) + " µL of " + str(self.ez_cc.text()) + " " + str(self.lab_ezccunit.text()) + " EZ (" + str(round(float(self.ez_vol.text()) * float(self.ez_cc.text()) / float(self.cuvette), self.precision)) + " " + str(self.lab_ezccunit.text()) + " final)" }


        eventtime = self.df.loc[len(self.df.index)-1, 'time' ]


        #add event
        self.df.loc[len(self.df.index)-1, 'eventtype'] = eventtype
        self.df.loc[len(self.df.index)-1, 'eventdetails'] = self.eventdetails[eventtype]
        self.dfcc.loc[len(self.df.index)-1, 'eventtype'] = eventtype
        self.dfcc.loc[len(self.df.index)-1, 'eventdetails'] = self.eventdetails[eventtype]

        #add line
        self.graph_rawdata.addItem(pg.InfiniteLine(pos=(eventtime+1)/self.x_axisfactor[self.xscale], angle=90, pen=self.eventcolors[eventtype], movable=False, bounds=None))
        self.graph_enrichrate.addItem(pg.InfiniteLine(pos=(eventtime+1)/self.x_axisfactor[self.xscale], angle=90, pen=self.eventcolors[eventtype], movable=False, bounds=None))

        annotation=pg.TextItem(text=self.eventdetails[eventtype], color=self.eventcolors[eventtype],fill=None, anchor=(0,0), angle=-90)
        annotation.setPos((eventtime+1)/self.x_axisfactor[self.xscale],0)
        self.graph_enrichrate.addItem(annotation)

        annotation=pg.TextItem(text=self.eventdetails[eventtype], color=self.eventcolors[eventtype],fill=None, anchor=(0,0), angle=-90)
        annotation.setPos((eventtime+1)/self.x_axisfactor[self.xscale],0)
        self.graph_rawdata.addItem(annotation)



    def deactivate_events(self):
        self.btn_bic.setEnabled(False)
        self.btn_cells.setEnabled(False)
        self.btn_lighton.setEnabled(False)
        self.btn_lightoff.setEnabled(False)
        self.btn_az.setEnabled(False)
        self.btn_ez.setEnabled(False)
        self.btn_custom.setEnabled(False)

    def activate_events(self):
        self.btn_bic.setEnabled(True)
        self.btn_cells.setEnabled(True)
        self.btn_lighton.setEnabled(True)
        self.btn_lightoff.setEnabled(True)
        self.btn_az.setEnabled(True)
        self.btn_ez.setEnabled(True)
        self.btn_custom.setEnabled(True)

    def linearRegSlope(self, i, col):
        tmp = self.regdf.loc[self.regdf.time2.isin(i),]
        return (stats.linregress(tmp.time2,tmp[col])[0] * 60)
        
    def change_user(self):
        self.user = Ui_userDialog.getUser(user = self.user)
        self.actionUser.setText("User: " + str(self.user))
        
    def change_cuvette(self):
        self.cuvette = Ui_cuvetteDialog.getCuvette(cuvette = self.cuvette)
        self.actionCuvette.setText("Cuvette: " + str(self.cuvette))
        
    def change_datafolder(self):
        self.datafolder = QtGui.QFileDialog.getExistingDirectory(self, 'Select folder for data',self.datafolder)
        self.actionDatafolder.setText("Datafolder: " + str(self.datafolder))
        
    def change_smoothing(self):
        self.smoothing = Ui_smoothingDialog.getSmoothing(smoothing = self.smoothing)
        self.actionSmoothing.setText("Smoothing: " + str(self.smoothing))



# -- Classe principale (lancement)  --
def main(args):
        a=QApplication(args) # crée l'objet application
        f=QMainWindow() # crée le QWidget racine
        c=pyMS(f) # appelle la classe contenant le code de l'application
        f.showMaximized() # affiche la fenêtre QWidget
        f.activateWindow()
        r=a.exec_() # lance l'exécution de l'application

        return r

if __name__=="__main__": # pour rendre le code exécutable
        main(sys.argv) # appelle la fonction main