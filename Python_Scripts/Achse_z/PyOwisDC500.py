# -*- coding: utf-8 -*-
"""
@author: Jan Schulze
"""

import time
import pyvisa as visa


import pyvisa

# rm = pyvisa.ResourceManager()
# print(rm.list_resources())

# #Parameter
# Achse = 1
# Position = 0 # Zwischen 101 mm und 0 mm



class PyOwisDC500:
    """
    Made for Owis DC500 controller.\n
    Uses PyVISA v1.8 and time modules.\n
    """
    
    t = 0.05 # time to wait between commands to hardware
    spmm = 10000 # number of steps for 1 mm
    
    def __init__(self, axis = 2, interfaceID = 0, instrPA = 1):
        """
        Initialize connection with controller for one axis.\n
        Input:\n
            axis: which axis to use\n
            interfaceID: ID number of GPIB interface\n
            instrPA: primary address of instrument
        """
        self.rm = visa.ResourceManager()
        # get handle for axis
        self.handle = self.rm.open_resource('GPIB%i::%i::INSTR'\
        % (interfaceID, instrPA))
        time.sleep(self.t)
        self.axis = axis # save number of axis
    
    
    def write(self, command):
        """
        Sends command to controller and waits a moment.\n
        Input:\n
            command: command to send (string)
        """
        self.handle.write(command)
        time.sleep(self.t)
    
    
    def read(self):
        """
        Reads answer of the controller.\n
        Returns:\n
            ans: answer of controller. Should be a string.
        """
        ans = self.handle.read()
        
        return ans
    
    
    def reset(self):
        """
        Resets the controller and wait 2.5 s to initialize interface.
        """
        self.write('RESET')
        time.sleep(2.5)
    
    
    def getParam(self):
        """
        Gets current parameters of the controller.\n
        Returns:\n
            paramDict: dict with name + value of all the parameters
        """
        self.write('?P%i' %(self.axis)) # ask for parameters
        paramString = self.read()
        
        paramList = paramString.split('/') # split string into list
        
        # names of parameters
        name = ('axis', 'coordInputMode',\
        'AC', 'PVEL', 'Time', 'KD', 'KI', 'KP', 'IL')
        # initialize dict to save parameters in
        paramDict = {}
        # start with element 1 of paramList, because the first one is empty
        i = 1
        
        for element in name: # save parameter value for every name
            paramDict[element] = int(paramList[i])
            i = i + 1
        
        return paramDict
    
    
    def setParam(self, paramDict):
        """
        Sets parameters for the controller.\n
        Input:\n
            paramDict: dict of parameters, like returned by getParam()\n
                Easiest way to use this is to get paramDict from getParam(),
                modify it and use it in setParam()\n
                coordInputMode changes for all axes!
        """
        
        if len(paramDict) != 9:
            print ('Incorrect amount of parameters.')
            
        else:
            name = ('axis', 'coordInputMode',\
            'AC', 'PVEL', 'Time', 'KD', 'KP', 'KI', 'IL')
            
            string = '/' # string starts with /
            # names of parameters
            
            for element in name: # add value for every parameter to string
                string = string + str(paramDict[str(element)]) + '/'
                
            string = string + ';' # string has to end with ;
            
            self.write(string)
            # wait some more time because the string is so long
            time.sleep(5*self.t)
    
    
    def stop(self):
        """
        Stops movement of axis.
        """
        self.write('STOP')
    
    
    def refRun(self, mode = 4, wait = True):
        """
        Does a reference run.\n
        Input:\n
            mode (optional): int for type of reference run (default: 4):\n
                0: find next zero ref. pulse in positive direction and stay\n
                1: find and go to MINDEC\n
                2: find and go to MAXDEC\n
                3: find next zero ref. pulse (like type 0) and set
                position to 0\n
                4: go to MINDEC and find next zero ref. pulse from there,
                set position to 0\n
            wait (optional): if True, function will wait until axis is
            not moving anymore. Default: True
        """
        self.write('ENDS=%i%i' % (mode, self.axis))
        
        if wait: # wait until axis is not moving anymore
            # if axis is not moving anymore, positioning will be set to 0
            positioning = 1
            while positioning != str(0): # go on waiting until not moving
                time.sleep(1) # wait some time
                self.write('?M') # ask for movement status of all axes
                positioningString = self.read()
                
                i = 0
                for char in positioningString:  # iterate through string
                    i = i + 1
                    if i == self.axis: # save char for current axis ... 
                        positioning = char # ... as int
    
    
    def getPos(self):
        """
        Gets current position of axis in mm.\n
        Maximum accuracy of pos: 1e-4 mm\n
        Returns:\n
            pos: current position of axis in mm
        """
        
        self.write('?C%i' % (self.axis)) # get position ...
        pos = float(self.read()) / self.spmm # ... in mm
        
        return pos
    
    
    def areWeThereYet(self, pos, maxdelta = 0, ):
        """
        Waits until axis is close enough to set position.\n
        Input:\n
            pos : target position
            maxdelta (optional): maximum allowed difference between set
            and real position in mm. Default: 0\n
        Returns:\n
            posdelta: difference between set and real position
        """
        axis = PyOwisDC500(axis= 2, interfaceID=0, instrPA=1)
        wait = True
        waitagain = True
        
        timeout = 30  # Sekunden
        start = time.time()  # Startzeit VOR der Schleife!
        # wait until real position matches wanted position
            # with maximum difference of maxdelta
        while wait:     
            self.write('?E%i' % (self.axis)) # get position difference ...
            posdelta = float(self.read()) / self.spmm # ... in mm
            posdelta = axis.getPos() - pos
            print('posdelta:',posdelta)
            # posdelta = axis.getPos() - pos
            # print(f"posdelta: {posdelta}")
            # if abs(posdelta) <= 0.03:
            #     print("Zielposition erreicht.")
            #     break
            if  time.time() - start > timeout:
                raise TimeoutError("Timeout: Bewegung dauert zu lange – maxdelta zu klein?")
            time.sleep(0.1)

            if abs(posdelta) > maxdelta: # wait if difference is to big
                time.sleep(0.5)
                waitagain = True
                
            # delta should be small enough 2 times in a row
                # to avoid overshooting    
            elif waitagain:
                waitagain = False
                time.sleep(0.25)
                
            else: # stop waiting if difference is small enough
                wait = False
            

        
        return posdelta
    
    
    def moveAbs(self, pos, wait = True, maxdelta = 0):
        """
        Moves axis to absolute position. Optionally waits until position
        is reached.\n
        Maximum accuracy of pos and maxdelta: 1e-4 mm\n
        Input:\n
            pos: target position in mm\n
            wait (optional): if True, function will wait until axis is
            close enough to set position. Default: True\n
            maxdelta (optional): maximum allowed difference between set
            and real position in mm, only used if wait = True. Default: 0\n
        """
        start = time.time()
        
        self.write('ABSOL') # change to absolute positioning
        self.write('SET%i=%i' % (self.axis, pos * self.spmm)) # set position
        self.write('START%i' % (self.axis)) # start moving to position

        
        if wait:
            delta = self.areWeThereYet(pos, maxdelta)
            
            realpos = pos + delta
            usedtime = time.time() - start
            #print('Axis %.i : It took %.1f s to reach position at %.4f mm (set: %.4f mm).')(self.axis, usedtime, realpos, pos)
            print('Zeit:', usedtime)
            print('Zielposition:', pos)
            print('Reale Position:', realpos)
            
    
    
    def moveRel(self, pos, wait = True, maxdelta = 0):
        """
        Moves axis to relative position. Optionally waits until position
        is reached.\n
        Maximum accuracy of pos and maxdelta: 1e-4 mm\n
        Input:\n
            pos: target position in mm\n
            wait (optional): if True, function will wait until axis is 
            close enough to set position. Default: True\n
            maxdelta (optional): maximum allowed difference between set 
            and real position in mm, only used if wait = True. Default: 0\n
        """
        start = time.time()
        
        self.write('RELAT') # change to relative positioning
        self.write('SET%i=%i' % (self.axis, pos * self.spmm)) # set position
        self.write('START%i' % (self.axis)) # start moving to position
        
        if wait:
            delta = self.areWeThereYet(maxdelta)
            
            realpos = pos + delta
            usedtime = time.time() - start
            print('It took %.1f s to cover a distance of %.4f mm (set: %.4f mm).') % (usedtime, realpos, pos)
    
    
    def close(self):
        """
        Closes connection. Should be used after axis is not needed anymore.
        """
        print ('Connection to DC500 closed.')
        self.handle.close()
        self.rm.close()
        
