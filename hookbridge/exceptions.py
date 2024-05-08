from fastapi import HTTPException


class HTTPExceptionWithParameters(HTTPException):
    def __init__(self, message, *parameters, http_status=500) -> None:
        super().__init__(status_code=http_status, detail=message.format(*parameters))


class UnauthorizedAccessException(HTTPExceptionWithParameters):
    """
    Unauthorized accesses-related exception.
    Always gives HTTP 401 error with given message, formatted with parameters
    """

    def __init__(self, message, *parameters) -> None:
        super().__init__(message, *parameters, http_status=401)


class ConfigurationException(Exception):
    pass


class UnResolvableInjectionException(HTTPExceptionWithParameters):
    def __init__(self, injectpath, *parameters) -> None:
        super().__init__(
            f"Could not resolve injection {injectpath}", *parameters, http_status=500
        )
