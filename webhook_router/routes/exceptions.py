from ..exceptions import HTTPExceptionWithParameters, UnauthorizedAccessException

class NonExistingRouteException(HTTPExceptionWithParameters):
    def __init__(self, route_name):
        super().__init__('Route \'{0}\' does not exist', route_name, http_status=404)
        
class MissingAuthException(UnauthorizedAccessException):
    def __init__(self, missing_auth_header) -> None:
        super().__init__('Missing \'{0}\' auth header', missing_auth_header)

class InvalidAuthException(UnauthorizedAccessException):
    def __init__(self, invalid_auth_header) -> None:
        super().__init__('Invalid \'{0}\' auth header', invalid_auth_header)

class RequestDoNotMatchRouteException(HTTPExceptionWithParameters):
    def __init__(self, rule_name, detail) -> None:
        super().__init__("Request violates a '{0}' rule. Detail : \'{1}'", rule_name, detail, http_status=400)
