from aerotech_dictonaries import error_dict


class WrapperException(Exception):
    def __init__(self, code: int, cause: str):
        super().__init__()
        self.code = code
        self.cause = cause

    def get_error_name(self) -> str:
        return error_dict[self.code]

    def get_error_code(self) -> int:
        return self.code

    def get_error_cause(self) -> str:
        return self.cause


class AxisCallException(WrapperException):


    def __init__(self, code: int, cause: str):
        super().__init__(code, cause)


class ConnectionException(WrapperException):
    """
    ConnectionException is raised for issues with the connection.
    """
    def __init__(self, code: int, cause: str):
        super().__init__(code, cause)


class WrappedDllException(WrapperException):
    """
    WrappedDllException is raised for errors that occur within the DLL
    """
    def __init__(self, code: int, cause: str):
        super().__init__(code, cause)
