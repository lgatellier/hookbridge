import json
from json.decoder import JSONDecodeError
from jsonpath_ng import parse
import logging
import requests

from ...request import WebhookRequest

logger = logging.getLogger(__name__)


class OutputRule:
    def __init__(self, obj: dict) -> None:
        self.__name = obj["name"]
        self.__url = obj["url"]
        self.__headers = obj["headers"]
        self.__body = obj["body"]
        self.__variables = {
            var_name: parse(json_path)
            for json_path, var_name in obj["context_variables"].items()
        }

    @property
    def name(self):
        return self.__name

    def apply(self, req: WebhookRequest):
        logger.debug(f"apply: Calling {self.name}")
        response = requests.post(
            self.__url,
            headers=req.context.apply(self.__headers),
            data=req.context.apply(self.__body),
        )
        logger.debug(f"apply: {self.name} got HTTP status {response.status_code}")
        try:
            json_object = json.loads(response.content)
            for var_name, json_path_expr in self.__variables.items():
                matches = json_path_expr.find(json_object)
                var_value = matches[0].value if len(matches) > 0 else None
                req.context.set(var_name, var_value)
        except JSONDecodeError:
            logger.debug(f"{self.name} response body is not JSON")
            pass
        return CallResult(rule_name=self.name, http_status=response.status_code)


class CallResult:
    def __init__(self, rule_name: str, http_status) -> None:
        self.rule_name = rule_name
        self.http_status = http_status
