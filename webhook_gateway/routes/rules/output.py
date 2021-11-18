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
        return CallResult(rule_name=self.name, http_status=response.status_code)


class CallResult:
    def __init__(self, rule_name: str, http_status) -> None:
        self.rule_name = rule_name
        self.http_status = http_status
