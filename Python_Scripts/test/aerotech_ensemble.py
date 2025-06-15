from ctypes.wintypes import *

from aerotech_native_datatypes import *
from aerotech_dictonaries import *

library = cdll.LoadLibrary(r"C:\Program Files (x86)\Aerotech\Ensemble\CLibrary\Bin64\EnsembleC64.dll")


def init(path: str) -> bool:
    """
    Attempts to load the DLL described by the given path, must be EnsembleC64.dll for the wrapper to function.
    :param path: the DLL path
    :return: True if the DLL was loaded, False otherwise
    """
    global library
    try:
        library = cdll.LoadLibrary(path)
    except Exception as e:
        print(e)
        return False
    return True


###################################################################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Connection Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###################################################################################

# EnsembleConnect
def EnsembleConnect(handles : EnsembleHandles, handle_count: HANDLECOUNT) -> c_bool:
    """
    Connects to all Ensembles.

    :param handles: EnsembleHandle pointer array
    :param handle_count: DWORD pointer
    :return: bool
    """

    result = library.EnsembleConnect(byref(handles.get_handle()), byref(handle_count.value))

    return result


# EnsembleDisconnect
def EnsembleDisconnect(handle: EnsembleHandle) -> c_bool:
    """
    Disconnects from all the Ensembles.

    :param handle: EnsembleHandle pointer array
    :return: bool
    """
    return library.EnsembleDisconnect(handle)


# EnsembleReset
def EnsembleReset(handle: EnsembleHandle, restart_programs: RESETPROGRAMM) -> c_bool:
    """
    Resets the Ensemble.

    :param restart_programs:
    :param handle: EnsembleHandle
    :return: bool
    """
    return library.EnsembleReset(handle, restart_programs.get_reset())


# EnsembleGetLastError
def EnsembleGetLastError() -> (int, str):
    """

    :return: error code, error message
    """
    result = library.EnsembleGetLastError()
    return result, error_dict[result]



###################################################################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Motion Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###################################################################################


def EnsembleMotionDisable(handle: EnsembleHandle, axis_mask: AXISMASK) -> c_bool:
    """
    Disables the axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :return: bool
    """
    return library.EnsembleMotionDisable(handle, axis_mask)


def EnsembleMotionEnable(handle: EnsembleHandle, axis_mask: AXISMASK) -> c_bool:
    """
    Enables the axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :return: bool
    """
    return library.EnsembleMotionEnable(handle, axis_mask)


def EnsembleMotionFaultAck(handle: EnsembleHandle, axis_mask: AXISMASK) -> c_bool:
    """
    Acknowledges and clears the fault on axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :return: bool
    """
    return library.EnsembleMotionFaultAck(handle, axis_mask)


def EnsembleMotionFreeRun(handle: EnsembleHandle, axis_mask: AXISMASK, speed: c_double) -> c_bool:
    """
    Freeruns the axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :param speed: float
    :return: bool
    """
    pass


def EnsembleMotionFreeRunStop(handle: EnsembleHandle, axis_mask: AXISMASK) -> c_bool:
    """
    Freeruns the axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :return: bool
    """
    pass


def EnsembleMotionHome(handle: EnsembleHandle, axis_mask: AXISMASK) -> c_bool:
    """
    Homes the axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :return: bool
    """
    return library.EnsembleMotionHome(handle,axis_mask)


def EnsembleMotionHomeConditional(handle: EnsembleHandle, axis_mask: AXISMASK) -> c_bool:
    """
    Homes the axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :return: bool
    """
    pass


def EnsembleMotionLinear(handle: EnsembleHandle, axis_mask: AXISMASK, distance: c_double,
                         coordinated_speed: c_double) -> c_bool:
    """
    Executes a linear move on axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :param distance: float pointer
    :param coordinated_speed: float
    :return: bool
    """
    pass


def EnsembleMotionMoveInc(handle: EnsembleHandle, axis_mask: AXISMASK, distance: c_double, speed: c_double) -> c_bool:
    """
    Executes an incremental move on axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :param distance: c_double
    :param speed: c_double
    :return: bool
    """
    return library.EnsembleMotionMoveInc(handle, axis_mask, byref(distance), byref(speed))


def EnsembleMotionMoveAbs(handle: EnsembleHandle, axis_mask: AXISMASK, distance: c_double, speed: c_double) -> c_bool:
    """
    Executes an absolute move on axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :param distance: c_double
    :param speed: c_double
    :return: bool
    """
    return library.EnsembleMotionMoveAbs(handle, axis_mask, byref(distance), byref(speed))


