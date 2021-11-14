import json
from os import access, R_OK
from os.path import isfile

from .exceptions import NonExistingRouteException

class Route:
    def __init__(self, name: str, cfg: object):
        print(f'Loading route {name}')
        self.__name = name
        self.__config = cfg

    @property
    def name(self):
        return self.__name

    @property
    def config(self):
        return self.__config

class RoutesService:
    def __init__(self, config_file = './config.json'):
        assert config_file is not None and isfile(config_file) and access(config_file, R_OK), 'File does not exist or is not readable'
        with open(config_file, 'r') as file:
            cfg = json.load(file)
            self.__routes = { k: Route(k, v) for k, v in cfg.items() }
    
    def get_route(self, route_name) -> Route:
        if route_name not in self.__routes:
            raise NonExistingRouteException(route_name)
        return self.__routes[route_name]