##
def achsez(Achse, Position):
    try:
        rm = pyvisa.ResourceManager()
        print(rm.list_resources())
        # Schritt 1: Instanzerstellung (häufige Fehlerquelle)
        axis = PyOwisDC500(axis= Achse, interfaceID=0, instrPA=1)
        
        # Schritt 2: Controller-Reset mit Fehlerabfrage
        try:
            axis.reset()
        except Exception as e:
            print(f"Reset fehlgeschlagen: {e}")
    
        # # Schritt 4: Parameter setzen
        # params = {
        #     'axis': Achse,
        #     'coordInputMode': 0,
        #     'AC': 4000,
        #     'PVEL': 1065000,
        #     'Time': 0,
        #     'KD': 150,
        #     'KP': 100,
        #     'KI': 0,
        #     'IL': 100
        # }
        # axis.setParam(params)
        # print("Aktuelle Parameter:", params)
    
        # Schritt 5: Positionsbewegung mit Delta-Überprüfung
        try:
            axis.moveAbs(pos=Position, wait= True, maxdelta=0.03)
        except Exception as e:
            print(f"Bewegungsfehler: {e} - Sind Sie im OWIS-Hauptfenster?")
    except Exception as e:
        print(f"Anderer Fehler: {e}")
    finally:
        axis.close()


# # Schritt 1: Instanz erstellen (z.B. GPIB0::1::INSTR für InterfaceID=0, instrPA=1, Axis 1)
# axis = PyOwisDC500(axis=1, interfaceID=0, instrPA=1)

# # Schritt 2: Controller resetten (optional)
# axis.reset()

# # Schritt 3: Referenzfahrt durchführen
# #axis.refRun(mode=1, wait=True)

# #Schritt 4: Aktuelle Parameter abrufen
# params = {
#     'axis': 1,
#     'coordInputMode': 0,
#     #'currentPos': 0,
#     #'targetPos': 0,
#     'AC': 4000,     # Beschleunigung (Steps/s²)
#     'PVEL': 2065000,    # Geschwindigkeit (Steps/s)
#     'Time': 0,
#     'KD': 150,
#     'KP': 100,
#     'KI': 0,
#     'IL': 100,
#     #'FVEL': 0,
#     #'LVEL': 0
# }

# axis.setParam(params)

# print("Aktuelle Parameter:", params)

# # Schritt 5: Position setzen /(MAX:101,5862 mm | MAX: 0 mm)
# axis.moveAbs(pos= 101.0, wait=True, maxdelta = 1)

# # Schritt 6: Position ändern (z.B. +2 mm relativ)
# #axis.moveRel(pos=2.0, wait=True)

# # Schritt 7: Verbindung schließen
# axis.close()
