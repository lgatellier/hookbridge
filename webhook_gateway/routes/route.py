import logging
from ..request import WebhookRequest

from .exceptions import MissingAuthException, InvalidAuthException
from .rules import parse_input_rule
from .rules.output import CallResult, OutputRule


logger = logging.getLogger(__name__)


class Route:
    def __init__(self, name: str, cfg: dict):
        logger.debug(f"Loading route {name}")
        self.__name = name
        self.__config = cfg
        self.__auth_headers = cfg["auth_headers"]
        self.__input_rules = [
            parse_input_rule(k, v) for k, v in cfg["input"]["body"].items()
        ]
        self.__output_rules = [OutputRule(v) for v in cfg["output"]]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def config(self) -> dict:
        return self.__config

    @property
    def input_rules(self):
        return self.__input_rules

    @property
    def output_rules(self):
        return self.__output_rules

    def validate_auth(self, req: WebhookRequest) -> None:
        """
        Validates auth headers in given Request for current Route.
        Raises MissingAuthException or InvalidAuthException when an auth header is missing or invalid.
        """
        for k, v in self.__auth_headers.items():
            if k not in req.headers:
                raise MissingAuthException(k)
            elif req.headers[k] != v:
                raise InvalidAuthException(k)

    def validate_inputs(self, req: WebhookRequest) -> None:
        for rule in self.__input_rules:
            rule.apply(req)

    def dispatch(self, req: WebhookRequest) -> list[CallResult]:
        results: list[CallResult] = []
        for rule in self.__output_rules:
            call_result = rule.apply(req)
            results.append(call_result)
        return results
