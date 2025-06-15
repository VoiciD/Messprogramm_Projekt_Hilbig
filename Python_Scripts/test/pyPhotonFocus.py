# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 17:00:27 2024

@author: David Hilbig
"""

#import numpy as np
import ctypes as c
from os import environ
from os.path import join, exists
import sys

# check for correct driver installation
if not 'PF_ROOT' in environ:
    raise Exception('Photon Focus driver installation not found.')
    
# create path to driver dlls string based on system environment variable 'PF_ROOT'
__pfBinPath = join(environ['PF_ROOT'],'PFSDK','bin')
__pfDblRatePath = join(environ['PF_ROOT'],'DoubleRateSDK','bin')

# add path of driver dlls to list of interpreter search directories
# has to be done after each kernel new start
if not __pfBinPath in sys.path:
    sys.path.append(__pfBinPath)
if sys.version_info >= (3,8): # for Python version >= 3.8
    from os import add_dll_directory
    add_dll_directory(__pfBinPath)
    add_dll_directory(__pfDblRatePath)

class pyPFCam():
    """
    Dll-wrapper object to access Photon Focus monochrome cameras. It uses an 
    accompanied dynamic-link-library `pyPhotonFocus.dll`.
    
    The path to this dll (without file name) can be given explicitly. 
    Otherwise, the predefined path 
    
    ./pyPhotonFocusC/x64/Release/
    
    will be used.
    
    The wrapper is build on PFSDK 2022.2.1. The corresponding version of the 
    drivers must be installed on the system. 

    Parameters
    ----------
    dll_path : str, optional
        (absolute or relative) path to the wrapper dll-file without 
        file name. The default is None.

    """
    
    # class local imports
    from numpy import empty, uint16
    
    # static attributes
    counter = 0  # number of active and connected cameras on system
    __dllPath = r'./pyPhotonFocusC/x64/Release/' # predefined path to wrapper dll
    __lib = None # ctypes windll-object for dll-function access

    def __init__(self,dll_path:str=None)-> None: 
        """
        Dll-wrapper object to access Photon Focus monochrome cameras. It uses an 
        accompanied dynamic-link-library `pyPhotonFocus.dll`.
        
        The path to this dll (without file name) can be given explicitly. 
        Otherwise, the predefined path 
        
        ./pyPhotonFocusC/x64/Release/
        
        will be used.
        
        The wrapper is build on PFSDK 2022.2.1. The corresponding version of the 
        drivers must be installed on the system. 

        Parameters
        ----------
        dll_path : str, optional
            (absolute or relative) path to the wrapper dll-file without 
            file name. The default is None.
        """
        self.__connected = False
        self.__width = 0
        self.__height = 0
        self.__address = ''
        self.__no = -1
        pyPFCam.__init_system(dll_path)
        
    def __del__(self):
        """ Ensure disconnect before delete"""
        self.disconnect()
        
    
    def __init_system(dll_path:str)-> bool:
        """
        Load wrapper dll globally for all pyPFCam instances as static attribute.
        Avoids reloading of the dll for every created instance. 

        Parameters
        ----------
        dll_path : str
            (absolute or relative) path to the wrapper dll-file without 
            file name. The default is None.

        Returns
        -------
        result : bool
            returns 'True' on success, 'False' otherwise

        """
        if pyPFCam.__lib == None: # if system is not initiated yet
            # initiate with...
            if dll_path: # given path
                path = dll_path
            else: # predefined path
               path = pyPFCam.__dllPath
               
            path = join(path, 'pyPhotonFocus.dll')
            if  not exists(path):
                print('[pyPFCam]: Error : Wrapper file cannot be found in this location.') 
                return False
            print('[pyPFCam]: Init system with wrapper library', path, end=' ... ')
            pyPFCam.__lib = c.windll.LoadLibrary(path)
            print('done')
            return True
    
    def connect(self, addressStr:str)-> bool:
        """
        Connect to a camera identified with the given address.
        
        Address can either be an IP4- or MAC-address. MAC-Address should be 
        preferred, as it does not change

        Parameters
        ----------
        addressStr : str
            IP4- or MAC-address of the device.

        Returns
        -------
        result : bool
            returns 'True' on success, 'False' otherwise
            
        Example
        -------
        Open a camera using a MAC-Address:
            
            >>> cam = pyPFCam()
            >>> cam.connect('00:11:1C:F5:B9:88')
            [pyPFCam]: Connecting to camera with MAC = 00:11:1C:F5:B9:88 ... done
            
        Open a camera using an IP-Address:
            
            >>> cam = pyPFCam()
            >>> cam.connect('169.254.128.169')
            [pyPFCam]: Connecting to camera with IP = 169.254.128.169 ... done
        """
        if self.__connected:
            print('[pyPFCam]: Warning: Camera already connected. Process aborted.')
            return True
        if pyPFCam.__lib == None:
            print('[pyPFCam]: Error: Wrapper system not initiated.')
            return False
            
        strBuf =c.create_string_buffer(addressStr.encode('utf-8'))
        if '.' in addressStr:# import as IP
            print('[pyPFCam]: Connecting to camera with IP =', addressStr, end=' ... ')
            ret = pyPFCam.__lib.connectIP(strBuf)
        if ':' in addressStr: # import as MAC
            print('[pyPFCam]: Connecting to camera with MAC =', addressStr, end=' ... ')
            ret = pyPFCam.__lib.connectMAC(strBuf)
        if ret != 0:
            print('\n[pyPFCam]: Error: Unable to connect to camera')
        else:
            if pyPFCam.__lib.isConnected():
                print('done')
                pyPFCam.counter += 1
                # set dynamic atributes
                self.__connected = True
                self.__width = self.getImageWidth()
                self.__height = self.getImageHeight()
                self.__address = addressStr
                self.__no = pyPFCam.counter
        return self.__connected
    
    def disconnect(self)-> bool:
        """
        Disconnect camera and free up resources bound by connection.
        
        Mandatory last step in camera communication.

        Returns
        -------
        result : bool
            returns 'True' on success, 'False' otherwise

        """
        if pyPFCam.__lib.isConnected():
            print('[pyPFCam]['+str(self.__no)+']: Disconnecting camera at '+self.__address, end=' ... ')
            pyPFCam.__lib.disconnect()
            if not pyPFCam.__lib.isConnected():
                self.__connected = False
                self.__width = 0
                self.__height = 0
                self.__address = ''
                self.__no = -1
                pyPFCam.counter -= 1
                print('done')
                return True
        return False
    
    def getImage(self):
        """
        Grab a single image from the camera and save the buffer data in a numpy 
        array.
            
        Parameters
        ----------
        None
        
        Returns
        -------
        buffer : ndarray
            image buffer data 
            
        Note
        ----
        The camera will be set to single frame acquisition mode

        """
        if self.__connected:
            try:
                buffer = pyPFCam.empty((self.__height, self.__width),dtype=pyPFCam.uint16)
                buffer_c = c.c_void_p(buffer.ctypes.data)
                pyPFCam.__lib.getImage(buffer_c)
            except:
                self.disconnect()
                raise
        else:
            return None
        return buffer
    
    def getImageAvg(self, nAvg:int=10):
        """
        Grab a single image from the camera and save the buffer data in a numpy 
        array.
        
        If nAvg > 1, the resulting image will be the average of several succeding
        images. 
        This increases the acquisition time per frame, but can be used to lower 
        the influence of noise.
            
        Parameters
        ----------
        nAvg : int, optional
            Number of images to average over. The default is 10.

        Returns
        -------
        buffer : ndarray
            image buffer data 
            
        Note
        ----
        The camera will be set to single frame acquisition mode

        """
        if self.__connected:
            try:
                nAvg = max(min(100, nAvg),1)
                print('[pyPFCam]['+str(self.__no)+']: Taking average of',nAvg,'images',end=' ... ')
                buffer = pyPFCam.empty((self.__height, self.__width),dtype=pyPFCam.uint16)
                buffer_c = c.c_void_p(buffer.ctypes.data)
                nAvg_c = c.c_int(nAvg)
                pyPFCam.__lib.getImageAvg(buffer_c, nAvg_c)
                print('done')
            except:
                self.disconnect()
                raise
        else:
            return None
        return buffer
    
    def saveImage(self, filePath:str) -> bool:
        """
        Grab a single image and save it to disk as *.png image file

        Parameters
        ----------
        filePath : str
            Complete path including directory and file name.
        """
        if self.__connected:
            try:
                # ensure proper file extension
                if filePath[-4:] != '.png':
                    filePath += '.png'
                # convert to: const char*
                strBuf =c.create_string_buffer(filePath.encode('utf-8'))
                if pyPFCam.__lib.saveImage(strBuf):
                    return False
                else:
                    print('[pyPFCam]['+str(self.__no)+']: Image saved as',filePath)
                    return True
            except:
                self.disconnect()
                raise
        else:
            return False
        
    def saveXML(self, filePath:str) -> bool:
        """
        Save complete XML data from camera to disk as text file

        Parameters
        ----------
        filePath : str
            Complete path including directory and file name.
        """
        if self.__connected:
            try:
                # ensure proper file extension
                if filePath[-4:] != '.txt':
                    filePath += '.txt'
                # convert to: const char*
                strBuf =c.create_string_buffer(filePath.encode('utf-8'))
                
                if pyPFCam.__lib.saveXMLFile(strBuf):
                    return False
                else:
                    print('[pyPFCam]['+str(self.__no)+']: XML-data saved as',filePath)
                    return True
            except:
                self.disconnect()
                raise
        else:
            return False
        
    def getCameraNo(self) -> int:
        return self.__no
    
    # camera property access methods ##########################################
    
    def getImageWidthMax(self) -> int:
        """
        Get maximum available image width value from camera

        Returns
        -------
        width : int 
            Maximum image width in px

        """  
        if self.__connected:
            try:
                value = -1
                value_c = c.c_int(value)
                pyPFCam.__lib.getIntProperty(b"WidthMax",c.byref(value_c))    
            except:
                self.disconnect()
                raise
            return value_c.value
        else:
            return -1
        
    def getImageHeightMax(self) -> int:
        """
        Get maximum available image height value from camera

        Returns
        -------
        height : int 
            Maximum image height in px

        """  
        if self.__connected:
            try:
                value = -1
                value_c = c.c_int(value)
                pyPFCam.__lib.getIntProperty(b"HeightMax",c.byref(value_c))    
            except:
                self.disconnect()
                raise
            return value_c.value
        else:
            return -1
    
    def getImageWidth(self) -> int:
        """
        Get currently set image width value from camera

        Returns
        -------
        width : int 
            Current image width in px

        """  
        if self.__connected:
            try:
                value = -1
                value_c = c.c_int(value)
                pyPFCam.__lib.getImageWidth(c.byref(value_c))    
            except:
                self.disconnect()
                raise
            return value_c.value
        else:
            return -1
    
    def setImageWidth(self, value:int) -> None:
        """
        Set active image width to given value in px.

        Parameters
        ----------
        value : int
            new image width in px

        Note
        ----
        Value will be automatically set within allowed range of minimum and 
        maximum as well as to the allowed increment step.

        """
        if self.__connected:
            try:
                value_c = c.c_int(value)
                pyPFCam.__lib.setImageWidth(value_c)
                self.__width = self.getImageWidth()
            except:
                self.disconnect()
                raise    
    
    def getImageHeight(self) -> int:
        """
        Get currently set image height value from camera

        Returns
        -------
        height : int 
            Current image height in px

        """
        if self.__connected:
            try:
                value = -1
                value_c = c.c_int(value)
                pyPFCam.__lib.getImageHeight(c.byref(value_c))
            except:
                self.disconnect()
                raise
            return value_c.value
        else:
            return -1
    
    def setImageHeight(self, value:int) -> None:
        """
        Set active image height to given value in px.

        Parameters
        ----------
        value : int
            new image height in px

        Note
        ----
        Value will be automatically set within allowed range of minimum and 
        maximum as well as to the allowed increment step.

        """
        if self.__connected:
            try:
                value_c = c.c_int(value)
                pyPFCam.__lib.setImageHeight(value_c)
                self.__height = self.getImageHeight()
            except:
                self.disconnect()
                raise
            
    def getDigitalOffset(self) -> int:
        """
        Get digital offset value from camera. This value is substracted as an 
        offset from the data and is typically negative.

        Returns
        -------
        value : int
            Actual digital offset value.

        """
        if self.__connected:
            try:
                value = -1
                value_c = c.c_int(value)
                pyPFCam.__lib.getDigitalOffset(c.byref(value_c))
            except:
                self.disconnect()
                raise
            return value_c.value
        else:
            return -1
    
    def setDigitalOffset(self, value:int) -> None:
        """
        Set digital offset value of camera. Value will be substracted as an 
        offset from the data and is typically negative.

        Parameters
        ----------
        value : int
            new digital offset value.

        Returns
        -------
        None.
        
        Note
        ----
        Value will be automatically set within allowed range of minimum and 
        maximum as well as to the allowed increment step.

        """
        if self.__connected:
            try:
                value_c = c.c_int(value)
                pyPFCam.__lib.setDigitalOffset(value_c)
                self.__height = self.getImageHeight()
            except:
                self.disconnect()
                raise
        
    def getExpTime(self) -> float:
        """
        Get exposure time value in microseconds from the camera. 

        Returns
        -------
        value : float
            Actual exposure time value in microseconds
            
        Note
        ----
        This is the open time of the camera in which it collects light for 
        one single frame. Increase value in lower light situations.
        """
        if self.__connected:
            try:
                value = -1.
                value_c = c.c_double(value)
                pyPFCam.__lib.getExpTime(c.byref(value_c))
            except:
                self.disconnect()
                raise
            return value_c.value
        else:
            return -1
    
    def setExpTime(self, value:float) -> None:
        """
        Set exposure time value of the camera. 

        Parameters
        ----------
        value : float
            new exposure time value in microseconds

        Returns
        -------
        None
        
        Note
        ----
        
        * Value will be automatically set within allowed range of minimum and maximum.
        * This sets the open time of the camera in which it collects light for one single frame. 
        * Increase value in lower light situations. 
        
        """
        if self.__connected:
            try:
                value_c = c.c_double(value)
                pyPFCam.__lib.setExpTime(value_c)
            except:
                self.disconnect()
                raise
        
    def getBlackLevel(self) -> float:
        """
        Get actual black level offset value from the camera.
        
        All digital values up to this threshold value will be set to black(value:0). 

        Returns
        -------
        value : float
            black level value.

        """
        if self.__connected:
            try:
                value = -1.
                value_c = c.c_double(value)
                pyPFCam.__lib.getBlackLevel(c.byref(value_c))
            except:
                self.disconnect()
                raise
            return value_c.value
        else:
            return -1
    
    def setBlackLevel(self, value:float) -> None:
        """
        Set black level offset value of the camera. 
        
        All digital values up to this threshold value will be set to black(value:0). 
        
        Use this value to suppress background noise.

        Parameters
        ----------
        value : float
            new black level value

        Returns
        -------
        result : bool
            returns 'True' on success, 'False' otherwise

        Note
        ----
        Value will be automatically set within allowed range of minimum and 
        maximum.
        """
        if self.__connected:
            try:
                value_c = c.c_double(value)
                if not pyPFCam.__lib.setBlackLevel(value_c):
                    return True
            except:
                self.disconnect()
                raise
        return False
    
    def getGain(self) -> float:
        """
        Get actual gain value from camera.
        
        Value represents amplification factor applied to the video signal.

        Returns
        -------
        gain : float
            Gain value

        """
        if self.__connected:
            try:
                value = -1.
                value_c = c.c_double(value)
                pyPFCam.__lib.getGain(c.byref(value_c))
            except:
                self.disconnect()
                raise
            return value_c.value
        else:
            return -1
    
    def setGain(self, value:float) -> None:
        """
        Set gain value to the camera.
        
        Controls the selected gain as an absolute physical value. 
        
        This is an amplification factor applied to the video signal. Typical
        range: [0.1 to 10.0]
        
        A value of gain = 1 will have no amplification.

        Parameters
        ----------
        value : float
            New gain value

        Returns
        -------
        result : bool
            returns 'True' on success, 'False' otherwise
        
        Note
        ----
        Value will be automatically set within allowed range of minimum and 
        maximum.
        """
        if self.__connected:
            try:
                value_c = c.c_double(value)
                if not pyPFCam.__lib.setGain(value_c):
                    return True
            except:
                self.disconnect()
                raise
        return False
     
    def setPixelFormat(self,formatStr: str='Mono8') -> bool:
        """
        Set pixel format in the camera. 
        
        Sets the digital format of each pixel in the image. Defines the used
        digital resolution for the conversion of analog camera values.
        
        The camera will be initiated with 'Mono8'.

        Parameters
        ----------
        formatStr : str
            String defining the digital pixel format
            
            Available formats depend on the support by the camera modell, 
            typical pixel format types are:
                
                * 'Mono8'
                * 'Mono10'
                * 'Mono10Packed'
                * 'Mono12'
                * 'Mono12Packed'
                * 'Mono16'
            
            The deafult is 'Mono8'.

        Returns
        -------
        result : bool
            returns 'True' on success, 'False' otherwise
            
        Note
        ----
        'Mono10Packed' and 'Mono12Packed' are according to GigE Vision 
        Specification 2.0, all others according to GenICam PFNC 1.1 

        """
        if self.__connected:
            try:
                strBuf =c.create_string_buffer(formatStr.encode('utf-8'))
                if not pyPFCam.__lib.setPixelFormat(strBuf):
                    return True
            except:
                self.disconnect()
                raise
        return False
    
    def setOffset(self, offsetX:int, offsetY:int) -> bool:
        """
        Set the start of region of interest (Top left corner)

        Parameters
        ----------
        offsetX : int
            New x-coordinate of region of interest
        offsetY : int
            New y-coordinate of region of interest

        Returns
        -------
        result : bool
            returns 'True' on success, 'False' otherwise

        """
        if self.__connected:
            if self.setOffsetX(offsetX):
                if self.setOffsetY(offsetY):
                    return True
        return False
    
    def setOffsetX(self, offsetX:int) -> bool:
        """
        Set the x-coordinate of the image offset relative to the sensor frame.
        This represents the start (top left corner) of the region of interest.

        Parameters
        ----------
        offsetX : int
            New x-coordinate of region of interest

        Returns
        -------
        result : bool
            returns 'True' on success, 'False' otherwise

        """
        if self.__connected:
            try:
                offsetX = max(offsetX,0)
                offsetX = min(self.getImageWidthMax() - self.__width, offsetX)
                offsetX_c = c.c_int(offsetX)
                if not pyPFCam.__lib.setIntProperty(b"OffsetX",offsetX_c):
                    return True
            except:
                self.disconnect()
                raise
        return False

    def getOffsetX(self) -> int:
        """
        Get actual x-coordinate of the image offset relative to the sensor frame.
        This represents the start (top left corner) of the region of interest.

        Returns
        -------
        gain : float
            x-coordinate of region of interest

        """
        if self.__connected:
            try:
                value = -1
                value_c = c.c_int(value)
                pyPFCam.__lib.getIntProperty(b"OffsetX", c.byref(value_c))
            except:
                self.disconnect()
                raise
            return value_c.value
        else:
            return -1
    
    def setOffsetY(self, offsetY:int) -> bool:
        """
        Set the y-coordinate of the image offset relative to the sensor frame.
        This represents the start (top left corner) of the region of interest.

        Parameters
        ----------
        offsetY : int
            New y-coordinate of region of interest

        Returns
        -------
        result : bool
            returns 'True' on success, 'False' otherwise

        """
        if self.__connected:
            try:
                offsetY = max(offsetY,0) # auto minimum 0
                offsetY = min(self.getImageHeightMax() - self.__height, offsetY)
                offsetY_c = c.c_int(offsetY)
                if not pyPFCam.__lib.setIntProperty(b"OffsetY",offsetY_c):
                    return True
            except:
                self.disconnect()
                raise
        return False
    
    def getOffsetY(self) -> int:
        """
        Get actual y-coordinate of the image offset relative to the sensor frame.
        This represents the start (top left corner) of the region of interest.

        Returns
        -------
        gain : float
            y-coordinate of region of interest

        """
        if self.__connected:
            try:
                value = -1
                value_c = c.c_int(value)
                pyPFCam.__lib.getIntProperty(b"OffsetY", c.byref(value_c))
            except:
                self.disconnect()
                raise
            return value_c.value
        else:
            return -1
        
    # properties for easier dynamic like member access ########################
    
    blackLevel = property(getBlackLevel, setBlackLevel, doc='Black Level')
    digitalOffset = property(getDigitalOffset, setDigitalOffset, doc='Digital Offset')
    expTime = property(getExpTime, setExpTime, doc='Exposure Time')
    gain = property(getGain, setGain, doc='Gain')
    imageWidth = property(getImageWidth, setImageWidth, doc='Image Width')
    imageHeight = property(getImageHeight, setImageHeight, doc='Image Height')
    no = property(getCameraNo,doc='Camera Number')
    offsetX = property(getOffsetX, setOffsetX, doc='X-Offset')
    offsetY = property(getOffsetY, setOffsetY, doc='Y-Offset')
    
    # magic methods ###########################################################
    
    def __str__(self):
        if self.__connected:
           outStr = 'pyPhotonFocus-Camera Wrapper Object connected to camera at '
           +self.__address
        else:
            outStr = 'pyPhotonFocus-Camera Wrapper Object currently not connected to any camera'    
        return outStr


#%% main
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    from os.path import expanduser
    
    macStr = "00:11:1C:F5:B9:88" # MV1-D2080-160-G2-12 fully housed
    #macStr= '00:11:1C:F9:5C:D0' # OEM + Ethalon
    
    # init camera system
    cam = pyPFCam('C:/Users/project/Desktop/Projekt2025-Vermessung_von_Freiraumflaechen/Python_Scripts/pyPhotonFocus/pyPhotonFocusC/x64/Release')
    
    # connect to camera
    if cam.connect(macStr):
        # set camera parameters
        cam.imageWidth = 1280
        cam.imageHeight = 720
        cam.expTime = 10000.0 
        cam.blackLevel = 146.0
        cam.digitalOffset = 0
        cam.gain = 1.
        cam.setOffset(1000, 1000)
        cam.setPixelFormat('Mono8')
        
        # print out camera parameters
        print('camera number:',cam.no)
        print('image width =',cam.imageWidth)
        print('image height =',cam.imageHeight)
        print('exposure time =', cam.expTime)
        print('black level =', cam.blackLevel)
        print('digital offset =', cam.digitalOffset)
        print('gain =', cam.gain)
        print('x-offset = ',cam.offsetX)
        print('y-offset = ',cam.offsetY)
        
        # grab an image
        buffer = cam.getImage()
        np.save('C:/Users/project/Desktop/Projekt2025-Vermessung_von_Freiraumflaechen/Bufferspeicher/buffer.npy',buffer)
        # save image to user desktop
        #cam.saveImage(expanduser('~\\Desktop\\') + 'image')
        
        # disconnect
        cam.disconnect()
       
        # show buffer data as gray level image
        plt.figure(1, clear=True)
        plt.imshow(buffer,cmap='gray')
           