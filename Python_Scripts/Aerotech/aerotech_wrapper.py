
from aerotech_ensemble import *

from aerotech_datatypes import *
from aerotech_dictonaries import status_items
from aerotech_exceptions import AxisCallException, ConnectionException, WrappedDllException


def connect() -> Connection:
    """
    Connects to the Axis controller
    :raises: ConnectionException if it can't connect to the axis controller
    :return: a Connection object to interact with the controller
    """
    handle = EnsembleHandle()
    handles = EnsembleHandles(handle)
    count = HANDLECOUNT(0)
    res = EnsembleConnect(handles, count)

    if not res:
        code, name = EnsembleGetLastError()
        raise ConnectionException(code,"Error in DLL while trying to connect")

    try:
        assert count.value.value == 1, "HandleCount is not 1"
    except AssertionError as e:
        raise ConnectionException(202, str(e))

    axismask = AXISMASK(0)

    res = EnsembleInformationGetAxisMask(handles.get_handle().contents, axismask.value)

    if not res:
        code, name = EnsembleGetLastError()
        raise ConnectionException(code,"Error in DLL while trying to get axis mask")

    axis_list = []   #dont do axis_list = [Axis] -> [class, Axis, Axis]

    # find used axis masks, append Axis for found masks to axis_list
    for i in range(0,10):
        m = 2**i
        if m & axismask.value.value:
            axis_list.append(Axis(handles,AXISMASK(m),AXISINDEX(i),str(i),0.0,0.0))

    connection = Connection(handles, axismask, axis_list)
    return connection


def disconnect(connection: Connection) -> bool:
    """
    Disconnects from the controller, ending the connection
    :raises: AxisCallException if the provided connection parameter is not of Type Connection
    :raises: WrappedDllError on error during command execution
    :return: True if successful
    """

    try:
        assert type(connection) == Connection, "parameter connection is not of type Connection"
    except AssertionError as e:
        raise AxisCallException(201,str(e))

    res = EnsembleDisconnect(connection.get_handles().get_handle().contents)
    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)

    return res


def acknowledge_errors(connection: Connection) -> bool:
    """
    Acknowledges errors that occurred in the axis controller.
    :raises: AxisCallException if the provided connection parameter is not of Type Connection
    :raises: WrappedDllError if an error occurs during execution
    :return: True if successful
    """

    try:
        assert type(connection) == Connection, "parameter connection is not of type Connection"
    except AssertionError as e:
        raise AxisCallException(201,str(e))

    res = EnsembleMotionFaultAck(connection.get_handles().get_handle().contents, connection.get_mask().value)

    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)

    return res


def reset(connection : Connection) -> bool:
    """
    resets the controller the connection corresponds to
    :param connection: the Connection object for the controller that is reset
    :raises: AxisCallException if the provided connection parameter is not of Type Connection
    :raises: WrappedDllError if an error occurs during execution
    :return: True if successful
    """

    try:
        assert type(connection) == Connection, "parameter connection is not of type Connection"
    except AssertionError as e:
        raise AxisCallException(201,str(e))

    res = EnsembleReset(connection.get_handles().get_handle().contents, RESETPROGRAMM(True))

    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)

    return res


def home_axis(axis : Axis):
    """
    Homes the axis corresponding to the Axis object.
    :raises: AxisCallException if the provided axis parameter is not of Type Axis
    :raises: WrappedDllError if an error occurs during execution
    :return: True if successful
    """

    try:
        assert type(axis) == Axis, "parameter axis is not of type Axis"
    except AssertionError as e:
        raise AxisCallException(201,str(e))

    res = EnsembleMotionHome(axis.get_handles().get_handle().contents, axis.get_mask().value)

    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)

    return res


def enable_all(connection : Connection) -> bool:
    """
        Enables all axis in a Connection
        :param connection: the Connection object for which the axis are enabled
        :raises: AxisCallException if the provided connection parameter is not of Type Connection
        :raises: WrappedDllError if an error occurs during execution
        :return: True if successful
        """

    try:
        assert type(connection) == Connection, "parameter connection is not of type Connection"
    except AssertionError as e:
        raise AxisCallException(201, str(e))


    res =  EnsembleMotionEnable(connection.get_handles().get_handle().contents, connection.get_mask().value)

    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)

    return res


def enable_axis(axis : Axis) -> bool:
    """
        Enables the axis
        :param axis: the Axis that is enabled
        :raises: AxisCallException if the provided axis parameter is not of Type Axis
        :raises: WrappedDllError if an error occurs during execution
        :return: True if successful
        """

    try:
        assert type(axis) == Axis, "parameter axis is not of type Axis"
    except AssertionError as e:
        raise AxisCallException(201, str(e))

    res =  EnsembleMotionEnable(axis.get_handles().get_handle().contents, axis.get_mask().value)

    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)

    return res


def disable_all(connection : Connection) -> bool:
    """
        Disables all axes in a Connection
        :param connection: the Connection object for which all axes are disabled
        :raises: AxisCallException if the provided connection parameter is not of Type Connection
        :raises: WrappedDllError if an error occurs during execution
        :return: True if successful
        """

    try:
        assert type(connection) == Connection, "parameter connection is not of type Connection"
    except AssertionError as e:
        raise AxisCallException(201, str(e))

    res =  EnsembleMotionDisable(connection.get_handles().get_handle().contents, connection.get_mask().value)

    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)

    return res


