import abc
import logging
from fastapi import Request
from jsonpath_ng import parse
from typing import final

from .exceptions import RequestDoNotMatchRouteException

logger = logging.getLogger(__name__)


class RouteInputRule:
    __metaclass__ = abc.ABCMeta

    def __init__(self, detail: str, config: dict) -> None:
        self.__name = self.__class__.__name__
        self.__detail = detail
        self.__config = config
        logger.debug(f"Loading rule {self.__name} with detail {detail}")

    @property
    def config(self):
        return self.__config

    @final
    def apply(self, req: Request) -> None:
        if not self._do_apply(req):
            raise RequestDoNotMatchRouteException(self.__name, self.__detail)

    @abc.abstractmethod
    def _do_apply(self, req) -> bool:
        pass


class RouteBodyInputRule(RouteInputRule):
    __metaclass__ = abc.ABCMeta

    def __init__(self, property_json_path, config: dict) -> None:
        super().__init__(property_json_path, config)
        self.__json_path_expr = parse(property_json_path)

    @final
    def _do_apply(self, req) -> bool:
        return self._matches_property(self.__json_path_expr.find(req.json_body))

    @abc.abstractmethod
    def _matches_property(self, matches: list) -> bool:
        return False


class BodyPropertyPresentInputRule(RouteBodyInputRule):
    def _matches_property(self, matches: list) -> bool:
        return len(matches) > 0


class BodyPropertyEqualsToInputRule(RouteBodyInputRule):
    def _matches_property(self, matches: list) -> bool:
        if len(matches) == 0:
            return False

        for m in matches:
            if m.value != self.config["equalsTo"]:
                return False

        return True


available_checks = {
    "present": BodyPropertyPresentInputRule,
    "equalsTo": BodyPropertyEqualsToInputRule,
}


def parse_input_rule(key, value) -> RouteInputRule:
    input_check_type = read_input_rule_type(key, value)

    if input_check_type not in available_checks.keys():
        raise Exception(f"Unknown input check type '{input_check_type}'")

    return available_checks[input_check_type](key, value)


def read_input_rule_type(key, value):
    if isinstance(value, str):
        return value
    elif isinstance(value, dict):
        if "type" in value.keys():
            return value["type"]
        elif len(value.keys()):
            return list(value.keys())[0]

    raise Exception(f"Invalid route input configuration format for key {key}")
