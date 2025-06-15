# -*- coding: utf-8 -*-
"""
Created on Mon May 26 11:00:48 2025

@author: Daniel Albinger
"""
import numpy as np
#%% Importieren der xy-Achsenbibliotheken
from Aerotech import *
from Aerotech import xy_Achsen as xy

#%% Importieren der z-Achsenbibliothek
from Achse_z import PyOwisDC500 as z

#%% Importieren der Kamerabibliotheken
from pyPhotonFocus import pyPhotonFocus as photon

#%% Imprtieren der Schwerpunktanalysebibliothek
from Schwerpunkt import schwerpunkt as schwer

#%% Achseneinstellungen
stepwidth = 0.5         #Schrittweite in mm
speed = 10.0            #Verfahrgeschwindigkeit 
max_width = 25          #Maximale Verfahrbare Länge in mm für die x- und y-Achse
offset_x = 0.0          #Offset der x-Achse in mm
offset_y = 0.0          #Offdet der y-Achse in mm

y_point = 0.0           #Startpunkt der y-Achse
x_point = 0.0           #Starpunkt der x-Achse
z_point = 0.0           #Startpunkt der z-Achse
res = max_width/stepwidth
#%% Kameraeinstellungen
macStr = "00:11:1C:F5:B9:88"
cam = photon.pyPFCam('C:/Users/project/Desktop/Projekt2025-Vermessung_von_Freiraumflaechen/Python_Scripts/pyPhotonFocus/pyPhotonFocusC/x64/Release')


def camsettings():
    cam.imageWidth = 2000
    cam.imageHeight = 2000
    cam.expTime = 10000.0 
    cam.blackLevel = 146.0
    cam.digitalOffset = 0
    cam.gain = 1.
    cam.setOffset(1000, 1000)
    cam.setPixelFormat('Mono8')
    

def grabBuffer():
    buffer = cam.getImage()
    #np.save('C:/Users/project/Desktop/Projekt2025-Vermessung_von_Freiraumflaechen/Bufferspeicher/buffer.npy',buffer)
    return buffer
#%% Auswertungseinstellungen

#%% Aufbauen der Matrix zur Auswertung

imageWidth = 25
imageHeight = 25
mx_a = 0    #Position image breite
mx_b = 0    #Position image höhe



vals = np.empty((imageHeight,imageWidth),dtype=object) #erst höhe dann breite der matrix
        

vals_z0 = np.empty_like(vals,dtype=object)          #Aufnehmen der Werte für z=0 Ebene
vals_z1 = np.empty_like(vals,dtype=object)          #Aufnehmen der Werte für z=1 Ebene
                                                    #Zum Abspeichern erst die Spalte und dann die Zeile angeben


#%% Aufbauen der Verbindung zu Achsencontroller und Kamera
try: 
    connection, axislist = xy.connect()
    wrapper.enable_all(connection)
    wrapper.set_custom_xy_origin(offset_x,offset_y,connection)
    xy.home(axislist)
    
except WrappedDllException as e:
        print(e.code, e.cause)

cam.connect(macStr)
cam.settings()

#%% Messung
input("Press Enter to start Measurement")
print("Starting Measurement")
while z_point == 0.0:
    z.achsez(z,z_point)
    try:
        while y_point <= max_width:
            wrapper.motion_move_abs(axislist[1],y_point,speed)                  #Fahren zum Ursprung der Achsen
            wrapper.motion_move_abs(axislist[0,x_point,speed0])                 #Fahren zum Ursprung der Achsen
            
            for point in range(0,(int(res+step_width))):                        #Verfahren der x-Achse und aufnehmen der Messung
                x_point = round(x_point + step_width,3)                         #Nächste Position der x-Achse
                wrapper.motion_move_abs(axislist[0],x_point,speed)              #Bewegen der x-Achse zu dieser Posisition
                x_pos,y_pos = xy.axis_pos(axislist)                             #Abfragen der aktuellen Achsenposition
                print("X-pos:",x_pos,"Y-pos:",y_pos)
                schwerpunkt = schwer.analysiere_schwerpunkt(Ixy=buffer)         #Platzhalter für Schwerpunktbestimmung des vorherigen Buffers
                schwerpunkt["cx_mm"],schwerpunkt["cx_mm"] = vals_z0[mx_a,mx_b]  #Platzhalter für das Spechern des Schwerpunktes in der Matrix
                buffer = grabBuffer()                                           #Aufnehmen des neuen Buffers
                mx_b = mx_b + 1
                
            y_point = y_point + stepwidth                                       #Nächste Posiotion der y-Achse
            mx_a = mx_a + 1
        else:               
            z_point = 1.0                                                       #Z-Achsen Position auf die nächste Ebene festlegen
            y_point = 0.0
            x_point = 0.0
    except WrappedDllException as e:
        print(e.code, e.cause)

while z_point == 1:
    z.achsez(z,z_point)
    mx_a = 0    #Position image breite
    mx_b = 0    #Position image höhe
    try:
        while y_point <= max_width:
            wrapper.motion_move_abs(axislist[1],y_point,speed)                  #Fahren zum Ursprung der Achsen
            wrapper.motion_move_abs(axislist[0,x_point,speed0])                 #Fahren zum Ursprung der Achsen
            
            for point in range(0,(int(res+step_width))):                        #Verfahren der x-Achse und aufnehmen der Messung
                x_point = round(x_point + step_width,3)                         #Nächste Position der x-Achse
                wrapper.motion_move_abs(axislist[0],x_point,speed)              #Bewegen der x-Achse zu dieser Posisition
                x_pos,y_pos = xy.axis_pos(axislist)                             #Abfragen der aktuellen Achsenposition
                print("X-pos:",x_pos,"Y-pos:",y_pos)
                schwerpunkt = schwer.analysiere_schwerpunkt(Ixy=buffer)         #Platzhalter für Schwerpunktbestimmung des vorherigen Buffers
                schwerpunkt["cx_mm"],schwerpunkt["cx_mm"] = vals_z1[mx_a,mx_b]  #Platzhalter für das Spechern des Schwerpunktes in der Matrix
                                                                                #Zum Abspeichern erst die Spalte und dann die Zeile angeben
                buffer = grabBuffer()                                           #Aufnehmen des neuen Buffers
                mx_b = mx_b + 1                                                 #Nächste Position in der Reihe der Matrix
                
            y_point = y_point + stepwidth                                       #Nächste Posiotion der y-Achse
            mx_a = mx_a + 1                                                     #Nächste Position in der Spalte der Matrix
        else:               
            z_point = 1                                                         #Z-Achsen Position auf die nächste Ebene festlegen
    except WrappedDllException as e:
        print(e.code, e.cause)
else:
     cam.disconnect()
     print("Messung beendet")
       
