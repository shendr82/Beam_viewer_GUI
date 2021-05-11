# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 15:20:21 2021

@author: ShendR
"""

from Beam_GUI8 import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QDialog


from nptdms import TdmsFile
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from tkinter import filedialog
from tkinter import *
import numpy as np
import matplotlib.animation as animation



from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import TDMS_class_for_GUI2
import TDMS_class_multi_files

class BeamGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
#        self.ui = Ui_MainWindow()
        self.setupUi(self)
        
# Canvas on GUI       
        self.Big_graphicsView = Canvas(parent=self.centralwidget)
        self.Big_graphicsView.setMinimumSize(QtCore.QSize(500, 400))
        self.Big_graphicsView.setObjectName("Big_graphicsView")
        self.gridLayout.addWidget(self.Big_graphicsView, 2, 0, 1, 2)
        
        self.CMOS_display = Canvas(parent=self.CMOS_images)
        self.CMOS_display.setMinimumSize(QtCore.QSize(0, 500))
        self.CMOS_display.setObjectName("CMOS_display")
        self.gridLayout_13.addWidget(self.CMOS_display, 0, 0, 1, 3)
        
        
        self.Big_textBrowser = QtCore.QProcess(self.centralwidget)
#        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
#        sizePolicy.setHorizontalStretch(0)
#        sizePolicy.setVerticalStretch(0)
#        sizePolicy.setHeightForWidth(self.Big_textBrowser.sizePolicy().hasHeightForWidth())
#        self.Big_textBrowser.setSizePolicy(sizePolicy)
#        self.Big_textBrowser.setMinimumSize(QtCore.QSize(400, 50))
#        self.Big_textBrowser.setMaximumSize(QtCore.QSize(16777215, 100))
#        self.Big_textBrowser.setObjectName("Big_textBrowser")
#        self.gridLayout.addWidget(self.Big_textBrowser, 3, 0, 1, 2)
        
        
        
        self.toolbar = NavigationToolbar(self.Big_graphicsView, self.Big_graphicsView)
        
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        
        
        
# Connecting TDMScalss and multiTDMSclass
        self.tdms = TDMS_class_for_GUI2.TDMSData()
        self.multi_tdms = TDMS_class_multi_files.MultiTDMSData()
        
        self.Open_button.clicked.connect(lambda: self.open_file())
        self.Plot_VA_button.clicked.connect(lambda: self.tdms.run_plot_UI(self.Big_graphicsView))
        self.Plot_temp_button.clicked.connect(lambda: self.tdms.run_plot_temperatures(self.Big_graphicsView))
        self.Plot_pressure_button.clicked.connect(lambda: self.tdms.run_plot_pressure(self.Big_graphicsView))
        self.Beam_current_button.clicked.connect(lambda: self.tdms.run_plot_beam_current(self.Big_graphicsView))
# Plot item selected from list of parameters
        self.ParamterPlot_button.clicked.connect(lambda: self.tdms.run_plot_list_item_clicked(self.Big_graphicsView, self.listitemclicked()))
        
# Multiple TDMS files:        
        self.Open_multi_button.clicked.connect(lambda: self.open_multi_files())
        self.CompareCurrFocus_button.clicked.connect(lambda: self.compare_beam_mean())
        self.MultiCurrents_button.clicked.connect(lambda: self.compare_current_button())
        
# CMOS images section
#        self.ShotID_box.text()
        self.Show_CMOS_images.clicked.connect(lambda: self.cmos_shotid_clicked())        
        
        
         
        
    def open_file(self):
#        try:
            self.tdms.run_open_tdms()
            self.updateLCD()
#        except:
#              print('You did not open any file')
        
    def updateLCD(self):
        
# Channels list viwer        
        self.Parameter_listView.clear()
        self.Parameter_listView.setAlternatingRowColors(True)
        channels = self.tdms.run_tdms_channel_list()
        for i in channels:
            self.Parameter_listView.addItem(str(i))
        self.Parameter_listView.itemClicked.connect(self.listitemclicked)
        
# Getting Beam mean values to LCD display        
        bevent = self.tdms.run_beam_mean_values()
        bevent1 = bevent[0]
        bevent2 = bevent[1]
        bevent3 = bevent[2]
        bevent4 = bevent[3]
        
               
        self.EmV_Lcd_disp.display(bevent1)
        self.EmV_Lcd_disp.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.ExV_Lcd_disp.display(bevent2)
        self.ExV_Lcd_disp.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.BeamFocus_Lcd_disp.display(bevent3)
        self.BeamFocus_Lcd_disp.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.BeamMean_Lcd_disp.display(bevent4)
        self.BeamMean_Lcd_disp.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
    
    
# Getting Chopper/Aiming parameters to LCD display
        
        chevent = self.tdms.run_show_aiming_parameters()
        chevent1 = chevent[1]
        chevent2 = chevent[0]
        chevent3 = chevent[3]
        chevent4 = chevent[2]
        chevent5 = chevent[5]
        chevent6 = chevent[4]
        chevent7 = chevent[7]
        chevent8 = chevent[6]
        chevent9 = chevent[9]
        chevent10 = chevent[8]
        chevent11 = chevent[11]
        chevent12 = chevent[10]
        
        self.SetChopPos_Lcd.display(chevent1)
        self.SetChopPos_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.ChopPos_Lcd.display(chevent2)
        self.ChopPos_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.SetChopNeg_Lcd.display(chevent3)
        self.SetChopNeg_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.ChopNeg_Lcd.display(chevent4)
        self.ChopNeg_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.SetPolAimPos_Lcd.display(chevent5)
        self.SetPolAimPos_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.PolAimPos_Lcd.display(chevent6)
        self.PolAimPos_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.SetPolAimNeg_Lcd.display(chevent7)
        self.SetPolAimNeg_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.PolAimNeg_Lcd.display(chevent8)
        self.PolAimNeg_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.SetTorAimPos_Lcd.display(chevent9)
        self.SetTorAimPos_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.TorAimPos_Lcd.display(chevent10)
        self.TorAimPos_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.SetTorAimNeg_Lcd.display(chevent11)
        self.SetTorAimNeg_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.TorAimNeg_Lcd.display(chevent12)  
        self.TorAimNeg_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
    
# Getting Beam sensor parameters to LCD display    
        
        event1 = self.tdms.run_mirror_in_out()[0]
        event2 = self.tdms.run_neut_open_close()[0]
        event3 = self.tdms.run_em_ex_on()[0]
        event3a = self.tdms.run_em_ex_on()[1]
        event4 = self.tdms.run_turbo_on()
        event5 = self.tdms.run_forevacuumpump_on()
        event6 = self.tdms.run_forevacuumvalve_open()
        event7 = self.tdms.run_e_sup_current()
        event8 = self.tdms.run_e_sup_voltage()
        event9 = self.tdms.run_fc1_res_current()
        event10 = self.tdms.run_fc2_res_current()
        
             
    
        self.Mirror_Lcd.display(event1)
        if event1==1:
            self.Mirror_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(100, 200, 50); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        else:
            self.Mirror_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(255, 50, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        self.NeutShutter_Lcd.display(event2)
        if event2==1:
            self.NeutShutter_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(100, 200, 50); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        else:
            self.NeutShutter_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(255, 50, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        self.HVEmitter_Lcd.display(event3)
        if event3==1:
            self.HVEmitter_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(100, 200, 50); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        else:
            self.HVEmitter_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(255, 50, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        
        self.HVExtractor_Lcd.display(event3)
        if event3a==1:
            self.HVExtractor_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(100, 200, 50); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        else:
            self.HVExtractor_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(255, 50, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        
        self.Turbo_Lcd.display(event4)
        if event4==1:
            self.Turbo_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(100, 200, 50); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        else:
            self.Turbo_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(255, 50, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        
        self.Forevacuum_Lcd.display(event5)
        if event5==1:
            self.Forevacuum_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(100, 200, 50); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        else:
            self.Forevacuum_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(255, 50, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        
        self.ForeValve_Lcd.display(event6)
        if event6==1:
            self.ForeValve_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(100, 200, 50); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        else:
            self.ForeValve_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(255, 50, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(0, 0, 0);}")
        
        
        
        self.ESupCurrent_Lcd.display(event7)
        self.ESupCurrent_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.ESupVolt_Lcd.display(event8)
        self.ESupVolt_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.FC1Res_Lcd.display(event9)
        self.FC1Res_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
        self.FC2Res_Lcd.display(event10)
        self.FC2Res_Lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
    
       
# Getting ShotID to Text box         
        info = self.tdms.run_tdms_basic_info()[1][1]  
        self.ShotID_box.setText(info)
        
        
# Getting CMOS images to display and number of images to LCD 
        self.CMOS_ShotID.setText(info)
        
        cmos = self.tdms.run_cmos_anim(self.CMOS_display)
        
        self.CMOS_im_lcd.display(cmos[1])
        self.CMOS_im_lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")
    def cmos_shotid_clicked(self):
        a =self.tdms.run_cmos_by_shotid(self.CMOS_ShotID.text(), self.CMOS_display)
        cmos_im_number = a[1]
        self.CMOS_im_lcd.display(cmos_im_number)
        self.CMOS_im_lcd.setStyleSheet("QLCDNumber {background-color: rgb(0, 0, 0); \
                                                   border-radius: 5px; \
                                                   color: rgb(255, 255, 255);}")

        

# List of paramters - selecting parameter from list
    def listitemclicked(self):
        self.selected_item = self.Parameter_listView.currentItem().text()
        print('Item in the list is clicked:  ' + self.selected_item)
        return self.selected_item
        
# Multiple TDMS section      
        
    def open_multi_files(self):
        self.MultiShot_listWidget.clear()
        self.MultiShot_listWidget.setAlternatingRowColors(True)
        shots = self.multi_tdms.run_open_multiple_tdms()[0]
        for i in shots:
            self.MultiShot_listWidget.addItem(str(i))
               
    def compare_current_button(self):
#        self.multi_res.run_compare_beam_current_plot()  
        self.MultiShot_listWidget.clear()
        self.MultiShot_listWidget.setAlternatingRowColors(True)
        shots = self.multi_tdms.run_compare_beam_current_plot(self.Big_graphicsView)
        for i in shots:
            self.MultiShot_listWidget.addItem(str(i))    
        
    def compare_beam_mean(self):
        self.MultiShot_listWidget.clear()
        self.MultiShot_listWidget.setAlternatingRowColors(True)
        shots = self.multi_tdms.run_plot_beam_meancurrent(self.Big_graphicsView)
        for i in shots:
            self.MultiShot_listWidget.addItem(str(i))
            
            
            
class Canvas(FigureCanvas):

    def __init__(self, parent=None):
        self.fig = Figure()
#        self.fig = plt.figure()
        self.fig.clear()
#        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        super(Canvas, self).__init__(self.fig)      
        

        
         
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    
    widget = BeamGUI()
    widget.show()
    
    app.exec_()
        
        
