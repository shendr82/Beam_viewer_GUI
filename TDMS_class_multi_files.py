# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 14:48:22 2021

@author: ShendR
"""
from nptdms import TdmsFile
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from tkinter import filedialog
from tkinter import *
import numpy as np
import pandas as pd


class MultiTDMSData:
    def __init__(self):
        pass
        

    def run_open_multiple_tdms(self):
        self.open_multiple_tdms = open_multiple_tdms()
        self.read_tdms_file = read_tdms_file(self.open_multiple_tdms)
        self.just_HV_raise_data = just_HV_raise_data(self.open_multiple_tdms)
        return self.read_tdms_file
        
    def run_pd_dataframe(self):
        self.pd_dataframe = pd_dataframe(self.read_tdms_file)
        
    def run_pd_dataframe2(self):
        self.pd_dataframe2 = pd_dataframe2(self.just_HV_raise_data)
        
    def run_compare_beam_current_plot(self, plot_area):
        if hasattr(self, 'read_tdms_file') is False:
            self.run_open_multiple_tdms()
        self.compare_beam_current_plot = compare_beam_current_plot(self.read_tdms_file, plot_area)
        return self.compare_beam_current_plot
        
    def run_compare_beam_values(self):
        if hasattr(self, 'just_HV_raise_data') is False:
            self.run_open_multiple_tdms()
        self.compare_beam_values = compare_beam_values(self.just_HV_raise_data)
        
    def run_plot_beam_meancurrent(self, plot_area):
        if hasattr(self, 'compare_beam_values') is False:
#            self.run_open_multiple_tdms()
            self.run_compare_beam_values()
        self.plot_beam_meancurrent = plot_beam_meancurrent(self.just_HV_raise_data, self.compare_beam_values, plot_area)
        return self.plot_beam_meancurrent
        
    
        
        
        

def open_multiple_tdms():
    root = Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    files = filedialog.askopenfilename(multiple=True) 
    var = root.tk.splitlist(files)
    filePaths = []
    shotid = []
    for f in var:
        filePaths.append(f)
        shotid.append(f[45:57])
    filePaths
    return shotid, filePaths
#open_multiple_tdms = open_multiple_tdms()

def read_tdms_file(open_multiple_tdms):
    shotid = []
    dict1 = {}
    for i in open_multiple_tdms[1]:
        tdms_file = TdmsFile(i)
        
        def tdms_groups_list():
            group_list = tdms_file.groups()
            return group_list

        group_list = tdms_groups_list()


        def tdms_channel_list(group = 'Neut-Active-1'):
            channels=[]
            channel_list = tdms_file.group_channels(group)
            for c in channel_list:
                channels.append(c.channel)
       
            return channels
        
        channels = tdms_channel_list(group_list[1])
        
        def get_channels_data(channel):
            data=list()            
            for q in group_list:                
                TS=tdms_file.object(q, channel)
                data.extend(list(TS.data))                
            data_array = np.array(data)
                
            return data  
        
        def data_array(channel=channels[0]):
            array = get_channels_data(channel)
            nparray = np.array(array)
            return nparray
        
        shotid.append(i[45:57])

# ****** Just Emitter and Extractor - Volage and Current data  *****       
        dict1[i[45:57]] = [data_array(), data_array(channels[39]), data_array(channels[40]), data_array(channels[44]), data_array(channels[45])]
        
#    print(shotid)
    return dict1, shotid

#read_tdms = read_tdms_file()
#read_tdms.keys()
#
#keys = []
#for key in read_tdms:
#    keys.append(key)
    
    
def just_HV_raise_data(open_multiple_tdms):
    shotid = []
    dict2 = {}
    for i in open_multiple_tdms[1]:
        tdms_file = TdmsFile(i)
        
        def tdms_groups_list():
            group_list = tdms_file.groups()
            return group_list

        group_list = tdms_groups_list()


        def tdms_channel_list(group = 'Neut-Active-1'):
            channels=[]
            channel_list = tdms_file.group_channels(group)
            for c in channel_list:
                channels.append(c.channel)
       
            return channels
        
        channels = tdms_channel_list(group_list[1])
        
        def get_onegroup_data(channel, group = 'HV-Beam-1'):
            data=list()
                    
            TS=tdms_file.object(group, channel)
            data.extend(list(TS.data))
                
            data_array = np.array(data)        
            return data  
        
        def data_array(channel=channels[0]):
            array = get_onegroup_data(channel)
            nparray = np.array(array)
            return nparray
        
        shotid.append(i[45:57])

# ****** Just Emitter and Extractor - Volage and Current data  *****       
        dict2[i[45:57]] = [data_array(), data_array(channels[39]), data_array(channels[40]), data_array(channels[44]), data_array(channels[45])]
        
    return dict2, shotid
 
#just_HV_raise_data = just_HV_raise_data()
#just_HV_raise_data.keys()

# ***** Data from the whole measurement - TimeStamp, EmVoltage, Em Current, Ext Voltage, Ext Current
def pd_dataframe(read_tdms_file):
    shotid = read_tdms_file[1]
    dataframe = pd.DataFrame(read_tdms_file[0])
    dataframe.index = ['TimeStamp', 'EmVoltage', 'Em Current', 'Ext Voltage', 'Ext Current']
    dataframe = dataframe.transpose()
#    print(dataframe)
    return dataframe

#dataframe = pd_dataframe(read_tdms)

#columns = dataframe.columns

# ***** Data just from HV rise group (Beam ON) - TimeStamp, EmVoltage, Em Current, Ext Voltage, Ext Current
def pd_dataframe2(just_HV_raise_data):
    dataframe2 = pd.DataFrame(just_HV_raise_data[0])
    dataframe2.index = ['TimeStamp', 'EmVoltage', 'Em Current', 'Ext Voltage', 'Ext Current']
    dataframe2 = dataframe2.transpose()
    return dataframe2

#dataframe2 = pd_dataframe2(just_HV_raise_data)



def compare_beam_current_plot(read_tdms_file, plot_area):    
    shot1=[]
    shot2=[]
    shot3=[]
    shot4=[]
    shot5=[]
    shot6=[]
    
    keys = read_tdms_file[1]
    
    no_of_shots = len(keys)
    shots=[shot1, shot2, shot3, shot4, shot5, shot6]
    
    
    count1 = 0
    for i in range(no_of_shots):
        dframe = pd.DataFrame(read_tdms_file[0][keys[i]])
        dframe.index = ['TimeStamp', 'EmVoltage', 'Em Current', 'Ext Voltage', 'Ext Current']
        dframe = dframe.transpose()
        shots[count1] = dframe[dframe['EmVoltage'] > 1].drop(columns=['EmVoltage','Ext Voltage'])
    #    shots[count1].plot(x='TimeStamp', title='ShotID: '+keys[i])
        count1+=1
        
    #shots[0].plot(x='TimeStamp')
    #shots[1].plot(x='TimeStamp')
    nrow=no_of_shots
    print(nrow)
    if no_of_shots > 4:
        nrow=3
        ncol=2
    else:
        ncol=1
    
#    fig, axes = plt.subplots(nrow, ncol)
    plot_area.fig.clf()
    axes = plot_area.fig.subplots(nrow, ncol)   
#    plot_area.fig.tight_layout()    
    for i in shots:
        if type(i)!=list:
    #        fig, axes = plt.subplots(nrow, ncol)
            # plot counter
            count=0
            for r in range(nrow):
                if ncol==1:        
                    shots[count].plot(x='TimeStamp', title='ShotID: '+keys[count], ax=axes[r], legend=False)
                    count+=1
                else:
                    for c in range(ncol):
                        shots[count].plot(x='TimeStamp', title='ShotID: '+keys[count],ax=axes[r,c], legend=False)
                        count+=1
        else:
            continue
    plot_area.draw()
    return keys

#compare_beam_current = compare_beam_current_plot()

def compare_beam_values(just_HV_raise_data):    
    shot1=[]
    shot2=[]
    shot3=[]
    shot4=[]
    shot5=[]
    shot6=[]
    
    keys = just_HV_raise_data[1]
    
    no_of_shots = len(keys)
    shots=[shot1, shot2, shot3, shot4, shot5, shot6] 
    
    count2 = 0
    for i in range(no_of_shots):      
        dframe = pd.DataFrame(just_HV_raise_data[0][keys[i]])
        dframe.index = ['TimeStamp', 'EmVoltage', 'Em Current', 'Ext Voltage', 'Ext Current']
        dframe = dframe.transpose()
        EmCvalue_array=dframe['Em Current']
        ExCvalue_array=dframe['Ext Current']
        EmVvalue_array=dframe['EmVoltage']
        ExVvalue_array=dframe['Ext Voltage']
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
        shots[count2] = [EmVvalue_mean, ExVvalue_mean, EmVvalue_mean/ExVvalue_mean, EmCvalue_mean1-EmCvalue_mean2-ExCvalue_drop]
        count2+=1
    
#    print(shots)
    return shots
    

#compare_beam_values = compare_beam_values()
#print(compare_beam_values)

def plot_beam_meancurrent(just_HV_raise_data, compare_beam_values, plot_area):
    x = []
    y = []
    y2 = []
    
    keys = just_HV_raise_data[1]
    no_of_shots = len(keys)
    
    for i in range(no_of_shots):
        x.append(keys[i].replace('.',''))
        y.append(compare_beam_values[i][3])
        y2.append(compare_beam_values[i][2])
        
    plot_area.fig.clf()
    fig1 = plot_area.fig.add_subplot(111)
    fig2 = plot_area.fig.add_subplot(111)
#    fig2 = plt.figure()  
    fig1.plot(x,y, lw=1, marker='o', c='r', label = 'Beam Current [mA]')
    fig2.plot(x,y2, lw=1, marker='o', c='b', label = 'Beam focus')
    fig1.set_title('Beam current and focus by ShotID')
    fig1.set_xlabel('ShotID')
    fig1.set_ylabel('Beam current [mA] / focus')
#    fig1.legend()
#    plt.show()
    plot_area.draw()
    return keys
    
#plot_beam_meancurrent = plot_beam_meancurrent()


#multi_res = MultiTDMSData()
#multi_res.run_open_multiple_tdms()
#multi_res.run_pd_dataframe()
#multi_res.run_pd_dataframe2()
#multi_res.run_compare_beam_current_plot()
#multi_res.run_compare_beam_values()
#multi_res.run_plot_beam_meancurrent()


    