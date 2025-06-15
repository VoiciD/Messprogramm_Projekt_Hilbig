# -*- coding: utf-8 -*-
"""
Created on Mon May 19 10:40:06 2025

@author: Daniel Albinger
"""

import time
import aerotech_wrapper as wrapper
import numpy as np
from pyPhotonFocus import pyPFCam
import pyPhotonFocus as photon
from aerotech_exceptions import WrappedDllException


#%% Movement and Resolution Settings
stepwidth = 0.5
speed = 1.0
max_width = 25


#%% Axis Settings
offset_x = 0.0
offset_y = 0.0

#%% Kamera
macStr = "00:11:1C:F5:B9:88"
cam = pyPFCam('C:/Users/project/Desktop/Projekt2025-Vermessung_von_Freiraumflaechen/Python_Scripts/pyPhotonFocus/pyPhotonFocusC/x64/Release')

cam.connect(macStr)

def camsettings():
    cam.imageWidth = 1280
    cam.imageHeight = 720
    cam.expTime = 10000.0 
    cam.blackLevel = 146.0
    cam.digitalOffset = 0
    cam.gain = 1.
    cam.setOffset(1000, 1000)
    cam.setPixelFormat('Mono8')
    

def grabBuffer():
    buffer = cam.getImage()
    np.save('C:/Users/project/Desktop/Projekt2025-Vermessung_von_Freiraumflaechen/Bufferspeicher/buffer.npy',buffer)
    return buffer


    

#%% Funktionen zum steuern
def connect():
    try:
        connection = wrapper.connect()
        axislist = connection.get_axis_list()
        print("Verbindung hergestellt")
    except WrappedDllException as e:
        print(e.code, e.cause)
        print("Verbindung zum Kontroller fehlgeschlagen")
    return connection, axislist

def disconnect(connection):
    try:
        wrapper.disable_all(connection)
        wrapper.disconnect(connection)
        print("Verbindung getrennt")
    except WrappedDllException as e:
        print(e.code, e.cause) 
    return

def home(axislist):
    try:
        wrapper.home_axis(axislist[0])
        wrapper.home_axis(axislist[1])
        print("Homing durchgeführt")
    except WrappedDllException as e:
        print(e.code, e.cause)
    return

def move_origin():
    try:
        wrapper.motion_move_abs(axislist[0],0.0,speed)
        wrapper.motion_move_abs(axislist[1],0.0,speed)
    except WrappedDllException as e:
        print(e.code, e.cause)   
    return
        
def measurment_x_axis(max_width,stepwdith):
    res = int(max_width/stepwidth)
    try:
        for point in range(0,res):
            wrapper.motion_move_abs(axislist[0],point*stepwidth,speed)
            axis_pos(axislist)
            grabBuffer()
            #time.sleep(0.1)                             #Platzhalte später noch austauschen
    except WrappedDllException as e:
       print(e.code, e.cause) 
    return

def axis_pos(axislist):
    try:
        x_pos = wrapper.position_info(axislist[0])
        y_pos = wrapper.position_info(axislist[1])
        print("Current Position:","x=",x_pos,"y=",y_pos)
    except WrappedDllException as e:
       print(e.code, e.cause)  
    return x_pos, y_pos

#%%Steuerung
        
# connection, axislist = connect()
    
# try:
#     wrapper.enable_all(connection)
#     home(axislist)
    
#     wrapper.set_custom_xy_orign(offset_x, offset_y, connection)
    
#     wrapper.enable_axis(axislist[0])
#     #wrapper.motion_move_abs(axislist[0],10.0,speed)

#     for point in range(0,max_width):
#         wrapper.motion_move_abs(axislist[1],point*stepwidth,speed)
#         time.sleep(1)
# except WrappedDllException as e:
#     print(e.code, e.cause)
#%% Messung


#%% Messebene
camsettings()
y_point = 0.0
res = int(max_width/stepwidth)

 
try:
    connection,axislist = connect()
    wrapper.enable_all(connection)
    wrapper.set_custom_xy_orign(offset_x, offset_y, connection)
    home(axislist)
    
    
    while y_point <= max_width:
        wrapper.motion_move_abs(axislist[1],y_point,speed)
        wrapper.motion_move_abs(axislist[0],0.0,10.0)
        #measurment_x_axis(max_width, stepwidth)
        for point in np.arange(0,(max_width+stepwidth),stepwidth)
        :
            wrapper.motion_move_abs(axislist[0],point*stepwidth,speed)
            time.sleep(0.1) 
            x_pos, y_pos = axis_pos(axislist)
            buffer = grabBuffer()
            bufferpfad = f"C:/Users/project/Desktop/Projekt2025-Vermessung_von_Freiraumflaechen/Bufferspeicher/buffer_{round(x_pos,1)}_{round(y_pos,1)}.npy"
            np.save(bufferpfad,buffer)
        
        
        y_point = y_point + stepwidth
        print(y_point)
    else:
        cam.disconnect()
        print("Messung beendet")
except WrappedDllException as e:
    print(e.code, e.cause)





        
            