def disable_axis(axis : Axis) -> bool:
    """
            Disables one axis
            :param axis: the Axis that is enabled
            :raises: AxisCallException if the provided axis parameter is not of Type Axis
            :raises: WrappedDllError if an error occurs during execution
            :return: True if successful
            """

    try:
        assert type(axis) == Axis, "parameter axis is not of type Axis"
    except AssertionError as e:
        raise AxisCallException(201, str(e))

    res =  EnsembleMotionDisable(axis.get_handles().get_handle().contents, axis.get_mask().value)

    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)

    return res


def position_info(axis : Axis, include_offset = False) -> int:
    """
    Gets the current postion of an axis, either absolute or including the set offset.
    :param axis: the axis for which the position is read
    :param include_offset: whether to include the set offset in the position or not
    :raises:
    :raises: WrappedDllError if an error occurs during execution
    :return: the position relative to the axis' point of origin in mm
    """

    try:
        assert type(axis) == Axis, "axis is not of type Axis"
        assert type(include_offset) == bool, "include_offset is not of type bool"
    except AssertionError as e:
        raise AxisCallException(201,str(e))

    item_code = c_int(status_items["STATUSITEM_PositionFeedback"])
    position = c_double(0.0)
    res = EnsembleStatusGetItem(axis.get_handles().get_handle().contents, axis.get_index().index, item_code, position)

    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)
    
    if include_offset:
        return position.value - axis.get_offset()
        
    return position.value


def motion_move_inc(axis: Axis, distance: float, speed = 10.0) -> bool:
    """
    Moves the axis by the given distance with the given speed.
    :param axis: the Axis to move
    :param distance: the distance by which to move the axis
    :param speed: the speed with which to move the axis, default 10.0
    :raises: AxisCallException if one of the parameters is of the wrong type
    :raises: WrappedDllError if an error occurs during execution
    :return: True if the function finishes successful
    """

    try:
        assert type(axis) == Axis, "axis is not of type axis"
        assert type(distance) == float, "distance is not of type float"
        assert type(speed) == float, "speed is not of type float"
    except AssertionError as e:
        raise AxisCallException(201,str(e))

    res = EnsembleMotionMoveInc(axis.get_handles().get_handle().contents, axis.mask.value, c_double(distance), c_double(speed))

    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)

    return res


def motion_move_abs(axis: Axis, target: float, speed=10.0) -> bool:
    """
    Moves the axis to the given position with the given speed.
    :param axis: the Axis to move
    :param target: the target position to which to move the axis
    :param speed: the speed with which to move the axis, default 10.0
    :raises: AxisCallException if one of the parameters is of the wrong type
    :raises: WrappedDllError if an error occurs during execution
    :return: True if the function finishes successful
    """

    try:
        assert type(axis) == Axis, "axis is not of type axis"
        assert type(target) == float, "target is not of type float"
        assert type(speed) == float, "speed is not of type float"
    except AssertionError as e:
        raise AxisCallException(201,str(e))

    target += axis.get_offset()
    res = EnsembleMotionMoveAbs(axis.get_handles().get_handle().contents, axis.mask.value, c_double(target), c_double(speed))

    if not res:
        code, msg = EnsembleGetLastError()
        raise WrappedDllException(code, msg)

    return res


def check_axis_mask(axis_mask: AXISMASK) -> (bool, int):
    """
    Checks whether an axis mask contains exactly one axis and returns the number of axes in an axis mask
    :param axis_mask: the axis mask to check
    :return: True if axis mask contains exactly one axis, False otherwise, and the number of axes in the axis mask
    """
    binary = bin(axis_mask.value)
    n = binary.count('1')
    return n == 1, n

def set_custom_xy_orign(x_offset : float, y_offset : float, connection : Connection):
    """
    Sets a new custom origin for the axis system, assumes the x-y-configuration from the OCT setup WiSe24/25
    :param x_offset: the x-Axis offset
    :param y_offset: the y-Axis offset
    :param connection: the connection to set the offsets on

    :raises: AxisCallException if the parameters are of the wrong type or the offset is out of bounds
    """

    try:
        assert type(x_offset) == float, "x_offset not of type float"
        assert type(y_offset) == float, "y_offset not of type float"
        assert type(connection) == Connection, "connection not of type Connection"
    except AssertionError as e:
        raise AxisCallException(201, str(e))

    if not check_offset(connection.get_axis_list()[0], x_offset):
        raise AxisCallException(202,"x_offset out of bounds")

    if not check_offset(connection.get_axis_list()[1], y_offset):
        raise AxisCallException(202,"y_offset out of bounds")

    connection.get_axis_list()[0].set_offset(x_offset)
    connection.get_axis_list()[1].set_offset(y_offset)


def check_offset(axis: Axis, offset: float) -> bool:
    """
    Checks whether an offset is within the bounds for an Axis
    :param axis: the axis to check
    :param offset: the offset to check
    :return: True if offset is within the bounds, False otherwise
    """
    return axis.get_min() <= offset <= axis.get_max()

