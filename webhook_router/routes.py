import json
import logging
from os import access, R_OK
from os.path import isfile

from .exceptions import NonExistingRouteException

logger = logging.getLogger(__name__)

class Route:
    def __init__(self, name: str, cfg: object):
        logger.debug(f'Loading route {name}')
        self.__name = name
        self.__config = cfg

    @property
    def name(self):
        return self.__name

    @property
    def config(self):
        return self.__config

class RouteService:
    def __init__(self, config_file = './config.json'):
        logger.info('Initializing RouteService')
        assert config_file is not None and isfile(config_file) and access(config_file, R_OK), 'File does not exist or is not readable'
        logger.info(f'Loading routes file \'{config_file}\'')
        with open(config_file, 'r') as file:
            cfg = json.load(file)
            self.__routes = { k: Route(k, v) for k, v in cfg.items() }
        logger.info('RouteService is ready')

    def get_route(self, route_name) -> Route:
        logger.debug(f'Looking for route {route_name}')
        if route_name not in self.__routes:
            raise NonExistingRouteException(route_name)
        return self.__routes[route_name]