def EnsembleMotionBlockMotion(handle: EnsembleHandle, axis_mask: AXISMASK, on_off: ONOFF) -> c_bool:
    """
    Sets motion blocking to On or OFF.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :param on_off: ONOFF
    :return: bool
    """
    pass


def EnsembleMotionAutoFocus(handle: EnsembleHandle, axis_mask: AXISMASK, on_off: ONOFF) -> c_bool:
    """
    Turns on or turns off autofocus.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :param on_off: ONOFF
    :return: bool
    """
    pass


def EnsembleMotionCWRadius(handle: EnsembleHandle, axis1: AXISINDEX, axis1_end: c_double, axis2: AXISINDEX,
                           axis2_end: c_double, radius: c_double, coordinated_speed: c_double) -> c_bool:
    """
    Executes a clockwise circular move on axes.

    :param handle: EnsembleHandle
    :param axis1: AXISINDEX
    :param axis1_end: float
    :param axis2: AXISINDEX
    :param axis2_end: float
    :param radius: float
    :param coordinated_speed: float
    :return: bool
    """
    pass


def EnsembleMotionCWCenter(handle: EnsembleHandle, axis1: AXISINDEX, axis1_end: c_double, axis2: AXISINDEX,
                           axis2_end: c_double, axis1_center: c_double, axis2_center: c_double,
                           coordinated_speed: c_double) -> c_bool:
    """
    Executes a clockwise circular move on axes.

    :param handle: EnsembleHandle
    :param axis1: AXISINDEX
    :param axis1_end: float
    :param axis2: AXISINDEX
    :param axis2_end: float
    :param axis1_center: float
    :param axis2_center: float
    :param coordinated_speed: float
    :return: bool
    """
    pass


def EnsembleMotionCCWRadius(handle: EnsembleHandle, axis1: AXISINDEX, axis1_end: c_double, axis2: AXISINDEX,
                            axis2_end: c_double, radius: c_double, coordinated_speed: c_double) -> c_bool:
    """
    Executes a counterclockwise circular move on axes.

    :param handle: EnsembleHandle
    :param axis1: AXISINDEX
    :param axis1_end: float
    :param axis2: AXISINDEX
    :param axis2_end: float
    :param radius: float
    :param coordinated_speed: float
    :return: bool
    """
    pass


def EnsembleMotionCCWCenter(handle: EnsembleHandle, axis1: AXISINDEX, axis1_end: c_double, axis2: AXISINDEX,
                            axis2_end: c_double, axis1_center: c_double, axis2_center: c_double,
                            coordinated_speed: c_double) -> c_bool:
    """
    Executes a counterclockwise circular move on axes.

    :param handle: EnsembleHandle
    :param axis1: AXISINDEX
    :param axis1_end: float
    :param axis2: AXISINDEX
    :param axis2_end: float
    :param axis1_center: float
    :param axis2_center: float
    :param coordinated_speed: float
    :return: bool
    """
    pass


def EnsembleMotionHalt(handle: EnsembleHandle) -> c_bool:
    """
    Halts the vector motion queue and prevents motion from starting.

    :param handle: EnsembleHandle
    :return: bool
    """
    pass


def EnsembleMotionStart(handle: EnsembleHandle) -> c_bool:
    """
    Starts execution of the vector motion queue.

    :param handle: EnsembleHandle
    :return: bool
    """
    pass


def EnsembleMotionWaitMode(handle: EnsembleHandle, wait_type: WAITTYPE) -> c_bool:
    """
    Sets the mode of wait of a task.

    :param handle: EnsembleHandle
    :param wait_type: WAITTYPE
    :return: bool
    """
    pass


def EnsembleMotionAbort(handle: EnsembleHandle, axis_mask: AXISMASK) -> c_bool:
    """
    Aborts motion on given axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :return: bool
    """
    pass


def EnsembleMotionWaitForMotionDone(handle: EnsembleHandle, axis_mask: AXISMASK, wait_option: WAITOPTION,
                                    timeout: DWORD, timed_out: c_bool) -> c_bool:
    """
    Waits for motion to be done on given axes.

    :param handle: EnsembleHandle
    :param axis_mask: AXISMASK
    :param wait_option: WAITOPTION
    :param timeout: DWORD
    :param timed_out: bool pointer
    :return: bool
    """
    pass






