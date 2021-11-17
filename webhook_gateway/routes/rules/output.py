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
        headers = self.__eval_headers(req)
        body = self.__eval_body(req)
        response = requests.post(self.__url, headers=headers, data=body)
        logger.debug(f"apply: {self.name} got HTTP status {response.status_code}")
        return CallResult(rule_name=self.name, http_status=response.status_code)

    def __eval_headers(self, req: WebhookRequest):
        return self.__headers

    def __eval_body(self, req: WebhookRequest):
        return self.__body


class CallResult:
    def __init__(self, rule_name: str, http_status) -> None:
        self.rule_name = rule_name
        self.http_status = http_status
