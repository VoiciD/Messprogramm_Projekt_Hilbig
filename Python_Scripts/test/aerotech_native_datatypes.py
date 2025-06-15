from ctypes import *


class EnsembleHandle:
    def __init__(self):
        self.void_pointer = c_void_p()
    
class EnsembleHandles:
    def __init__(self, handle: EnsembleHandle):
        self.pointer = pointer(handle.void_pointer)

    def get_handle(self):
        return self.pointer
    

class HANDLECOUNT:
    def __init__(self, value):
        self.value = c_int(value)


class AXISINDEX:
    def __init__(self, index):
        self.index = c_int(index)



class ONOFF:
    pass


class WAITTYPE:
    pass


class WAITOPTION:
    pass


class c_time_t:
    pass


class EnsembleParameterFile:
    pass


class PARAMETERID:
    pass


class AXISMASK:
    def __init__(self, value):
        self.value = c_int(value)


class RESETPROGRAMM:
    def __init__(self, value: bool):
        self.reset = c_bool(value)

    def get_reset(self):
        return self.reset


class ETHERNETSTATUS:
    pass

class MODETYPE:
    pass

class STATUSITEM:
    pass



