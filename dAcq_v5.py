# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 16:59:00 2015

@author: Vincent Chochois / u5040252



####################################################################################################
INSTRUCTIONS:
####################################################################################################


 1. Select dAcq_v4 in top right corner of this window if not already selected
 2. Hit the play (green triangle) button next to it.

####################################################################################################






"""

# from ui_files.main_ui import *
from ui_files.main2 import *

# dialog windows
from ui_files.userdialog import *
from ui_files.cuvettedialog import *
from ui_files.startdialog import *
from ui_files.calib_dialog import *
from ui_files.membrane_dialog import *
from ui_files.smoothingdialog import *
from ui_files.samples import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *  # inclut QTimer..
import pyqtgraph as pg  # pour accès à certaines constantes pyqtgraph, widget, etc...))

import pandas as pd
import numpy as np
import peakutils
from functools import *
import sys
import serial
import array
import time
import os
import datetime

import yaml


class pyMS(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.datafolder = "C:\\Mass_Spec_Data\\"

        # configuration
        self.cfgfolder = os.path.join(os.environ['USERPROFILE'], 'dAcq')
        self.cfgfile = os.path.join(self.cfgfolder, 'config_dacq.yaml')
        self.cfg_load()

        self.setupUi(parent)  # Obligatoire

        self.user = Ui_userDialog.getUser(user=self.user)
        if self.user == "":
            sys.exit(
                "You have to select a username. Please create an empty folder in " + self.datafolder + " if not in list.")
        else:
            self.actionUser.setText("User: " + self.user)


        self.cuvette = Ui_cuvetteDialog.getCuvette(cuvette=self.cuvette)
        if self.cuvette == "":
            sys.exit("You have to select a cuvette.")
        else:
            self.actionCuvette.setText("Cuvette: " + self.cuvette)

        # initialize variables
        self.cal = {}
        self.last = ""
        self.sampledf = None
        self.exp_type = None
        self.reportmsg = ""
        self.ts = {}
        self.courbe = {}


        self.today = datetime.date.today().strftime('%Y%m%d')
        self.ch = {32: 6, 34: 5, 36: 7, 40: 10, 44: 2, 45: 0, 46: 3, 47: 1, 49: 4}
        self.z = {32: 0, 34: 48, 36: 64, 40: 128, 44: 80, 45: 96, 46: 144, 47: 112, 49: 16}
        self.carbon_masses = [44, 45, 46, 47, 49]
        self.x_axisfactor = {"sec": 1, "min": 60}

        self.courbes_rawdata = ['Mass32', 'Mass40', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49', 'logE49',
                                'totalCO2', 'AF']
        self.courbes_ratedata = ['d32dt', 'd40dt', 'd44dt', 'd45dt', 'd46dt', 'd47dt', 'd49dt', 'enrichrate47',
                                 'enrichrate49', 'dtotalCO2dt','rel_d45dt','rel_d49dt','dAFdt']


        # deactivate events
        self.event_deactivate()

        self.actionAdd_O2_Calibration.setEnabled(False)
        self.actionAdd_Consumptions.setEnabled(True)

        # connect actions
        self.actionStart.triggered.connect(self.start)
        self.actionTestmode.triggered.connect(self.testmode)
        self.actionStop.triggered.connect(self.stop)

        self.actionAdd_new_Membrane.triggered.connect(self.set_membrane)
        self.actionAdd_CO2_Calibration.triggered.connect(self.set_co2calibration)
        self.actionAdd_Electrical_Zeros.triggered.connect(self.set_zeros)
        self.actionAdd_Consumptions.triggered.connect(self.set_consumption)

        self.actionUser.triggered.connect(self.change_user)
        self.actionCuvette.triggered.connect(self.change_cuvette)
        self.actionDatafolder.triggered.connect(self.change_datafolder)
        self.actionSmoothing.triggered.connect(self.change_smoothing)

        self.actionSamples.triggered.connect(self.samples_manager)

        self.btn_bic.clicked.connect(partial(self.event_add, "BIC"))
        self.btn_cells.clicked.connect(partial(self.event_add, "CELLS"))
        self.btn_lighton.clicked.connect(partial(self.event_add, "LIGHT ON"))
        self.btn_lightoff.clicked.connect(partial(self.event_add, "LIGHT OFF"))
        self.btn_az.clicked.connect(partial(self.event_add, "AZ"))
        self.btn_ez.clicked.connect(partial(self.event_add, "EZ"))
        self.btn_custom.clicked.connect(partial(self.event_add, "CUSTOM"))

        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Insert), self.btn_bic, partial(self.event_add, "BIC"))
        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_PageDown), self.btn_cells, partial(self.event_add, "CELLS"))
        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_PageUp), self.btn_custom, partial(self.event_add, "CUSTOM"))

        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Left), self.btn_lighton, partial(self.event_add, "LIGHT ON"))
        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Right), self.btn_lightoff, partial(self.event_add, "LIGHT OFF"))

        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_End), self.btn_az, partial(self.event_add, "AZ"))
        QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Home), self.btn_ez, partial(self.event_add, "EZ"))

        self.__init__graphs()

        # open serial port
        self.ser = serial.Serial(self.portCOM)

    def __init__graphs(self):
        # general graph config
        pg.setConfigOptions(antialias=True)
        self.labelStyle = {'color': '#000', 'font-size': '14pt'}  # propriétés CSS à utiliser pour le label
        self.gridColors = (100, 100, 100)

        # RAWDATA GRAPH
        self.graph_rawdata.setBackgroundBrush(
            QBrush(QColor(Qt.white)))  # la classe PlotWidget est un GraphicsWidget qui est un QGraphics View
        self.graph_rawdata.showGrid(x=True, y=True)  # affiche la grille
        self.graph_rawdata.getAxis('bottom').setPen(pg.mkPen(*self.gridColors))  # couleur de l'axe + grille
        self.graph_rawdata.getAxis('left').setPen(pg.mkPen(*self.gridColors))  # couleur de l'axe + grille

        self.graph_rawdata.getAxis('bottom').setLabel('Time', units=self.xscale, **self.labelStyle)  # label de l'axe
        self.graph_rawdata.getAxis('left').setLabel('Concentration', units='micromole/L',
                                                    **self.labelStyle)  # label de l'axe

        # self.graph_rawdata.getViewBox().setMouseMode(pg.ViewBox.RectMode) # fonction ViewBox pas accessible depuis PlotWidget : fixe selection par zone
        self.graph_rawdata.setMouseEnabled(x=True, y=True)

        # ENRICHRATE GRAPH
        self.graph_enrichrate.setBackgroundBrush(
            QBrush(QColor(Qt.white)))  # la classe PlotWidget est un GraphicsWidget qui est un QGraphics View
        self.graph_enrichrate.showGrid(x=True, y=True)  # affiche la grille
        self.graph_enrichrate.getAxis('bottom').setPen(pg.mkPen(*self.gridColors))  # couleur de l'axe + grille
        self.graph_enrichrate.getAxis('left').setPen(pg.mkPen(*self.gridColors))  # couleur de l'axe + grille

        self.graph_enrichrate.getAxis('bottom').setLabel('Time', units=self.xscale, **self.labelStyle)  # label de l'axe
        self.graph_enrichrate.getAxis('left').setLabel('Rate', units=self.yscale, **self.labelStyle)  # label de l'axe

        # self.graph_enrichrate.getViewBox().setMouseMode(pg.ViewBox.RectMode)  # fonction ViewBox pas accessible depuis PlotWidget : fixe selection par zone
        self.graph_enrichrate.setMouseEnabled(x=True, y=True)

        # Create empty curves
        for m in self.courbes_rawdata:
            if m == "logE49":
                self.courbe[m] = self.graph_rawdata.plot(
                    pen=pg.mkPen(self.courbeColors[m], width=self.graphs_linewidth, style=QtCore.Qt.DashLine),
                    name=m)

                # alternative
                # self.courbe[m] = pg.PlotCurveItem(
                #     pen=pg.mkPen(self.courbeColors[m], width=self.graphs_linewidth, style=QtCore.Qt.DashLine),
                #     name=m)


            else:
                self.courbe[m] = self.graph_rawdata.plot(
                    pen=pg.mkPen(self.courbeColors[m], width=self.graphs_linewidth),
                    name=m)
                # alternative
                # self.courbe[m] = pg.PlotCurveItem(
                #     pen=pg.mkPen(self.courbeColors[m], width=self.graphs_linewidth, style=QtCore.Qt.DashLine),
                #     name=m)

        for m in self.courbes_ratedata:
            if m in ["enrichrate47", "enrichrate49"]:
                self.courbe[m] = self.graph_enrichrate.plot(
                    pen=pg.mkPen(self.courbeColors[m], width=self.graphs_linewidth, style=QtCore.Qt.DashLine),
                    name=m)
            elif m in ["rel_d49dt", "rel_d45dt"]:
                self.courbe[m] = self.graph_enrichrate.plot(
                    pen=pg.mkPen(self.courbeColors[m], width=self.graphs_linewidth, style=QtCore.Qt.DotLine),
                    name=m)

            else:
                self.courbe[m] = self.graph_enrichrate.plot(
                    pen=pg.mkPen(self.courbeColors[m], width=self.graphs_linewidth), name=m)

    def cfg_generate(self):
        # check if config folder and config file exist
        if not os.path.isfile(self.cfgfile):
            if not os.path.isdir(self.cfgfolder):
                os.makedirs(os.path.join(self.cfgfolder))

        # generate default values
        config = dict(
            smoothing=60,
            precision=8,
            portCOM='COM1',
            xscale="sec",
            yscale="s-1",
            datafolder="C:\\Mass_Spec_Data\\",
            user="Vincent",
            cuvette="600",
            cuvetteList=["600", "2000", "4000"],
            courbeColors={"Mass32": (250, 0, 0, 255),
                          "Mass40": (200, 150, 0, 255),
                          "Mass44": (0, 250, 0, 255),
                          "Mass45": (50, 200, 250, 255),
                          "Mass46": (250, 150, 250, 255),
                          "Mass47": (0, 100, 250, 255),
                          "Mass49": (100, 0, 250, 255),
                          "totalCO2": (0, 0, 0, 255),
                          "logE49": (100, 100, 100, 255),
                          "d32dt": (250, 0, 0, 255),
                          "d40dt": (200, 150, 0, 255),
                          "d44dt": (0, 250, 0, 255),
                          "d45dt": (50, 200, 250, 255),
                          "d46dt": (250, 150, 250, 255),
                          "d47dt": (0, 100, 250, 255),
                          "d49dt": (100, 0, 250, 255),
                          "dtotalCO2dt": (0, 0, 0, 255),
                          "logE47": (100, 100, 100, 255),
                          "enrichrate47": (0, 100, 250, 255),
                          "enrichrate49": (100, 0, 250, 255),
                          "rel_d45dt": (50, 200, 250, 255),
                          "rel_d49dt": (100, 0, 250, 255),
                          "AF": (227,48,215,255),
                          "dAFdt": (227,48,215,255)
                          },
            buffer_time=1,
            save_interval=5,
            graph_interval=1,
            ui_interval=1,
            graphs_linewidth=1.25)

        # save config in cfgfile
        with open(self.cfgfile, 'w') as outfile:
            outfile.write(yaml.dump(config))

    def cfg_load(self):
        if not os.path.isfile(self.cfgfile):
            self.cfg_generate()

        else:
            with open(self.cfgfile, 'r') as f:
                try:
                    cfg = yaml.load(f)

                    self.smoothing = cfg['smoothing']
                    self.precision = cfg['precision']
                    self.xscale = cfg['xscale']
                    self.yscale = cfg['yscale']
                    self.portCOM = str(cfg['portCOM'])
                    self.datafolder = cfg['datafolder']
                    self.user = cfg['user']
                    self.cuvette = cfg['cuvette']
                    self.cuvetteList = cfg['cuvetteList']
                    self.buffer_time = cfg['buffer_time']
                    self.graphs_linewidth = cfg['graphs_linewidth']
                    self.courbeColors = cfg['courbeColors']
                    self.save_interval = cfg['save_interval']
                    self.graph_interval = cfg['graph_interval']
                    self.ui_interval = cfg['ui_interval']

                except yaml.YAMLError as exc:
                    print(exc)

    def start(self):
        print("start... ", self.exp_type)

        # display units
        self.lab_M32unit.setText(" µM")
        self.lab_ER47unit.setText(" " + self.yscale)
        self.lab_ER49unit.setText(" " + self.yscale)

        for lab in [self.lab_M32unit, self.lab_M44unit, self.lab_M45unit,
                    self.lab_M46unit, self.lab_M47unit, self.lab_M49unit,
                    self.lab_M40unit, self.lab_totCO2unit]:
            lab.setText(" µM")

        for lab in [self.lab_d32dtunit, self.lab_d44dtunit, self.lab_d45dtunit,
                    self.lab_d46dtunit, self.lab_d47dtunit, self.lab_d49dtunit,
                    self.lab_d40dtunit, self.lab_dtotalCO2dtunit]:
            lab.setText(" µM." + self.yscale)


        # get infos from startDialog
        self.samplename = Ui_StartDialog.getStartData(user=self.user, datafolder=self.datafolder)
        if self.samplename != '':
            self.today = datetime.date.today().strftime('%Y%m%d')

            # clear graphs
            self.graph_rawdata.clear()
            self.graph_enrichrate.clear()
            self.__init__graphs()

            # disable menus
            self.actionAdd_CO2_Calibration.setEnabled(False)
            self.actionStart.setEnabled(False)
            self.actionAdd_O2_Calibration.setEnabled(False)
            self.actionAdd_Consumptions.setEnabled(False)
            self.actionAdd_Electrical_Zeros.setEnabled(False)

            # activate events
            self.event_activate()

            # build filenames
            self.dffilename = os.path.join(self.datafolder, self.user, self.today, "rawdata",
                                           self.today + "_" + str(self.samplename) + ".csv")
            self.dfccfilename = os.path.join(self.datafolder, self.user, self.today,
                                             self.today + "_" + str(self.samplename) + ".csv")
            self.membranefile = os.path.join(str(self.datafolder), "_calibrations", "membranes.csv")
            self.calfile = os.path.join(str(self.datafolder), "_calibrations", "cal.csv")
            self.targetfolder = os.path.join(self.datafolder, self.user, self.today)

            # check if file exists
            self.check_file_exists()

            # get membrane
            membranedf = pd.read_csv(self.membranefile)
            q = "cuvette==" + str(self.cuvette)
            self.membraneid = int(membranedf.query(q).sort('date', ascending=False).reset_index().head(1)['id'][0])
            membranedf = None

            # calibration (includes membraneid)
            if self.exp_type != "CO2calib" and self.exp_type != "O2calib" and self.exp_type != "zeros":
                self.get_calibration()
                print(self.cal)

            # samplefile
            self.create_samplefile()

            # initialize timer
            self.exp_start = time.time()
            self.packet_start = time.time()
            self.total_time = 0
            self.total_packets = 0

            # initialise variables
            self.dfcolumns = ['time', 'Mass32', 'Mass40', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49', 'eventtype',
                              'eventdetails']
            self.dfcccolumns = ['time', 'Mass32', 'Mass40', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49',
                                'eventtype', 'eventdetails', 'totalCO2', 'logE47', 'logE49', 'd32dt', 'd32dt_d',
                                'd32dt_cd', 'enrichrate47',
                                'enrichrate49', 'd40dt', 'd44dt', 'd45dt', 'd46dt', 'd47dt', 'd49dt', 'dtotalCO2dt',
                                'd40dt_d', 'AF', 'dAFdt', 'rel_d49dt', 'rel_d45dt']
            self.df = pd.DataFrame(columns=self.dfcolumns)
            self.dfcc = pd.DataFrame( columns=self.dfcccolumns)

            # flush buffer
            self.ser.flushInput()

            # start timer
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.myupdate)
            self.timer.start(self.buffer_time * 1000)

            # csv saving timer // saves CSV only every save_interval seconds
            self.save_csv()
            self.timer2 = QtCore.QTimer(self)
            self.timer2.timeout.connect(self.save_csv)
            self.timer2.start(self.save_interval * 1000)

            # graph updating thread
#            self.timer3 = QtCore.QTimer(self)
#            self.timer3.timeout.connect(self.update_data)
#            self.timer3.start(self.graph_interval * 1000)
#
#            # UI updating thread
#            self.timer4 = QtCore.QTimer(self)
#            self.timer4.timeout.connect(self.update_ui)
#            self.timer4.start(self.ui_interval * 1000)

        else:
            print("dialog rejected, cancelling acquisition...")
            self.stop()

    def stop(self):
        print("STOP")
        self.timer.stop()

        if self.exp_type != "test":
            self.timer2.stop()


        # enable menus
        self.actionAdd_CO2_Calibration.setEnabled(True)
        self.actionStart.setEnabled(True)
        self.actionTestmode.setEnabled(True)

        self.actionAdd_O2_Calibration.setEnabled(False)
        self.actionAdd_Consumptions.setEnabled(True)
        self.actionAdd_Electrical_Zeros.setEnabled(True)

        # deactivate events
        self.event_deactivate()

        # if this is a calibration, then do some calculations
        if self.exp_type == "CO2calib":
            self.cal_co2()

        elif self.exp_type == "O2calib":
            self.calculate_O2calib()

        elif self.exp_type == "zeros":
            self.cal_zeros()

        elif self.exp_type == "consumption":
            self.cal_consumption()

        else:  # normal experiment
            pass

        # reset important variables
        self.exp_type = None
        self.exp_start = None
        self.df = None
        self.dfcc = None
        self.cal = None

    def myupdate(self):
        # check if events are activated:
        if not self.btn_bic.isEnabled():
            self.event_activate()

        self.previous_packet = self.packet_start
        self.packet_start = time.time()
        u = array.array("B", self.ser.read(self.ser.inWaiting()))

        # split packets
        self.newdata = "-".join(map(str, u)).split("255-255-255-255")

        # how many packets in the buffeR ?
        self.ts['npackets'] = len(self.newdata) - 1

        if self.total_packets > 0:
            # stick first packet with last packet of previous buffer
            self.newdata[0] = self.last + "-" + self.newdata[0]
            self.last = self.newdata[-1]
        else:
            # remove first packet
            self.newdata = self.newdata[1:len(self.newdata)]

        # packets
        if self.ts['npackets'] > 0:
            self.getvolts2()
            self.df = self.df.append(pd.DataFrame(data=self.lastnd[1:], columns=self.dfcolumns), ignore_index=True)
            self.dfcc = self.dfcc.append(pd.DataFrame(data=self.lastnd[1:], columns=self.dfcolumns), ignore_index=True)

        # calculate concentrations and derivatives
        self.update_data()

        # update graphs
        self.update_graph()

        # update UI
        self.update_ui()

    def getvolts2(self):
        """
        get value for each mass and convert it from hex to dec
        """
        self.lastnd = np.zeros(shape=(1,len(self.dfcolumns)), dtype=float)

        # timestamp start
        st = self.previous_packet - self.exp_start

        # average time between each packet
        self.ts['packet_time'] = (self.packet_start - self.previous_packet) / self.ts['npackets']

        for c, d in enumerate(self.newdata[:-1]):  # remove last packet which may be incomplete
            ret = None

            # set timestamp value
            ret = [round(st + (c * self.ts['packet_time']), 2)]

            # remove empty elements
            e = list(filter(None, d.split("-")))

            for m in [32, 40, 44, 45, 46, 47, 49]:
                # index
                i = len(e) - 50 + (self.ch[m] * 4)

                # decimal
                decimal = (int(e[i]) - self.z[m]) * 256 * 256 * 256 + \
                      int(e[i + 1]) * 256 * 256 + \
                      int(e[i + 2]) * 256 + \
                      int(e[i + 3])
                ret.append((float(decimal) / 4) / 587202 - 1)

            # add empty event columns
            ret = self.myround(ret)
            ret = np.append(ret, np.empty(shape=(1, 2)))

            # append to array
            self.lastnd = np.append(self.lastnd, self.myround([ret]), axis=0)

#            self.lastnd.astype(float)

        # cleanup variables
        del ret, decimal, c, d, e, i

        # update statusbar with last value
        self.total_time = int(time.time() - self.exp_start)
        self.total_packets = int(self.total_packets) + self.ts['npackets']

        self.lab_timer.setText(str(self.total_time) + " s")
        if self.exp_type != "test":
            statusmessage = "Acquiring: " + self.dffilename + \
                            "  |  " + str(self.total_time) + " s  |  " + \
                            str(self.total_packets) + " packets |  "
            self.statusbar.showMessage(statusmessage)

    def check_file_exists(self):
        while os.path.exists(self.dffilename):

            sugsamplename = self.samplename

            # create suggested sample name
            while os.path.exists(self.dffilename):
                if "_" in sugsamplename:
                    try:  # if there's already a number, try to increment it
                        incstr = sugsamplename.split("_")[-1]
                        inc = int(incstr)
                        inc += 1
                        sugsamplename = sugsamplename.rstrip("_" + incstr) + "_" + str(inc)


                    except ValueError:  # else just add a number
                        sugsamplename += "_2"
                else:
                    sugsamplename += "_2"

                self.dffilename = os.path.join(self.datafolder, self.user, self.today, "rawdata",
                                               self.today + "_" + str(sugsamplename) + ".csv")

            # open a dialog to ask for a new sample name
            newsample, ok = QtGui.QInputDialog.getText(self, "Sample already exists",
                                                       "Suggested new sample name for '<b>" + self.samplename + "</b>' :",
                                                       QtGui.QLineEdit.Normal,
                                                       sugsamplename)

            # new name not empty and "OK" button clicked :
            if ok and newsample != '':
                self.samplename = str(newsample)
                self.dffilename = os.path.join(self.datafolder, self.user, self.today, "rawdata",
                                               self.today + "_" + self.samplename + ".csv")
                self.dfccfilename = os.path.join(self.datafolder, self.user, self.today,
                                                 self.today + "_" + self.samplename + ".csv")

    def create_samplefile(self):
        # Create or append to samples file
        self.samplefile = os.path.join(self.targetfolder, self.today + "_SAMPLES.csv")

        self.sampleline = [self.today, str(time.strftime('%H:%M:%S')),
                           self.user, self.samplename, self.today + "_" + self.samplename + ".csv",
                           str(self.cuvette),
                           str(self.membraneid),
                           str(self.smoothing),
                           str(self.cal['cal44']),
                           str(self.cal['cal32']),
                           str(self.cal['cons40']),
                           str(self.cal['cons32']),
                           str(self.cal['zero44']),
                           str(self.cal['zero45']),
                           str(self.cal['zero46']),
                           str(self.cal['zero47']),
                           str(self.cal['zero49']),
                           str(self.cal['zero32'])]

        # append to dataframe
        try:
            print(self.sampleline)
            self.sampledf = pd.read_csv(self.samplefile)
            self.sampledf.loc[len(self.sampledf.index)] = self.sampleline

        except OSError:
            columns = ['date', 'time', 'user',
                       'samplename', 'filename',
                       'cuvette', 'membraneid',
                       'smoothing',
                       'cal44', 'cal32',
                       'cons40', 'cons32',
                       'zero44', 'zero45', 'zero46', 'zero47', 'zero49',
                       'zero32']
            self.sampledf = pd.DataFrame(data=np.zeros((0, len(columns))), columns=columns)
            self.sampledf.loc[len(self.sampledf.index)] = self.sampleline

        # save to file
        self.sampledf.to_csv(self.samplefile, index=False, encoding='ISO-8859-1')

    def set_membrane(self):
        Ui_Membrane_Dialog.add_membrane()
        pass

    def set_co2calibration(self):
        self.exp_type = "CO2calib"
        self.calib_bicarb_cc, self.calib_volinject = Ui_Calib_Dialog.calib_infos()

        self.cal = {}
        for what in ['cal32', 'cal44', 'zero32', 'zero40', 'zero44', 'zero45', 'zero46', 'zero47', 'zero49', 'cons32',
                     'cons40']:
            self.cal[what] = 0

        # find membrane id
        membranefile = "C:\\Mass_Spec_Data\\_calibrations\\membranes.csv"
        membranedf = pd.read_csv(membranefile, index_col='id')
        query = "cuvette == " + self.cuvette
        membraneid = membranedf.query(query).sort('date', ascending=False).head(1).index[0]
        print('membraneid = ', membraneid)

        # activate 44 only
        for m in self.courbes_rawdata:
            self.chk[m].setChecked(False)

        for m in self.courbes_ratedata:
            self.chk[m].setChecked(False)

        for m in ["Mass44", "d44dt"]:
            self.chk[m].setChecked(True)

        # display units
        self.lab_ER47unit.setText(" " + self.yscale)
        self.lab_ER49unit.setText(" " + self.yscale)

        for lab in [self.lab_M32unit, self.lab_M40unit, self.lab_M44unit,
                    self.lab_M45unit, self.lab_M46unit, self.lab_M47unit,
                    self.lab_M49unit, self.lab_totCO2unit]:
            lab.setText(" V")

        for lab in [self.lab_d32dtunit, self.lab_d40dtunit, self.lab_d44dtunit,
                    self.lab_d45dtunit, self.lab_d46dtunit, self.lab_d47dtunit,
                    self.lab_d49dtunit, self.lab_dtotalCO2dtunit]:
            lab.setText(" V" + self.yscale)

        self.start()
        pass

    def set_zeros(self):
        self.exp_type = "zeros"

        self.cal = {}
        for what in ['cal32', 'cal44',
        'zero32', 'zero40', 'zero44', 'zero45', 'zero46', 'zero47', 'zero49',
        'cons32','cons40']:
            self.cal[what] = 0

        # activate all masses
        for m in self.courbes_rawdata:
            self.chk[m].setChecked(True)

        for m in self.courbes_ratedata:
            self.chk[m].setChecked(True)

        for m in ["Mass32", "Mass40", "logE49", "d32dt", "d40dt", "enrichrate49", "enrichrate47"]:
            self.chk[m].setChecked(False)

        # display units
        self.lab_ER47unit.setText(" " + self.yscale)
        self.lab_ER49unit.setText(" " + self.yscale)

        for lab in [self.lab_M32unit, self.lab_M40unit, self.lab_M44unit,
                    self.lab_M45unit, self.lab_M46unit, self.lab_M47unit,
                    self.lab_M49unit, self.lab_totCO2unit]:
            lab.setText(" V")

        for lab in [self.lab_d32dtunit, self.lab_d40dtunit, self.lab_d44dtunit,
                    self.lab_d45dtunit, self.lab_d46dtunit, self.lab_d47dtunit,
                    self.lab_d49dtunit, self.lab_dtotalCO2dtunit]:
            lab.setText(" V" + self.yscale)

        self.start()

        pass

    def set_o2calibration(self):
        self.exp_type = "O2calib"

        self.cal = {}
        for what in ['cal32', 'cal44', 'zero32', 'zero40', 'zero44', 'zero45', 'zero46', 'zero47', 'zero49', 'cons32',
                     'cons40']:
            self.cal[what] = 0

        # activate 44 only
        for m in self.courbes_rawdata:
            self.chk[m].setChecked(False)

        for m in self.courbes_ratedata:
            self.chk[m].setChecked(False)

        for m in ["Mass32", "d32dt"]:
            self.chk[m].setChecked(False)

        # self.start()

        pass

    def set_consumption(self):
        self.exp_type = "consumption"

        # display units
        self.lab_ER47unit.setText(" " + self.yscale)
        self.lab_ER49unit.setText(" " + self.yscale)

        for lab in [self.lab_M32unit, self.lab_M40unit, self.lab_M44unit,
                    self.lab_M45unit, self.lab_M46unit, self.lab_M47unit,
                    self.lab_M49unit, self.lab_totCO2unit]:
            lab.setText(" V")

        for lab in [self.lab_d32dtunit, self.lab_d40dtunit, self.lab_d44dtunit,
                    self.lab_d45dtunit, self.lab_d46dtunit, self.lab_d47dtunit,
                    self.lab_d49dtunit, self.lab_dtotalCO2dtunit]:
            lab.setText(" V" + self.yscale)


        self.start()

    def get_calibration(self):
        # load calibration file path
        caldf = pd.read_csv(self.calfile)

        self.cal = {'membraneid': self.membraneid,
                    'calfile': self.calfile}

        for what in ['cal32', 'cal44', 'zero32', 'zero40', 'zero44', 'zero45', 'zero46', 'zero47', 'zero49', 'cons32',
                     'cons40']:
            q = "cuvette=={} & type=='{}'".format(str(self.cuvette), what)
            self.cal[what] = float(caldf.query(q).sort('date', ascending=False).head(1)['value'])

    def save_csv(self):
        if self.exp_type != 'test':
            self.df.to_csv(self.dffilename, index=False, encoding='ISO-8859-1')

            if self.exp_type == None:
                self.dfcc.to_csv(self.dfccfilename, index=False, encoding='ISO-8859-1')

    def denoising(self, df, m):
        m40 = np.array(df['Mass40'])
        d40 = np.array(df['d40dt'])
        mx = np.array(df['Mass' + str(m)])
        dx = np.array(df['d' + str(m) + 'dt'])

        df['dfit40dt'] = m40 * self.cal['cons40']
        df['d' + str(m) + 'dt_d'] = dx - ((mx / m40) * (d40 - (m40 * self.cal['cons40'])))
        return df

    def update_data(self):
        # calculate concentrations
        for mass in [44, 45, 46, 47, 49, 32]:
            c = 'Mass' + str(mass)
            if self.exp_type == None or self.exp_type == 'consumption':
                calcol = 'cal32' if mass == 32 else 'cal44'
#                print(np.array(self.df[c]), self.cal['zero' + str(mass)], self.cal[calcol] )
                self.dfcc[c] = (np.array(self.df[c]) - self.cal['zero' + str(mass)]) * self.cal[calcol]
            else:
                self.dfcc[c] = self.df[c]

        self.dfcc['totalCO2'] = (self.dfcc.Mass44 + self.dfcc.Mass45 + self.dfcc.Mass46 + self.dfcc.Mass47 + self.dfcc.Mass49)

        # homogenous time
        self.dfcc['avgdt'] = self.myround(self.dfcc.time.diff().mean())
        self.dfcc['time2'] = self.myround(self.dfcc.avgdt.cumsum())

        # rates
        if self.total_packets > int(self.smoothing) + 1:
            self.smoothing_window = int(self.smoothing) + np.shape(self.lastnd)[0]
            self.regdf = self.dfcc.tail(self.smoothing_window).copy()


            t = np.array(self.regdf.time)
            m32, m40 = np.array(self.regdf.Mass32), np.array(self.regdf.Mass40)
            m44, m46 = np.array(self.regdf.Mass44),np.array(self.regdf.Mass46)
            m45, m47, m49 = np.array(self.regdf.Mass45), np.array(self.regdf.Mass47), np.array(self.regdf.Mass49)

            # avoid errors due to log
            if (m47 > 0).all() and ( (m45 + m47 +m49) > 0).all():
                self.regdf['logE47'] = np.log10(100 * m47 / (m45 + m47 + m49))
                self.regdf['enrichrate47'] = self.rolling_linear_reg(t, np.array(self.regdf['logE47']))
            else:
                self.regdf['logE47'], self.regdf['enrichrate47'] = 0, 0

            if (m49 > 0).all() and ((m45 + m47 + m49) > 0).all():
                self.regdf['logE49'] = np.log10(100 * m49 / (m45 + m47 + m49))
                self.regdf['AF'] = np.log10(100*(2 *m49 + m47)/(2*(m45 + m47 + m49)))

                self.regdf['enrichrate49'] = self.rolling_linear_reg(t, np.array(self.regdf['logE49']))
                self.regdf['dAFdt'] = self.rolling_linear_reg(t, np.array(self.regdf['AF']))
            else:
                self.regdf['logE49'], self.regdf['enrichrate49'] = 0, 0
                self.regdf['AF'], self.regdf['dAFdt'] = 0, 0


            self.regdf['d32dt'] = self.rolling_linear_reg(t, m32)
            self.regdf['d40dt'] = self.rolling_linear_reg(t, m40)
            self.regdf['d44dt'] = self.rolling_linear_reg(t, m44)
            self.regdf['d45dt'] = self.rolling_linear_reg(t, m45)
            self.regdf['d46dt'] = self.rolling_linear_reg(t, m46)
            self.regdf['d47dt'] = self.rolling_linear_reg(t, m47)
            self.regdf['d49dt'] = self.rolling_linear_reg(t, m49)

            self.regdf['dtotalCO2dt'] = self.regdf['d44dt'] + self.regdf['d45dt'] + self.regdf['d46dt'] + self.regdf['d47dt'] + self.regdf['d49dt']


            if self.exp_type == None:
                # denoising
                for m in [32, 40]:
                    self.regdf = self.denoising(self.regdf, m)

                # M32 consumption
                self.regdf['d32dt_c'] = self.cal['cons32'] * m32
                self.regdf['d32dt_cd'] = self.regdf['d32dt_d'] - self.regdf['d32dt_c']

                #calcul relative derivatives
                self.regdf['rel_d49dt'] = self.myround(np.array(self.regdf['d49dt']) / m49)
                self.regdf['rel_d45dt'] = self.myround(np.array(self.regdf['d45dt']) / m45)

            else:
                self.regdf['d32dt_d'] = self.regdf['d32dt']
                self.regdf['d32dt_cd'] = self.regdf['d32dt_d']
                self.regdf['d40dt_d'] = self.regdf['d40dt']


            self.dfcc.ix[self.dfcc.time.isin(self.regdf.loc[self.regdf.d32dt.notnull(), 'time'].values),
                  ['Mass32', 'Mass40','Mass44', 'Mass45',
                   'Mass46', 'Mass47','Mass49','totalCO2',
                   'logE47','logE49', 'd32dt', 'enrichrate47',
                   'enrichrate49','d40dt', 'd44dt', 'd45dt', 'd46dt',
                   'd47dt', 'd49dt','dtotalCO2dt', 'd32dt_cd', 'd32dt_d','d40dt_d',
                   'AF','dAFdt','rel_d49dt','rel_d45dt']] = \
                self.regdf.ix[self.regdf.d32dt.notnull(),
                  ['Mass32', 'Mass40', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49',
                   'totalCO2', 'logE47', 'logE49', 'd32dt', 'enrichrate47',
                   'enrichrate49', 'd40dt', 'd44dt', 'd45dt', 'd46dt', 'd47dt', 'd49dt',
                   'dtotalCO2dt', 'd32dt_cd', 'd32dt_d', 'd40dt_d',
                   'AF','dAFdt','rel_d49dt','rel_d45dt']]


        else:
            self.dfcc['d32dt'] = 0
            self.dfcc['enrichrate47'] = 0
            self.dfcc['enrichrate49'] = 0
            self.dfcc['d40dt'] = 0
            self.dfcc['d44dt'] = 0
            self.dfcc['d45dt'] = 0
            self.dfcc['d46dt'] = 0
            self.dfcc['d47dt'] = 0
            self.dfcc['d49dt'] = 0
            self.dfcc['dtotalCO2dt'] = 0
            self.dfcc['rel_d45dt'] = 0
            self.dfcc['rel_d49dt'] = 0
            self.dfcc['AF'] = 0
            self.dfcc['dAFdt'] = 0

    def update_ui(self):

        """
        Updates user interface
        """
        self.lab_32.setText(str(np.array(self.dfcc['Mass32'])[-1]))
        self.lab_40.setText(str(np.array(self.dfcc['Mass40'])[-1]))
        self.lab_44.setText(str(np.array(self.dfcc['Mass44'])[-1]))
        self.lab_45.setText(str(np.array(self.dfcc['Mass45'])[-1]))
        self.lab_46.setText(str(np.array(self.dfcc['Mass46'])[-1]))
        self.lab_47.setText(str(np.array(self.dfcc['Mass47'])[-1]))
        self.lab_49.setText(str(np.array(self.dfcc['Mass49'])[-1]))
        self.lab_totalCO2.setText(str(np.array(self.dfcc['totalCO2'])[-1]))

        if self.total_packets > int(self.smoothing) + 1:
            idx = self.dfcc.loc[self.dfcc.d32dt.notnull(), 'd32dt'].index[-1]
            self.lab_d32dt.setText(str(self.dfcc.at[idx, 'd32dt']))
            self.lab_d40dt.setText(str(np.array(self.dfcc.at[idx, 'd40dt'])))
            self.lab_d44dt.setText(str(np.array(self.dfcc.at[idx, 'd44dt'])))
            self.lab_d45dt.setText(str(np.array(self.dfcc.at[idx, 'd45dt'])))
            self.lab_d46dt.setText(str(np.array(self.dfcc.at[idx, 'd46dt'])))
            self.lab_d47dt.setText(str(np.array(self.dfcc.at[idx, 'd47dt'])))
            self.lab_d49dt.setText(str(np.array(self.dfcc.at[idx, 'd49dt'])))
            self.lab_d49dt.setText(str(np.array(self.dfcc.at[idx, 'd49dt'])))
            self.lab_d49dt.setText(str(np.array(self.dfcc.at[idx, 'd49dt'])))
            self.lab_d49dt.setText(str(np.array(self.dfcc.at[idx, 'd49dt'])))
            self.lab_dtotalCO2dt.setText(str(np.array(self.dfcc.at[idx, 'dtotalCO2dt'])))
            self.lab_rel_d45dt.setText(str(np.array(self.dfcc.at[idx, 'rel_d45dt'])))
            self.lab_rel_d49dt.setText(str(np.array(self.dfcc.at[idx, 'rel_d49dt'])))
            self.lab_atomic_fraction.setText(str(np.array(self.dfcc.at[idx, 'AF'])))
            self.lab_datomic_fractiondt.setText(str(np.array(self.dfcc.at[idx, 'dAFdt'])))
            self.lab_ER47.setText(str(np.array(self.dfcc.at[idx, 'enrichrate47'])))
            self.lab_ER49.setText(str(np.array(self.dfcc.at[idx, 'enrichrate49'])))

    def update_graph(self):
        """
        Updates graphs
        """
        tscaled = np.array(self.dfcc['time2']) / self.x_axisfactor[self.xscale]
        for m in self.courbes_rawdata:
            if self.chk[m].isChecked():
                self.courbe[m].setData(tscaled, np.array(self.dfcc[m]))
            else:
                self.courbe[m].clear()

        if self.total_packets > int(self.smoothing) + 1:
            for m in self.courbes_ratedata:
                if self.chk[m].isChecked():
                    self.courbe[m].setData(tscaled, np.array(self.dfcc[m]))
                else:
                    self.courbe[m].clear()

    def myround(self, value):
        return np.round(value, self.precision)

    def cal_consumption(self):
        """
        Determines consumption parameters for oxygen (f32) and for Argon (f40)

        :return:
        f40: expressed in volts/second/volt of Mass40 signal
        f32: expressed in µM/second/µM of Mass32
        """
        df = self.dfcc.loc[:, ['time2', 'Mass32', 'Mass40', 'd32dt', 'd40dt']]

        # calculate slope d32dt = f(Mass32) and d40dt = f(Mass40)
        x32, y32 = np.array(df.loc[df.d32dt.notnull(), "Mass32"]), np.array(df.loc[df.d32dt.notnull(), "d32dt"])
        x40, y40 = np.array(df.loc[df.d40dt.notnull(), "Mass40"]), np.array(df.loc[df.d40dt.notnull(), "d40dt"])

        self.cal['cons32'] = np.linalg.lstsq(x32[:, np.newaxis], y32)[0][0]
        self.cal['cons40'] = np.linalg.lstsq(x40[:, np.newaxis], y40)[0][0]

        # save in file
        newrow40 = [str(self.today), str(self.cuvette), str(self.membraneid), 'cons40', str(self.cal['cons40'])]
        newrow32 = [str(self.today), str(self.cuvette), str(self.membraneid), 'cons32', str(self.cal['cons32'])]

        with open(self.calfile, 'a') as f:
            f.write(",".join(newrow40) + "\n")
            f.write(",".join(newrow32) + "\n")

        # display result message
        self.reportmsg = "date: <b><font color='red'>" + str(self.today) + "</font></b> <br>" + \
                         "cuvette: <b><font color='red'>" + str(self.cuvette) + "</font></b><br>" + \
                         "cons32: <b><font color='red'>" + str(self.cal['cons32']) + "</font></b><br>" + \
                         "cons40: <b><font color='red'>" + str(self.cal['cons40']) + "</font></b><br>" + \
                         "--------------------------------------------------------------------<br>"

        # display message box
        QMessageBox.about(self, "Consumption", self.reportmsg)


    def cal_co2(self):
        # look for calibration folder
        bicarb_vol = float(self.calib_volinject)
        bicarb_cc = float(self.calib_bicarb_cc)
        cuvette = int(self.cuvette)

        # open list of past calibrations
        dfcal = self.df.loc[:, ['time', 'Mass44']]

        # deriv
        dM44dt = dfcal.Mass44.diff().fillna(0) / dfcal.time.diff().fillna(1)
        M44 = dfcal.Mass44.tolist()

        # find injections
        # rescale data from 0 to 1 to find indices
        z = peakutils.prepare.scale(dM44dt, new_range=(0.0, 1.0), eps=1e-09)
        #        print('z=',z)

        # finds indices of peaks
        indexes = peakutils.indexes(z[0], thres=0.7, min_dist=300)
        print('indexes=', indexes)
        # interpolate
        # peaks = peakutils.interpolate(dfcal.time, z[0], ind=indexes)
        peaks = [int(x) for x in indexes]
        # peaks = list(map(int, indexes))

        # add first and last indices
        peaks.insert(0, 0)  # add a "peak" at zero
        peaks.append(max(dfcal.index))  # add a "peak" at the end to calculate differences
        print("peaks=", peaks)

        plateaux = []
        for c in range(len(peaks) - 1):  # for each injection
            tmp = dM44dt[peaks[c]:peaks[c + 1]]

            # i = x in segment between two peaks where mass44 is the most stable
            # I = global x corresponding to i

            i = np.where(tmp == min(tmp))[0]
            print('i=', i)

            I = i + peaks[c]
            print("I=", I)
            print("M44[I - 10:I]", M44[I - 10:I])
            plateaux.append(np.mean(M44[I - 10:I]))

        jumps = np.diff(plateaux)

        print("plateaux =", plateaux)
        print("jumps=", jumps)

        # How much bic was added in injection
        # 1000 * (millimole/Litre * microlitre) /  microlitre = micromole/Litre
        c = 1000 * (bicarb_cc * bicarb_vol) / cuvette

        if len(jumps) > 4:  # if enough values, we remove highest and lowest values
            jumps = np.setdiff1d(jumps, [min(jumps), max(jumps)])

        # calibration (in micromole/litre)/volt
        cal44 = self.myround(np.mean(c / jumps))

        # prepare new row to insert
        newrow = [str(self.today), str(cuvette), str(self.membraneid), 'cal44', str(cal44)]
        with open(self.calfile, 'a') as f:
            f.write(",".join(newrow) + "\n")

        self.reportmsg = "date: <b><font color='red'>" + str(self.today) + "</font></b> <br>" + \
                         "cuvette: <b><font color='red'>" + str(self.cuvette) + "</font></b><br>" + \
                         "type: <b><font color='red'>cal44</font></b><br>" + \
                         "value: <b><font color='red'>" + str(cal44) + "</font></b><br>" + \
                         "--------------------------------------------------------------------\n"

        # display message box
        QMessageBox.about(self, "CO2 calibration", self.reportmsg)

    def cal_zeros(self):
        dfcal = self.df.loc[:, ['time', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49']]
        zero = {}
        for mass in [44, 45, 46, 47, 49]:
            zero[str(mass)] = self.myround(dfcal.loc[(max(dfcal.index) - 10):, 'Mass' + str(mass)].mean())

        # prepare new row to insert
        for key in zero:
            lines = [",".join([str(self.today), str(self.cuvette), str(self.membraneid), 'zero' + key, str(zero[key])])]
            with open(self.calfile, 'a') as f:
                f.write(",".join(lines) + "\n")

    def event_add(self, eventtype):

        self.event_deactivate()

        self.eventcolors = {"CUSTOM": (0, 0, 0, 255),
                            "BIC": (0, 0, 0, 255),
                            "CELLS": (0, 200, 0, 255),
                            "LIGHT ON": (100, 100, 0, 255),
                            "LIGHT OFF": (100, 100, 0, 255),
                            "AZ": (200, 0, 0, 255),
                            "EZ": (0, 0, 200, 255)}

        self.eventdetails = {"CUSTOM": str(self.custom_text.text()),
                             "BIC": "Added " + str(self.bic_vol.text()) + " " + str(
                                 self.lab_bicvolunit.text()) + " of " + str(self.bic_cc.text()) + " " + str(
                                 self.lab_bicccunit.text()) + " bicarbonate",
                             "LIGHT ON": "Light ON (" + str(self.light_int.text()) + " µmol/m2/s)",
                             "LIGHT OFF": "Light OFF",
                             "AZ": "Added " + str(self.az_vol.text()) + " µL of " + str(self.az_cc.text()) + " " + str(
                                 self.lab_azccunit.text()) + " AZ (" + str(
                                 self.myround(float(self.az_vol.text()) * float(self.az_cc.text())) / float(
                                     self.cuvette)) + " " + str(self.lab_azccunit.text()) + " final)",
                             "EZ": "Added " + str(self.ez_vol.text()) + " µL of " + str(self.ez_cc.text()) + " " + str(
                                 self.lab_ezccunit.text()) + " EZ (" + str(
                                 self.myround(float(self.ez_vol.text()) * float(self.ez_cc.text())) / float(
                                     self.cuvette)) + " " + str(self.lab_ezccunit.text()) + " final)"}


        if str(self.cells_cc.text()) == "0":
            self.eventdetails["CELLS"] = "Added " + str(self.cells_vol.text()) + " " + str(
                    self.lab_cellsvolunit.text()) + " of cells (" + \
                    str(self.cells_cc.text()) + " X)"
        else:
            self.eventdetails["CELLS"] = "Added " + str(self.cells_vol.text()) + " " + str(
                    self.lab_cellsvolunit.text()) + " of cells"


        eventtime = self.df.loc[len(self.df.index) - 1, 'time']

        # add event
        self.df.loc[len(self.df.index) - 1, 'eventtype'] = eventtype
        self.df.loc[len(self.df.index) - 1, 'eventdetails'] = self.eventdetails[eventtype]
        self.dfcc.loc[len(self.df.index) - 1, 'eventtype'] = eventtype
        self.dfcc.loc[len(self.df.index) - 1, 'eventdetails'] = self.eventdetails[eventtype]

        # add line
        self.graph_rawdata.addItem(pg.InfiniteLine(pos=(eventtime + 1) / self.x_axisfactor[self.xscale], angle=90,
                                                   pen=self.eventcolors[eventtype], movable=False, bounds=None))
        self.graph_enrichrate.addItem(pg.InfiniteLine(pos=(eventtime + 1) / self.x_axisfactor[self.xscale], angle=90,
                                                      pen=self.eventcolors[eventtype], movable=False, bounds=None))

        annotation = pg.TextItem(text=self.eventdetails[eventtype], color=self.eventcolors[eventtype], fill=None,
                                 anchor=(0, 0), angle=-90)
        annotation.setPos((eventtime + 1) / self.x_axisfactor[self.xscale], 0)
        self.graph_enrichrate.addItem(annotation)

        annotation = pg.TextItem(text=self.eventdetails[eventtype], color=self.eventcolors[eventtype], fill=None,
                                 anchor=(0, 0), angle=-90)
        annotation.setPos((eventtime + 1) / self.x_axisfactor[self.xscale], 0)
        self.graph_rawdata.addItem(annotation)

    def event_deactivate(self):
        self.btn_bic.setEnabled(False)
        self.btn_cells.setEnabled(False)
        self.btn_lighton.setEnabled(False)
        self.btn_lightoff.setEnabled(False)
        self.btn_az.setEnabled(False)
        self.btn_ez.setEnabled(False)
        self.btn_custom.setEnabled(False)

    def event_activate(self):
        self.btn_bic.setEnabled(True)
        self.btn_cells.setEnabled(True)
        self.btn_lighton.setEnabled(True)
        self.btn_lightoff.setEnabled(True)
        self.btn_az.setEnabled(True)
        self.btn_ez.setEnabled(True)
        self.btn_custom.setEnabled(True)

    def rolling_linear_reg(self, x, y):
        r = np.zeros(len(x))
        r[:] = np.NAN
        factor = {'s-1': 1,
                  'min-1': 60,
                  'hour-1': 3600}

        A = np.vstack([x, np.ones(len(x))]).T
        for i in range(int(self.smoothing / 2), len(x) - int(self.smoothing / 2)):
            r[i] = self.myround(np.linalg.lstsq(A[i - int(self.smoothing / 2) + 1:i + int(self.smoothing / 2) - 1],
                                                y[i - int(self.smoothing / 2) + 1:i + int(self.smoothing / 2) - 1])[0][
                                    0] * factor[self.yscale])
        return r

    def change_user(self):
        self.user = Ui_userDialog.getUser(user=self.user)
        self.actionUser.setText("User: " + str(self.user))

    def change_cuvette(self):
        for i, cuv in enumerate(self.cuvetteList):
            if cuv == self.cuvette:
                cid = i
        cuvette, ok = QtGui.QInputDialog.getItem(self, 
                                                "Select Cuvette", 
                                                "Select Cuvette", 
                                                 self.cuvetteList,
                                                 cid,
                                                 editable=False)
        if ok:
            self.cuvette = cuvette
            self.actionCuvette.setText("Cuvette: " + str(self.cuvette))

    def change_datafolder(self):
        self.datafolder = QtGui.QFileDialog.getExistingDirectory(self, 'Select folder for data', self.datafolder)
        self.actionDatafolder.setText("Datafolder: " + str(self.datafolder))

    def change_smoothing(self):
        smoothing, ok = QtGui.QInputDialog.getInt(self, 
                                        "Smoothing", 
                                        "Enter an integer value for smoothing",
                                                  self.smoothing, 10, 1000)
        if ok:
            if smoothing >= 10 and smoothing <= 999:
                self.smoothing = smoothing

    def testmode(self):
        print("start testmode...")
        self.exp_type = "test"

        # display units
        self.lab_M32unit.setText(" V")
        self.lab_M40unit.setText(" V")
        self.lab_M44unit.setText(" V")
        self.lab_M45unit.setText(" V")
        self.lab_M46unit.setText(" V")
        self.lab_M47unit.setText(" V")
        self.lab_M49unit.setText(" V")
        self.lab_totCO2unit.setText(" V")

        self.lab_ER47unit.setText(" " + self.yscale)
        self.lab_ER49unit.setText(" " + self.yscale)
        self.lab_d32dtunit.setText(" V." + self.yscale)
        self.lab_d40dtunit.setText(" V." + self.yscale)
        self.lab_d44dtunit.setText(" V." + self.yscale)
        self.lab_d45dtunit.setText(" V." + self.yscale)
        self.lab_d46dtunit.setText(" V." + self.yscale)
        self.lab_d47dtunit.setText(" V." + self.yscale)
        self.lab_d49dtunit.setText(" V." + self.yscale)
        self.lab_dtotalCO2dtunit.setText(" V." + self.yscale)

        self.today = datetime.date.today().strftime('%Y%m%d')

        # clear graphs
        self.graph_rawdata.clear()
        self.graph_enrichrate.clear()
        self.__init__graphs()

        # disable menus
        self.actionAdd_CO2_Calibration.setEnabled(False)
        self.actionStart.setEnabled(False)
        self.actionTestmode.setEnabled(False)
        self.actionAdd_O2_Calibration.setEnabled(False)
        self.actionAdd_Consumptions.setEnabled(False)
        self.actionAdd_Electrical_Zeros.setEnabled(False)

        # activate events
        self.event_activate()

        # initialize timer
        self.exp_start = time.time()
        self.packet_start = time.time()

        # initialise variables
        # initialise variables
        self.dfcolumns = ['time', 'Mass32', 'Mass40', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49', 'eventtype',
                          'eventdetails']
        self.dfcccolumns = ['time', 'Mass32', 'Mass40', 'Mass44', 'Mass45', 'Mass46', 'Mass47', 'Mass49',
                            'eventtype', 'eventdetails', 'totalCO2', 'logE47', 'logE49', 'd32dt', 'd32dt_d', 'd32dt_cd',
                            'enrichrate47',
                            'enrichrate49', 'd40dt', 'd44dt', 'd45dt', 'd46dt', 'd47dt', 'd49dt', 'dtotalCO2dt',
                            'd40dt_d', 'd44dt_d', 'd45dt_d', 'd46dt_d', 'd47dt_d', 'd49dt_d', 'dtotalCO2dt_d']
        self.df = pd.DataFrame(data=np.zeros((0, len(self.dfcolumns))), columns=self.dfcolumns)
        self.dfcc = pd.DataFrame(data=np.zeros((0, len(self.dfcccolumns))), columns=self.dfcccolumns)
        self.total_time = 0
        self.total_packets = 0

        # flush buffer
        self.ser.flushInput()

        # start timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.myupdate_testmode)
        self.timer.start(self.buffer_time * 1000)

    def myupdate_testmode(self):
        # check if events are activated:
        if not self.btn_bic.isEnabled():
            self.event_activate()

        self.previous_packet = self.packet_start
        self.packet_start = time.time()

        # get data from buffer and put it into a bytearray
        u = array.array("B", self.ser.read(self.ser.inWaiting()))

        # split packets
        self.newdata = "-".join(map(str, u)).split("255-255-255-255")

        # count full packets in buffer, excluding 1st and last which may be incomplete
        self.ts['npackets'] = len(self.newdata) - 1

        if self.total_packets > 0:
            # stick first packet with last packet of previous buffer
            self.newdata[0] = self.last + "-" + self.newdata[0]
        else:
            # remove first packet
            self.newdata = self.newdata[1:len(self.newdata)]

        self.last = self.newdata[-1]

        # calculate time between 2 packets
        self.ts['packet_time'] = (self.packet_start - self.previous_packet) / self.ts['npackets']

        if self.ts['npackets'] > 0:
            self.getvolts2()
            self.df = self.df.append(pd.DataFrame(data=self.lastnd[1:], columns=self.dfcolumns), ignore_index=True)
            self.dfcc = self.dfcc.append(pd.DataFrame(data=self.lastnd[1:], columns=self.dfcolumns), ignore_index=True)


        # calculate concentrations and slopes
        self.update_data()

        # update UI
        self.update_ui()

        # update graphs
        self.update_graph()

    def samples_manager(self):
        Ui_SamplesDialog(datafolder=os.path.join(self.datafolder,self.user, time.strftime("%Y%m%d")))

# -- Classe principale (lancement)  --
def main(args):
    a = QApplication(args)  # crée l'objet application
    f = QMainWindow()  # crée le QWidget racine
    c = pyMS(f)  # appelle la classe contenant le code de l'application
    f.showMaximized()  # affiche la fenêtre QWidget
    f.activateWindow()
    r = a.exec_()  # lance l'exécution de l'application

    return r


if __name__ == "__main__":
    main(sys.argv)