###################################################################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Parameter Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###################################################################################

def EnsembleParameterGetValue(handle: EnsembleHandle, parameter_id: PARAMETERID, index: DWORD,
                              value: c_double) -> c_bool:
    """
    Retrieves the value of a double parameter from the drive.

    :param handle: EnsembleHandle
    :param parameter_id: PARAMETERID
    :param index: DWORD
    :param value: float pointer
    :return: bool
    """
    pass


def EnsembleParameterGetValueString(handle: EnsembleHandle, parameter_id: PARAMETERID, index: DWORD, size: ULONG,
                                    value: LPSTR) -> c_bool:
    """
    Retrieves the value of a string parameter from the drive.

    :param handle: EnsembleHandle
    :param parameter_id: PARAMETERID
    :param index: DWORD
    :param size: ULONG
    :param value: char pointer
    :return: bool
    """
    pass


def EnsembleParameterSetValue(handle: EnsembleHandle, parameter_id: PARAMETERID, index: DWORD,
                              value: c_double) -> c_bool:
    """
    Sends the value of a double parameter to the drive.

    :param handle: EnsembleHandle
    :param parameter_id: PARAMETERID
    :param index: int
    :param value: c_double
    :return: bool
    """
    pass


def EnsembleParameterSetValueString(handle: EnsembleHandle, parameter_id: PARAMETERID, index: DOUBLE,
                                    value: LPCSTR) -> c_bool:
    """
    Sends the value of a string parameter to the drive.

    :param handle: EnsembleHandle
    :param parameter_id: PARAMETERID
    :param index: DOUBLE
    :param value: LPCSTR
    :return: bool
    """
    pass


def EnsembleParameterCommit(handle: EnsembleHandle) -> c_bool:
    """
    Commits parameters on the controller.

    :param handle: EnsembleHandle
    :return: bool
    """
    pass


def EnsembleParameterFileGetDefaults(param_file: EnsembleParameterFile) -> c_bool:
    """
    Gets the default parameter file.

    :param param_file: EnsembleParameterFile
    :return: bool
    """
    pass


def EnsembleParameterFileOpen(file_name: LPCSTR, param_file: EnsembleParameterFile) -> c_bool:
    """
    Opens the parameter file.

    :param file_name: LPCSTR
    :param param_file: EnsembleParameterFile
    :return: bool
    """
    pass


def EnsembleParameterFileClose(param_file: EnsembleParameterFile) -> c_bool:
    """
    Closes the parameter file.

    :param param_file: EnsembleParameterFile
    :return: bool
    """
    pass


def EnsembleParameterFileSave(param_file: EnsembleParameterFile, file_name: LPCSTR) -> c_bool:
    """
    Saves the parameter file.

    :param param_file: EnsembleParameterFile
    :param file_name: LPCSTR
    :return: bool
    """
    pass


def EnsembleParameterFileGetValueString(param_file: EnsembleParameterFile, parameter_id: PARAMETERID, index: DWORD,
                                        value: LPSTR, value_size: DWORD) -> c_bool:
    """
    Retrieves the value of a string parameter from the parameter file.

    :param param_file: EnsembleParameterFile
    :param parameter_id: PARAMETERID
    :param index: DWORD
    :param value: LPCSTR
    :param value_size: DWORD
    :return: bool
    """
    pass


def EnsembleParameterFileGetValue(param_file: EnsembleParameterFile, parameter_id: PARAMETERID, index: DWORD,
                                  value: c_double) -> c_bool:
    """
    Gets the value of a double parameter from the parameter file.

    :param param_file: EnsembleParameterFile
    :param parameter_id: PARAMETERID
    :param index: DWORD
    :param value: double pointer
    :return: bool
    """
    pass


def EnsembleParameterFileSetValueString(param_file: EnsembleParameterFile, parameter_id: PARAMETERID, index: DWORD,
                                        value: LPCSTR) -> c_bool:
    """
    Sends the value of a string parameter to the parameter file.

    :param param_file: EnsembleParameterFile
    :param parameter_id: PARAMETERID
    :param index: DWORD
    :param value: LPCSTR
    :return: bool
    """
    pass


def EnsembleParameterFileSetValue(param_file: EnsembleParameterFile, parameter_id: PARAMETERID, index: DWORD,
                                  value: c_double) -> c_bool:
    """
    Sets the value of a double parameter to the parameter file.

    :param param_file: EnsembleParameterFile
    :param parameter_id: PARAMETERID
    :param index: DWORD
    :param value: c_double
    :return: bool
    """
    pass


