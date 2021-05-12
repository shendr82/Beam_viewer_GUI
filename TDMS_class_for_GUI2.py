# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 13:24:59 2021

Class TDMSData is a line of code for Beam viewer GUI

TDMSData contains methods for reading TDMS (Beam parameters) files and uses 
data to show parameters and characteristics of the alkali beam for the given
shot.
These methods get called by buttons clicked in Beam viewer GUI.

IMPORTANT: 
    Line 167 - Check TDMS file location on you drive
    Line 766 - Check CMOS file location on you drive (directory should be shotID)

@author: ShendR
"""

from nptdms import TdmsFile
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import filedialog
from tkinter import *
import numpy as np
import matplotlib.animation as animation
from glob import glob
import cv2


class TDMSData:
    def __init__(self):
        pass
        

    def run_open_tdms(self):
        self.tdms_file = open_tdms()
        self.group_list = tdms_groups_list(self.tdms_file)
        self.channels = tdms_channel_list(self.tdms_file, group = 'Neut-Active-1')
        
    
    def run_tdms_basic_info(self):        
        self.tdms_basic = tdms_basic_info(self.tdms_file)
        return self.tdms_basic
        
#    
    def run_tdms_channel_list(self):
        if hasattr(self, 'tdms_file') is False:
            self.run_open_tdms()
        self.channels = tdms_channel_list(self.tdms_file, group = 'Neut-Active-1')
        return self.channels
        
    def run_find_in_channels(self):
        self.string_in_channels = find_in_channels(self.channels, string = 'Voltage')
        
    def run_get_channels_data(self, channel='TimeStamp'):
        self.all_data = get_channels_data(self.tdms_file, self.group_list, channel)
#        print(self.all_data)
    
    def run_get_onegroup_data(self, channel='TimeStamp'):
        self.one_data = get_onegroup_data(self.tdms_file, channel, group = 'HV-Beam-1')
#        print(self.one_data)
        
    def run_data_array_dict(self, channel='TimeStamp'):
        self.dict1 = data_array_dict(self.tdms_file, self.group_list, channel)
#        print(self.dict1)
        
    def run_data_nparray(self, channel='TimeStamp'):
        self.nparray = data_nparray(self.tdms_file, self.group_list, channel)
#        print(self.nparray)
        
    def run_cut_off_values(self, channel='HV Emitter Voltage'):
        self.data_less_than_1 = cut_off_values(self.tdms_file, self.group_list, channel)[0]
#        print(self.data_less_than_1)
        self.cut_off_from = cut_off_values(self.tdms_file, self.group_list, channel)[1]
#        print(self.cut_off_from)
        self.cut_off_to = cut_off_values(self.tdms_file, self.group_list, channel)[2]
#        print(self.cut_off_to)
        self.cut_off_value = [self.data_less_than_1, self.cut_off_from, self.cut_off_to]
#        print(self.cut_off_value)
#        return self.cut_off_value
        
    def run_beam_mean_values(self):
        self.beam_mean_values = beam_mean_values(self.tdms_file, self.channels, group = 'HV-Beam-1' )
        print('Beam mean values:')
        print(self.beam_mean_values)
        return self.beam_mean_values
    
    def run_plot_beam_current(self, plot_area):
        self.plot_beam_current = plot_beam_current(self.tdms_file, self.channels, plot_area, group = 'HV-Beam-1')
        
    def run_plot_UI(self, plot_area, cut_off=True):
        if hasattr(self, 'cut_off_from') is False:
            self.run_cut_off_values()
        self.plot_UI = plot_UI(self.tdms_file, self.group_list, self.channels, self.cut_off_from, self.cut_off_to, plot_area, cut_off)
        
    def run_anim_plot_UI(self, plot_area, cut_off=True):
        if hasattr(self, 'cut_off_from') is False:
            self.run_cut_off_values()
        self.anim_plot_UI = anim_plot_UI(self.tdms_file, self.group_list, self.channels, self.cut_off_from, self.cut_off_to, plot_area, cut_off)
    
    def run_plot_pressure(self, plot_area):
        self.plot_pressure = plot_pressure(self.tdms_file, self.group_list, self.channels, plot_area)

    def run_plot_temperatures(self, plot_area):
        self.plot_temperatures = plot_temperatures(self.tdms_file, self.group_list, self.channels, plot_area)
     
    def run_show_aiming_parameters(self):
        self.show_aiming_parameters = show_aiming_parameters(self.tdms_file, self.group_list, self.channels)
        return self.show_aiming_parameters
        
    def run_mirror_in_out(self):
        self.mirror_in_out = mirror_in_out(self.tdms_file, self.group_list, self.channels)
        return self.mirror_in_out
        
    def run_neut_open_close(self):
        self.neut_open_close = neut_open_close(self.tdms_file, self.channels, group = 'HV-Beam-1' )
        return self.neut_open_close
        
    def run_em_ex_on(self):
        self.em_ex_on = em_ex_on(self.tdms_file, self.channels, group = 'HV-Beam-1' )
        return self.em_ex_on
        
    def run_turbo_on(self):
        self.turbo_on = turbo_on(self.tdms_file, self.group_list, self.channels)
        return self.turbo_on
        
    def run_forevacuumpump_on(self):
        self.forevacuumpump_on = forevacuumpump_on(self.tdms_file, self.group_list, self.channels)   
        return self.forevacuumpump_on
        
    def run_forevacuumvalve_open(self):
        self.forevacuumvalve_open = forevacuumvalve_open(self.tdms_file, self.group_list, self.channels)
        return self.forevacuumvalve_open
        
    def run_e_sup_current(self):
        self.e_sup_current = e_sup_current(self.tdms_file, self.group_list, self.channels)
        return self.e_sup_current
        
    def run_e_sup_voltage(self):
        self.e_sup_voltage = e_sup_voltage(self.tdms_file, self.group_list, self.channels)
        return self.e_sup_voltage
        
    def run_fc1_res_current(self):
        self.fc1_res_current = fc1_res_current(self.tdms_file, self.group_list, self.channels)
        return self.fc1_res_current
        
    def run_fc2_res_current(self):
        self.fc2_res_current = fc2_res_current(self.tdms_file, self.group_list, self.channels)
        return self.fc2_res_current
    
    def run_plot_list_item_clicked(self, plot_area, item_clicked):
        self.plot_list_item_clicked = plot_list_item_clicked(self.tdms_file, self.group_list, self.channels, plot_area, item_clicked)
        
    def run_cmos_anim(self, cmos_plot):
        self.cmos_anim = cmos_anim(self.tdms_file, cmos_plot)
        return self.cmos_anim
    
    def run_cmos_by_shotid(self, entered_shot, cmos_plot):
        self.cmos_by_shotid = cmos_by_shotid(entered_shot, cmos_plot)
        return self.cmos_by_shotid
        
    
        
# Open TDMS file by browsing and puts it in tdms_file
def open_tdms():    
    root = Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    root.filename = filedialog.askopenfilename(initialdir='C:\ShendR\Python\TDMS\TDMS files\TDMS_shotID' , title='Select a file', filetypes=(('TDMS files', '*.tdms'),('All files','*.*')))
    tdms_file = TdmsFile(root.filename)
    root.destroy()
    root.mainloop()
    return tdms_file


# Get basic information from TDMS file (Name, Date...)
def tdms_basic_info(tdms_file):
    root_obj_keys=[]
    root_obj_values=[]
    root_object=tdms_file.object()
    root_properties=root_object.properties.items()
    for key, value in root_properties:
        root_obj_keys.append(key)
        root_obj_values.append(value)
#    print('From Root properties: \n', '\n', root_obj_keys[1], ': ', root_obj_values[1], "\n", '\n', root_obj_keys[2], ': ', root_obj_values[2], '\n')
    return [root_obj_keys, root_obj_values]

#tdms_basic = tdms_basic_info()
# Gives a touple of elements - access Job name: tdms_basic[1][1]
# root_obj_keys, root_obj_values = tdms_basic_info() ???


# Get the list of groups given in the TDMS file (Neut-Active, HV-Raise...)
def tdms_groups_list(tdms_file):
    group_list = tdms_file.groups()
#    print(group_list)
    return group_list

#group_list = tdms_groups_list()
    


# Get the list of channels in a group (HV Emitter Voltage, HV Emitter Current...)
def tdms_channel_list(tdms_file, group = 'Neut-Active-1'):
    channels=[]
    channel_list = tdms_file.group_channels(group)
    for c in channel_list:
        channels.append(c.channel)
#    print('List of channel Names: \n')
#    for c1 in channels:
#        print(c1)
#    print('\n')
    return channels
#channels = tdms_channel_list(group_list[1])

# Check for String in channel names to find in channels list by index
#string = 'Voltage'
def find_in_channels(channels, string = 'Voltage'):
    string_in_channels = [s for s in channels if string in s]
    print("List of names containing", string, ':', '\n')
    for e in string_in_channels:
        print(e, '------ with index', channels.index(e))
    return string_in_channels

#string_in_channels = find_in_channels('Current')


def get_channels_data(tdms_file, group_list, channel):
    all_data=list()
    
    for q in group_list:
        
        TS=tdms_file.object(q, channel)
        all_data.extend(list(TS.data))
        
    return all_data  
#get_channels_data = get_channels_data(channels[1])    
    
def get_channels_unit(tdms_file, channel):
    
    TS=tdms_file.object('Neut-Active-1', channel)
    unit = TS.property('unit_string')
    
    return unit
        
    
    
def get_onegroup_data(tdms_file, channel, group):
    one_data=list()
            
    TS=tdms_file.object(group, channel)
    one_data.extend(list(TS.data))
            
    return one_data  


def data_array_dict(tdms_file, group_list, channel):    
    dict1 = {}
    dict1[channel] = [get_channels_data(tdms_file, group_list, channel)]
    
    return dict1
    

def data_nparray(tdms_file, group_list, channel):
    array = get_channels_data(tdms_file, group_list, channel)
    nparray = np.array(array)
    return nparray    


def cut_off_values(tdms_file, group_list, channel='HV Emitter Voltage'):
    d = data_array_dict(tdms_file, group_list, channel)
    data_list = d[channel][0]
    data_less_than_1 = [i for i in data_list if i>1]
    
    cut_off_from = data_list.index(data_less_than_1[0])    
    cut_off_to = len(data_less_than_1)
    
    return [data_less_than_1, cut_off_from, cut_off_to]


def beam_mean_values(tdms_file, channel, group):
    EmCvalue_array=get_onegroup_data(tdms_file, 'HV Emitter Current', group)
    ExCvalue_array=get_onegroup_data(tdms_file, 'HV Extractor Current', group)
    EmVvalue_array=get_onegroup_data(tdms_file, 'HV Emitter Voltage', group)
    ExVvalue_array=get_onegroup_data(tdms_file, 'HV Extractor Voltage', group)
    
    EmCvalue_array1=EmCvalue_array[15:len(EmCvalue_array)]
    EmCvalue_mean1=np.mean(EmCvalue_array1)
    EmCvalue_array2=EmCvalue_array[0:5]
    EmCvalue_mean2=np.mean(EmCvalue_array2)
    
    ExCvalue_array1=ExCvalue_array[15:len(ExCvalue_array)]
    ExCvalue_mean1=np.mean(ExCvalue_array1)
    ExCvalue_array2=ExCvalue_array[0:5]
    ExCvalue_mean2=np.mean(ExCvalue_array2)
    ExCvalue_drop=ExCvalue_mean2 - ExCvalue_mean1
    
    EmVvalue_array1=EmVvalue_array[15:len(EmVvalue_array)]
    EmVvalue_mean=np.mean(EmVvalue_array1)
    
    ExVvalue_array1=ExVvalue_array[15:len(ExVvalue_array)]
    ExVvalue_mean=np.mean(ExVvalue_array1)
    
   
    return [EmVvalue_mean, 
            ExVvalue_mean, 
            ExVvalue_mean/(EmVvalue_mean-ExVvalue_mean), 
            EmCvalue_mean1-EmCvalue_mean2-ExCvalue_drop]
    

def plot_beam_current(tdms_file, channel, plot_area, group):
    EmCvalue_array=get_onegroup_data(tdms_file, 'HV Emitter Current', group)
    ExCvalue_array=get_onegroup_data(tdms_file, 'HV Extractor Current', group)
    TimeStamp = get_onegroup_data(tdms_file, 'TimeStamp', group)
    TimeStamp_array = TimeStamp[15:len(TimeStamp)]
    
    EmCvalue_array1=EmCvalue_array[15:len(EmCvalue_array)]
    EmCvalue_array2=EmCvalue_array[0:4]
    EmCvalue_mean2=np.mean(EmCvalue_array2)
    
    ExCvalue_array1=ExCvalue_array[15:len(ExCvalue_array)]
#    ExCvalue_mean1=np.mean(ExCvalue_array1)
    ExCvalue_array2=ExCvalue_array[0:4]
    ExCvalue_mean2=np.mean(ExCvalue_array2)
#    ExCvalue_drop=ExCvalue_mean2 - ExCvalue_mean1
    ExCvalue_array3 = []
    for j in ExCvalue_array1:
        ExCvalue_array3.append(ExCvalue_mean2 - j)
    
    EmCvalue_array3 = []
    for i in EmCvalue_array1:
        EmCvalue_array3.append(i - EmCvalue_mean2)
        
    beam_current = [x - y for x, y in zip(EmCvalue_array3, ExCvalue_array3)]
    
    plot_area.fig.clf()
    BeamC = plot_area.fig.add_subplot(111)
    BeamC.plot(TimeStamp_array, beam_current)
    BeamC.set_title('Beam Current')
    BeamC.set_ylabel('Beam Current' + ' [mA]')
    BeamC.set_xlabel('TimeStamp' +' [s]')    
#    plot_area.fig.tight_layout()        
    plot_area.draw()
    
            
    
def plot_UI(tdms_file, group_list, channel, cut_off_from, cut_off_to, plot_area ,cut_off=True):   
    # Get data dictionarys to plot out
    f_x = data_nparray(tdms_file, group_list, 'TimeStamp')   # TimeStamp ------ with inde 0
    f_y1 = data_nparray(tdms_file, group_list, 'HV Emitter Voltage') # HV Emitter Voltage ------ with index 39
    f_y2 = data_nparray(tdms_file, group_list, 'HV Emitter Current') # HV Emitter Current ------ with index 40
    f_y3 = data_nparray(tdms_file, group_list, 'HV Extractor Voltage') # HV Extractor Voltage ------ with index 44
    f_y4 = data_nparray(tdms_file, group_list, 'HV Extractor Current') # HV Extractor Current ------ with index 45
    
    #Converting Timestamps (from 1904.01.01 seconds) into date
    TS_first = f_x[0]
    TS_last = f_x[-1]
    dt = datetime.fromtimestamp(TS_first - 2082844800)
    dt1= datetime.fromtimestamp(TS_last - 2082844800)
    s='Start at: ' + str(dt)
    s5=dt1.time()
    
    # Transform timestamp to start from 0
    f_x0 = get_channels_data(tdms_file, group_list, 'TimeStamp')
    f_x1 = f_x0 - TS_first    
    
    # Cut off Voltage values less than 1 V - (NO Beam values)
    if cut_off is True:
        f = cut_off_from
        t = cut_off_to
        f_x1 = f_x1[f:t+f]
        f_y1 = f_y1[f:t+f]
        f_y2 = f_y2[f:t+f]
        f_y3 = f_y3[f:t+f]
        f_y4 = f_y4[f:t+f]
    
      #Shows the plot of objects dependence of time
      
    plot_area.fig.clf()
    HVEmV = plot_area.fig.add_subplot(211)
    HVEmV.plot(f_x1, f_y1)
    HVEmV.set_title(s)
    HVEmV.set_ylabel('HV Emitter Voltage' + ' [V]')
    HVEmV.set_ylim([min(f_y1)-max(f_y1)*0.05, max(f_y1)+max(f_y1)*0.1])
    
    HVEmC = plot_area.fig.add_subplot(212)
    HVEmC.plot(f_x1, f_y2)
    HVEmC.set_ylabel('HV Emitter Current' + ' [mA]')
    HVEmC.set_ylim([min(f_y2)-max(f_y2)*0.05, max(f_y2)+max(f_y2)*0.1])
    
    HVExV = plot_area.fig.add_subplot(211)
    HVExV.plot(f_x1, f_y3)
    HVExV.set_ylabel('HV Extractor Voltage' + ' [V]')
    
    HVExC = plot_area.fig.add_subplot(212)
    HVExC.plot(f_x1, f_y4)
    HVExC.set_ylabel('HV Extractor Current' + ' [mA]')
    HVExC.set_ylim([min(f_y2)-max(f_y2)*0.05, max(f_y2)+max(f_y2)*0.1])
    HVExC.set_xlabel('TimeStamp' +' [s]')    
#    plot_area.fig.tight_layout()        
    plot_area.draw()
    

def anim_plot_UI(tdms_file, group_list, channel, cut_off_from, cut_off_to, plot_area, cut_off=True):   
    f_x = data_nparray(tdms_file, group_list, 'TimeStamp')   # TimeStamp ------ with inde 0
    f_y1 = data_nparray(tdms_file, group_list, 'HV Emitter Voltage') # HV Emitter Voltage ------ with index 39
    f_y2 = data_nparray(tdms_file, group_list, 'HV Emitter Current') # HV Emitter Current ------ with index 40
    f_y3 = data_nparray(tdms_file, group_list, 'HV Extractor Voltage') # HV Extractor Voltage ------ with index 44
    f_y4 = data_nparray(tdms_file, group_list, 'HV Extractor Current') # HV Extractor Current ------ with index 45
    
    
    #Converting Timestamps (from 1904.01.01 seconds) into date
    TS_first = f_x[0]
    TS_last = f_x[-1]
    dt = datetime.fromtimestamp(TS_first - 2082844800)
    dt1= datetime.fromtimestamp(TS_last - 2082844800)
    s='Start at: ' + str(dt)
    s5=dt1.time()
    
    # Transform timestamp to start from 0
    f_x0 = get_channels_data(tdms_file, group_list, 'TimeStamp')
    f_x1 = f_x0 - TS_first
    
    # Cut off Voltage values less than 1 V - (NO Beam values)
    if cut_off is True:
        f = cut_off_from
        t = cut_off_to
        f_x1 = f_x1[f:t+f]
        f_y1 = f_y1[f:t+f]
        f_y2 = f_y2[f:t+f]
        f_y3 = f_y3[f:t+f]
        f_y4 = f_y4[f:t+f]
      
#    fig1, (ax1, ax2, ax3, ax4) = plt.subplots(4,1)
    plot_area.fig.clf()
    ax1 = plot_area.fig.add_subplot(411)
    ax2 = plot_area.fig.add_subplot(412)
    ax3 = plot_area.fig.add_subplot(413)
    ax4 = plot_area.fig.add_subplot(414)

    # intialize two line objects (one in each axes)
    line1, = ax1.plot([], [], lw=2)
    line2, = ax2.plot([], [], lw=2, color='r')
    line3, = ax3.plot([], [], lw=2, color='g')
    line4, = ax4.plot([], [], lw=2, color='c')
    line = [line1, line2, line3, line4]
    
    ax1.set_xlim(min(f_x1), max(f_x1))
    ax1.set_ylim(min(f_y3)-max(f_y3)*0.05, max(f_y3)+max(f_y3)*0.1)    
    ax1.grid()
    ax1.set_title(s) 
    ax2.set_xlim(min(f_x1), max(f_x1))
    ax2.set_ylim(min(f_y3)-max(f_y3)*0.05, max(f_y3)+max(f_y3)*0.1)
    ax2.grid()
    ax3.set_xlim(min(f_x1), max(f_x1))
    ax3.set_ylim(min(f_y2)-max(f_y2)*0.05, max(f_y2)+max(f_y2)*0.1)
    ax3.grid()
    ax4.set_xlim(min(f_x1), max(f_x1))
    ax4.set_ylim(min(f_y2-max(f_y2)*0.05), max(f_y2)+max(f_y2)*0.1)
    ax4.grid()
    
    # initialize the data arrays 
    xdata, y1data, y2data, y3data, y4data = [], [], [], [], []
    def run(i):
        
        # update the data
        xdata.append(f_x1[i])
        y1data.append(f_y1[i])
        y2data.append(f_y3[i])
        y3data.append(f_y2[i])
        y4data.append(f_y4[i])
        
        if i==0:
            xdata.clear()
            y1data.clear()
            y2data.clear()
            y3data.clear()
            y4data.clear()
    
        # update the data of both line objects
        line[0].set_data(xdata, y1data)
        line[1].set_data(xdata, y2data)
        line[2].set_data(xdata, y3data)
        line[3].set_data(xdata, y4data)
    
        return line
        
    ani = animation.FuncAnimation(plot_area.fig, run, repeat=True, frames=len(f_x1), interval=1)
    
    return ani


def plot_pressure(tdms_file, group_list, channel, plot_area):
    # Get data dictionarys to plot out
    f_x = data_nparray(tdms_file, group_list, 'TimeStamp')   # TimeStamp ------ with inde 0
    f_y1 = data_nparray(tdms_file, group_list,'PA1 Pressure') # PA1 Pressure ------ with index 35
    f_y2 = data_nparray(tdms_file, group_list,'PA2 Pressure') # PA2 Pressure ------ with index 36
    f_y3 = data_nparray(tdms_file, group_list,'PB1 Pressure') # PB1 Pressure ------ with index 37
    f_y4 = data_nparray(tdms_file, group_list,'PB2 Pressure') # PB2 Pressure ------ with index 38
    
    #Converting Timestamps (from 1904.01.01 seconds) into date
    TS_first = f_x[0]
    TS_last = f_x[-1]
    dt = datetime.fromtimestamp(TS_first - 2082844800)
    dt1= datetime.fromtimestamp(TS_last - 2082844800)
    s='Start at: ' + str(dt)
    s5=dt1.time()
    
    # Transform timestamp to start from 0
    f_x0 = get_channels_data(tdms_file, group_list, 'TimeStamp')
    f_x1 = f_x0 - TS_first
    
    plot_area.fig.clf()
    PA1 = plot_area.fig.add_subplot(411)
    PA1.plot(f_x1, f_y1)
    PA1.set_title(s)
    PA1.set_ylabel('PA1 Pressure [mbar]')
    
    PA2 = plot_area.fig.add_subplot(412)
    PA2.plot(f_x1, f_y2)
    PA2.set_ylabel('PA2 Pressure [mbar]')
    
    PB1 = plot_area.fig.add_subplot(413)
    PB1.plot(f_x1, f_y3)
    PB1.set_ylabel('PB1 Pressure [mbar]')
    
    PB2 = plot_area.fig.add_subplot(414)
    PB2.plot(f_x1, f_y4)
    PB2.set_ylabel('PB2 Pressure [mbar]')
    PB2.set_xlabel('TimeStamp' +' [s]')           
    plot_area.draw()
        
          
def plot_temperatures(tdms_file, group_list, channel, plot_area):
    # Get data dictionarys to plot out
    f_x = data_nparray(tdms_file, group_list, 'TimeStamp')   # TimeStamp ------ with inde 0
    f_y1 = data_nparray(tdms_file, group_list, 'TC  W7X SideCone') # TC  W7X SideCone ------ with index 1
    f_y2 = data_nparray(tdms_file, group_list, 'TC Oven Temp') # TC Oven Temp ------ with index 2
    f_y3 = data_nparray(tdms_file, group_list, 'TC Emit SideCone') # TC Emit SideCone ------ with index 3
    f_y4 = data_nparray(tdms_file, group_list, 'TC3') # TC3 ------ with index 4
    f_y5 = data_nparray(tdms_file, group_list, 'TC Plate Temp') # TC Plate Temp ------ with index 5
    f_y6 = data_nparray(tdms_file, group_list, 'TC Plate Temp') # TC Plate Temp ------ with index 5
    
    #Converting Timestamps (from 1904.01.01 seconds) into date
    TS_first = f_x[0]
    TS_last = f_x[-1]
    dt = datetime.fromtimestamp(TS_first - 2082844800)
    dt1= datetime.fromtimestamp(TS_last - 2082844800)
    s='Start at: ' + str(dt)
    s5=dt1.time()
    
    # Transform timestamp to start from 0
    f_x0 = get_channels_data(tdms_file, group_list, 'TimeStamp')
    f_x1 = f_x0 - TS_first
    
#    fig=plt.figure()
#    plt.subplot(611)
#    plt.plot(f_x1, f_y1)
#    plt.title(s)
#    plt.ylabel('TC  W7X SideCone' + ' [°C]')
#    
#    plt.subplot(612)
#    plt.plot(f_x1, f_y2)
#    plt.ylabel('TC Oven Temp' + ' [°C]')
#    
#    plt.subplot(613)
#    plt.plot(f_x1, f_y3)
#    plt.ylabel('TC Emit SideCone' + ' [°C]')
#    
#    plt.subplot(614)
#    plt.plot(f_x1, f_y4)
#    plt.ylabel('TC3' + ' [°C]')
#    
#    plt.subplot(615)
#    plt.plot(f_x1, f_y5)
#    plt.ylabel('TC Plate Temp' + ' [°C]')
#    
#    plt.subplot(616)
#    plt.plot(f_x1, f_y6)
#    plt.ylabel('TC Top Temp' + ' [°C]')
#    plt.xlabel('Time [s]')
#    plt.text(120,0.8, s5)
#    plt.show()
    
    plot_area.fig.clf()
    TCW7XSide = plot_area.fig.add_subplot(611)
    TCW7XSide.plot(f_x1, f_y1)
    TCW7XSide.set_title(s)
    TCW7XSide.set_ylabel('TC  W7X SideCone' + ' [°C]')
    
    TCOven = plot_area.fig.add_subplot(612)
    TCOven.plot(f_x1, f_y2)
    TCOven.set_ylabel('TC Oven Temp' + ' [°C]')
    
    TCEmitSide = plot_area.fig.add_subplot(613)
    TCEmitSide.plot(f_x1, f_y3)
    TCEmitSide.set_ylabel('TC Emit SideCone' + ' [°C]')
    
    TC3 = plot_area.fig.add_subplot(614)
    TC3.plot(f_x1, f_y4)
    TC3.set_ylabel('TC3' + ' [°C]')
    
    TCPlate = plot_area.fig.add_subplot(615)
    TCPlate.plot(f_x1, f_y4)
    TCPlate.set_ylabel('TC Plate Temp' + ' [°C]')
    
    TCTop = plot_area.fig.add_subplot(616)
    TCTop.plot(f_x1, f_y4)
    TCTop.set_ylabel('TC Top Temp' + ' [°C]')    
    TC3.set_xlabel('TimeStamp' +' [s]')           
    plot_area.draw()
    
    
def show_aiming_parameters(tdms_file, group_list, channel):  
    AI_chopp_pos_V_mean = data_nparray(tdms_file, group_list, 'AI +Chopper Voltage').mean()   # AI +Chopper Voltage ------ with index 10
    AI_chopp_neg_V_mean = data_nparray(tdms_file, group_list, 'AI -Chopper Voltage ').mean()  # AI -Chopper Voltage  ------ with index 11
    AI_aim_pol_pos_V_mean = data_nparray(tdms_file, group_list, 'AI +Aiming(pol) Voltage').mean()  # +Aiming(pol) Voltage ------ with index 12
    AI_aim_pol_neg_V_mean = data_nparray(tdms_file, group_list, 'AI -Aiming(pol) Voltage').mean()  # -Aiming(pol) Voltage ------ with index 13
    AI_aim_tor_pos_V_mean = data_nparray(tdms_file, group_list, 'AI +Aiming(tor) Voltage ').mean()  # +Aiming(tor) Voltage  ------ with index 14
    AI_aim_tor_neg_V_mean = data_nparray(tdms_file, group_list, 'AI -Aiming(tor) Voltage').mean()  # -Aiming(tor) Voltage ------ with index 15
    AO_chopp_pos_V_mean = data_nparray(tdms_file, group_list, 'AO +Chopper Voltage').mean()  # +Chopper Voltage ------ with index 18
    AO_chopp_neg_V_mean = data_nparray(tdms_file, group_list, 'AO -Chopper Voltage').mean()  # -Chopper Voltage ------ with index 19
    AO_aim_pol_pos_V_mean = data_nparray(tdms_file, group_list, 'AO +Aiming(pol) Voltage').mean()  # +Aiming(pol) Voltage ------ with index 20
    AO_aim_pol_neg_V_mean = data_nparray(tdms_file, group_list, 'AO -Aiming(pol) Voltage').mean()  # -Aiming(pol) Voltage ------ with index 21
    AO_aim_tor_pos_V_mean = data_nparray(tdms_file, group_list, 'AO +Aiming(tor) Voltage').mean()  # +Aiming(tor) Voltage ------ with index 22
    AO_aim_tor_neg_V_mean = data_nparray(tdms_file, group_list, 'AO -Aiming(tor) Voltage').mean()  # -Aiming(tor) Voltage ------ with index 23
    
#    print('\n', 'Chopper+ measured mean: ', round(AI_chopp_pos_V_mean,2), '[V]', '---  SET vaule is: ', AO_chopp_pos_V_mean, '[V]', '\n')
#    print('\n', 'Chopper- measured mean: ', round(AI_chopp_neg_V_mean,2), '[V]', '---  SET vaule is: ', AO_chopp_neg_V_mean, '[V]', '\n')
#    print('\n', 'Aiming+ (pol) Voltage mean: ', round(AI_aim_pol_pos_V_mean,2), '[V]', '---  SET vaule is: ', AO_aim_pol_pos_V_mean, '[V]', '\n')
#    print('\n', 'Aiming- (pol) Voltage mean: ', round(AI_aim_pol_neg_V_mean,2), '[V]', '---  SET vaule is: ', AO_aim_pol_neg_V_mean, '[V]', '\n')
#    print('\n', 'Aiming+ (tor) Voltage mean: ', round(AI_aim_tor_pos_V_mean,2), '[V]', '---  SET vaule is: ', AO_aim_tor_pos_V_mean, '[V]', '\n')
#    print('\n', 'Aiming- (tor) Voltage mean: ', round(AI_aim_tor_neg_V_mean,2), '[V]', '---  SET vaule is: ', AO_aim_tor_neg_V_mean, '[V]', '\n')
    
    return [AI_chopp_pos_V_mean, AO_chopp_pos_V_mean, 
            AI_chopp_neg_V_mean, AO_chopp_neg_V_mean,
            AI_aim_pol_pos_V_mean, AO_aim_pol_pos_V_mean,
            AI_aim_pol_neg_V_mean, AO_aim_pol_neg_V_mean,
            AI_aim_tor_pos_V_mean, AO_aim_tor_pos_V_mean,
            AI_aim_tor_neg_V_mean,AO_aim_tor_neg_V_mean]
 
       
def mirror_in_out(tdms_file, group_list, channel):
    mirror_out = data_nparray(tdms_file, group_list, 'DI Mirror out').mean()
    mirror_in = data_nparray(tdms_file, group_list, 'DI Mirror in').mean()
#    print('Mirror out: ', mirror_out)
#    print('Mirror in: ', mirror_in)
    return [mirror_out, mirror_in]
    
    
def neut_open_close(tdms_file, channel, group):
    neut_open = np.array(get_onegroup_data(tdms_file, 'DI Neut shut open', group)).mean()
    neut_closed = np.array(get_onegroup_data(tdms_file, 'DI Neut shut closed', group)).mean()
#    print('Neutralizer shutter open:', neut_open)
#    print('Neutralizer shutter open:', neut_closed)
    return [neut_open, neut_closed]
    
    
def em_ex_on(tdms_file, channel, group):
    emitter_on = np.array(get_onegroup_data(tdms_file, 'HV Emitter ON', group)).mean()
#    print('Emitter ON:', emitter_on)
    extractor_on = np.array(get_onegroup_data(tdms_file, 'HV Extractor ON', group)).mean()
#    print('Extractor ON', extractor_on)
    return [emitter_on, extractor_on]    


def turbo_on(tdms_file, group_list, channel):
    turbo_on = data_nparray(tdms_file, group_list, 'DO Turbo pump power').mean()
#    print('Turbo pump ON:', turbo_on)
    return turbo_on
    
    
def forevacuumpump_on(tdms_file, group_list, channel):
    forevacuumpump_on = data_nparray(tdms_file, group_list, 'DO Forevacuum pump power').mean()
#    print('Forevacuum pump ON:', forevacuumpump_on)
    return forevacuumpump_on
    
    
def forevacuumvalve_open(tdms_file, group_list, channel):
    forevacuumvalve_open = data_nparray(tdms_file, group_list, 'DI Forevac valve open').mean()
#    print('Forevacuum valve open:', forevacuumvalve_open)
    return forevacuumvalve_open


def e_sup_current(tdms_file, group_list, channel):
    e_sup_current = data_nparray(tdms_file, group_list, 'AI E.supp Current ').mean()
#    print('E.supp Current:', round(e_sup_current, 4), '[mA]')
    return e_sup_current
    
def e_sup_voltage(tdms_file, group_list, channel):
    e_sup_voltage = data_nparray(tdms_file, group_list, 'AI E.supp Voltage').mean()
#    print('E.supp Voltage:', round(e_sup_voltage, 2), '[V]')
    return e_sup_voltage
    
    
def fc1_res_current(tdms_file, group_list, channel):
    fc1_res_current = data_nparray(tdms_file, group_list, 'AI FC1 Resistor Current ').mean()
#    print('FC1 Resistor Current:', round(fc1_res_current, 4), '[mA]')
    return fc1_res_current
    
def fc2_res_current(tdms_file, group_list, channel):
    fc2_res_current = data_nparray(tdms_file, group_list, 'AI FC2 Resistor Current').mean()
#    print('FC2 Resistor Current:', round(fc2_res_current, 4), '[mA]')  
    return round(fc2_res_current, 4)
    

def plot_list_item_clicked(tdms_file, group_list, channel, plot_area, item_clicked):
    f_x = data_nparray(tdms_file, group_list, 'TimeStamp')
    f_y1 = data_nparray(tdms_file, group_list, str(item_clicked))
    unit = get_channels_unit(tdms_file, str(item_clicked))
    
    TS_first = f_x[0]
    TS_last = f_x[-1]
    dt = datetime.fromtimestamp(TS_first - 2082844800)
    dt1= datetime.fromtimestamp(TS_last - 2082844800)
    s='Start at: ' + str(dt)
    s5=dt1.time()
    
    # Transform timestamp to start from 0
    f_x0 = get_channels_data(tdms_file, group_list, 'TimeStamp')
    f_x1 = f_x0 - TS_first
    
    plot_area.fig.clf()
    itemclicked = plot_area.fig.add_subplot(111)
    itemclicked.plot(f_x1, f_y1)
    itemclicked.set_ylabel(item_clicked + ' ' + '[' + unit + ']')    
    itemclicked.set_xlabel('TimeStamp' +' [s]')           
    plot_area.draw()
    
    
def cmos_anim(tdms_file, cmos_plot):
    cmos_plot.fig.clf()
    cmos_plot.close_event()
    try:        
        shot_id = tdms_basic_info(tdms_file)[1][1]
        mydir = "C:\\Shendr\\Python\\HDF5\\" + shot_id
        print('Showing CMOS images for Shot: ' + shot_id)
        file_list = glob(mydir + "/*.bmp")    
        images = []
        for i in file_list:
            a = cv2.imread(i)
            images.append(a)          
        cmos_plot.fig.clf()
        ax = cmos_plot.fig.add_subplot(111, axes=None)  
        ax.set_axis_off()
        ims = []
        for x in range(len(images)):
            x += 0
            im = ax.imshow(images[x], animated=True)       
            ims.append([im])
            ani = animation.ArtistAnimation(cmos_plot.fig, ims, interval=50, blit=True, repeat_delay=1000)
        #    ani.save('dynamic_images.gif', writer='pillow')
        return [ani, len(images)]
    
    except:
        cmos_plot.fig.clf()
        cmos_plot.close_event()
        print("There are no CMOS images for this ShotID")
        return [0, 0]
        

def cmos_by_shotid(entered_shot, cmos_plot):
    cmos_plot.fig.clf()
    cmos_plot.close_event()
    try:
        mydir = "C:\\Shendr\\Python\\HDF5\\" + entered_shot
        print('Showing CMOS images for Shot: ' + entered_shot)
        file_list = glob(mydir + "/*.bmp")    
        images = []
        for i in file_list:
            a = cv2.imread(i)
            images.append(a)            
        cmos_plot.fig.clf()
#        cmos_plot.fig.tight_layout()
        ax = cmos_plot.fig.add_subplot(111)
        ax.set_axis_off()
#        ax.get_tightbbox()
        ims = []
        for x in range(len(images)):
            x += 0
            im = ax.imshow(images[x], animated=True)       
            ims.append([im])
            ani = animation.ArtistAnimation(cmos_plot.fig, ims, interval=50, blit=True, repeat_delay=1000)
        #    ani.save('dynamic_images.gif', writer='pillow')
        return [ani, len(images)]
    
    except:
        cmos_plot.fig.clf()
        cmos_plot.close_event()
        print("There are no CMOS images for this ShotID")
        return [0, 0]


# Testing Class methods:
    
#results = TDMSData()
#results.run_open_tdms()
#results.run_tdms_basic_info()
#results.run_tdms_basic_info()[1][1] # <--- ShotID
#results.run_tdms_groups_list()
#results.run_tdms_channel_list()
#results.run_find_in_channels()
#results.run_get_channels_data('TC Oven Temp')
#results.run_get_onegroup_data('TC Oven Temp')
#results.run_data_array_dict()
#results.run_data_nparray()
#results.run_cut_off_values()
#results.run_beam_mean_values()
#results.run_plot_UI()
#results.run_anim_plot_UI()
#results.run_plot_pressure()
#results.run_plot_temperatures()
#results.run_show_aiming_parameters()
#results.run_mirror_in_out()
#results.run_neut_open_close()
#results.run_em_ex_on()
#results.run_turbo_on()
#results.run_forevacuumpump_on()
#results.run_forevacuumvalve_open()
#results.run_e_sup_current()
#results.run_e_sup_voltage()
#results.run_fc1_res_current()
#results.run_fc2_res_current()

