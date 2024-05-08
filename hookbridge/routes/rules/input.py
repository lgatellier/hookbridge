import abc
import logging
from jsonpath_ng import parse
from typing import Optional, final

from hookbridge.request import WebhookRequest
from hookbridge.routes.exceptions import RequestDoNotMatchRouteException
from hookbridge.exceptions import UnResolvableInjectionException

logger = logging.getLogger(__name__)


class InputRule:
    __metaclass__ = abc.ABCMeta

    def __init__(self, target: str, config: dict) -> None:
        self.__name = self.__class__.__name__
        self.__target = target
        self.__config = config
        if "context_variable" in config:
            self.__variable_name = config["context_variable"]
        else:
            self.__variable_name = None
        logger.debug(f"Loading rule {self.__name} with target {target}")

    @property
    def name(self):
        return self.__name

    @property
    def target(self) -> Optional[str]:
        return self.__target

    @property
    def config(self) -> Optional[dict]:
        return self.__config

    @property
    def variable_name(self) -> Optional[str]:
        return self.__variable_name

    @final
    def apply(self, req: WebhookRequest) -> None:
        if not self._do_apply(req):
            raise RequestDoNotMatchRouteException(self.name, self.target)

    @abc.abstractmethod
    def _do_apply(self, req) -> bool:
        pass


class RouteBodyInputRule(InputRule):
    __metaclass__ = abc.ABCMeta

    def __init__(self, property_json_path: str, config: dict) -> None:
        super().__init__(property_json_path, config)
        self.__json_path_expr = parse(property_json_path)

    @final
    def _do_apply(self, req: WebhookRequest) -> bool:
        try:
            value = req.context.resolve_input(self.__json_path_expr)
        except UnResolvableInjectionException:
            raise RequestDoNotMatchRouteException(self.name, self.target)

        if self.variable_name:
            req.context.set(self.variable_name, value)

        return self._matches_property(value)

    @abc.abstractmethod
    def _matches_property(self, value: any) -> bool:
        return False


class BodyPropertyPresentInputRule(RouteBodyInputRule):
    def _matches_property(self, value: any) -> bool:
        return bool(value)


class BodyPropertyEqualsToInputRule(RouteBodyInputRule):
    def _matches_property(self, value: any) -> bool:
        if not value:
            return False

        return value == self.config["equalsTo"]


input_rules = {
    "present": BodyPropertyPresentInputRule,
    "equalsTo": BodyPropertyEqualsToInputRule,
}


def read_input_rule_type(key, value):
    if isinstance(value, str):
        return value
    elif isinstance(value, dict):
        if "type" in value.keys():
            return value["type"]
        elif len(value.keys()):
            return list(value.keys())[0]

    raise Exception(f"Invalid route input configuration format for key {key}")


def parse_input_rule(key: str, value) -> InputRule:
    input_rule_type = read_input_rule_type(key, value)

    if input_rule_type not in input_rules.keys():
        raise Exception(f"Unknown input check type '{input_rule_type}'")

    return input_rules[input_rule_type](key, value)
