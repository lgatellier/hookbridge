class NonExistingRouteException(Exception):
    MESSAGE_PATTERN = 'Route \'{0}\' does not exist'

    def __init__(self, route_name):
        self.__route_name = route_name
        super().__init__(NonExistingRouteException.MESSAGE_PATTERN.format(route_name))

    @property
    def route_name(self):
        return self.__route_name
