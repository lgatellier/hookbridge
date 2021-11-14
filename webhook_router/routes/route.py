from fastapi import Request
import logging

from .rules import parse_input_rule
from .exceptions import MissingAuthException, InvalidAuthException


logger = logging.getLogger(__name__)

class Route:
    def __init__(self, name: str, cfg: object):
        logger.debug(f'Loading route {name}')
        self.__name = name
        self.__config = cfg
        self.__auth_headers = cfg['auth_headers']
        self.__input_rules = [ parse_input_rule(k, v) for k, v in cfg['input']['body'].items() ]

    @property
    def name(self):
        return self.__name

    @property
    def config(self):
        return self.__config

    def validate_auth(self, req: Request) -> None:
        '''
        Validates auth headers in given Request for current Route.
        Raises MissingAuthException or InvalidAuthException when an auth header is missing or invalid.
        '''
        for k, v in self.__auth_headers.items():
            if k not in req.headers:
                raise MissingAuthException(k)
            elif req.headers[k] != v:
                raise InvalidAuthException(k)

    def check_inputs(self, req: Request) -> None:
        for rule in self.__input_rules:
            rule.apply(req)