def EnsembleParameterFileGetData(param_file: EnsembleParameterFile, section: LPCSTR, data: LPSTR,
                                 data_size: DWORD) -> c_bool:
    """
    Provides access to the user-customizable tag in the configuration file.

    :param param_file: EnsembleParameterFile
    :param section: LPCSTR
    :param data: LPSTR
    :param data_size: DWORD
    :return: bool
    """
    pass


def EnsembleParameterFileSetData(param_file: EnsembleParameterFile, data: LPCSTR) -> c_bool:
    """
    Provides access to the user-customizable tag in the configuration file.

    :param param_file: EnsembleParameterFile
    :param data: LPCSTR
    :return: bool
    """
    pass


def EnsembleParameterFileGetAxisMask(param_file: EnsembleParameterFile, axis_mask: AXISMASK) -> c_bool:
    """
    Gets the existing axis mask from the parameter file.

    :param param_file: EnsembleParameterFile
    :param axis_mask: AXISMASK
    :return: bool
    """
    pass


def EnsembleParameterFileSetAxisMask(param_file: EnsembleParameterFile, axis_mask: AXISMASK) -> c_bool:
    """
    Sets the existing axis mask in the parameter file.

    :param param_file: EnsembleParameterFile
    :param axis_mask: AXISMASK
    :return: bool
    """
    pass


def EnsembleParameterSendToController(handle: EnsembleHandle, param_file: EnsembleParameterFile) -> c_bool:
    """
    Sends the specified parameter file to the controller.

    :param handle: EnsembleHandle
    :param param_file: EnsembleParameterFile
    :return: bool
    """
    pass


def EnsembleParameterRetrieveFromController(handle: EnsembleHandle, param_file: EnsembleParameterFile) -> c_bool:
    """
    Retrieves the parameters and writes them to the specified file.

    :param handle: EnsembleHandle
    :param param_file: EnsembleParameterFile
    :return: bool
    """
    pass


def EnsembleInformationGetAxisMask(handle: EnsembleHandle, axisMask: AXISMASK) -> c_bool:
    """
    :param handle: EnsembleHandle
    :param axisMask: AXISMASK
    :return: bool
    """
    return library.EnsembleInformationGetAxisMask(handle,byref(axisMask))



###################################################################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Status Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###################################################################################



def EnsembleStatusPositionMarkerLatched(handle: EnsembleHandle, axis: AXISINDEX, return_value: c_double) -> c_bool:
    """
    Gets the position feedback latched when the marker signal occurred during a home.

    :param handle: EnsembleHandle
    :param axis: AXISINDEX
    :param return_value: c_double
    :return: BOOL
    """
    pass

def EnsembleStatusEtherStatus(handle: EnsembleHandle, return_value: ETHERNETSTATUS) -> c_bool:
    """
    Gets the Ethernet status.

    :param handle: EnsembleHandle
    :param return_value: ETHERNETSTATUS
    :return: BOOL
    """
    pass

def EnsembleStatusGetMode(handle: EnsembleHandle, modeType: MODETYPE, returnValue: c_double) -> c_bool:
    """
    Gets the setting of one of the modal variables.

    :param handle: EnsembleHandle
    :param modeType: MODETYPE
    :param returnValue: DOUBLE
    :return: BOOL
    """
    pass

def EnsembleStatusGetItems(handle: EnsembleHandle, axisIndex: AXISINDEX, numberOfItems: DWORD, itemCodeArray: STATUSITEM, itemValuesArray: c_double ) -> c_bool:
    """
    Retrieves multiple status items from the Ensemble.

    :param handle: EnsembleHandle
    :param axisIndex: AXISINDEX
    :param numberOfItems: DWORD
    :param itemCodeArray: STATUSITEM array pointer
    :param itemValuesArray: c_double array pointer
    :return: BOOL
    """
    pass

def EnsembleStatusGetItem(handle: EnsembleHandle, axisIndex: AXISINDEX, itemCode: STATUSITEM, itemValue : c_double) -> c_bool:
    """
    Retrieves a single status item from the Ensemble.

    :param handle: EnsembleHandle
    :param axisIndex: AXISINDEX
    :param itemCode: STATUSITEM
    :param itemValue: DOUBLE pointer
    :return: BOOL
    """
    return library.EnsembleStatusGetItem(handle, axisIndex, itemCode, byref(itemValue))