from aerotech_native_datatypes import *


class Axis:
    """
    Class Axis handles an AeroTech Axis and correspondign data.

    Attributes:
        handles: the EnsembleHandles object for this axis
        mask: the axis mask used to address the axis in the AeroTech driver
        index: the index used to address the axis in the AeroTech driver
        name: A name given to the axis, use this to label it (e.g. 'x' or 'y')
        min: The smallest possible position
        max: The largest possible position
    """
    def __init__(self, handles: EnsembleHandles, mask: AXISMASK, axisindex: AXISINDEX, name: str, min: float, max: float, offset = 0.0):
        
        m = 2**axisindex.index.value
        assert m == mask.value.value, "mismatch between axismask and axisindex"

        self.handles = handles
        self.mask = mask
        self.index = axisindex
        self.name = name
        self.min = min
        self.max = max
        self.offset = offset

    def get_handles(self) -> EnsembleHandles:
        """
        Allows access to this axis' handles
        :return: the EnsembleHandles object this axis belongs to
        """
        return self.handles

    def get_mask(self) -> AXISMASK:
        """
        Allows access to the bitmask used to address this axis.
        :return:
        """
        return self.mask

    def get_index(self) -> AXISINDEX:
        return self.index

    def set_name(self, name:str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def get_min(self) -> float:
        return self.min

    def get_max(self) -> float:
        return self.max
    
    def get_offset(self) -> float:
        return self.offset

    def set_offset(self, new_offset : float) -> bool:
        self.offset = new_offset
        return True



    
class Connection:
    """
    Connection represents a connection to an Aerotech Controller
    """
    def __init__(self, handles: EnsembleHandles, mask: AXISMASK , axis_list : [Axis]):
        self.handles = handles
        self.mask = mask
        self.axis_list = axis_list
        
    def get_handles(self):
        return self.handles
    
    def get_mask(self):
        return self.mask
    
    def get_axis_list(self) -> [Axis]:
        return self.axis_list



