import logging
import requests

from ...request import WebhookRequest

logger = logging.getLogger(__name__)


class OutputRule:
    def __init__(self, obj: dict) -> None:
        self.__url = obj["url"]
        self.__headers = obj["headers"]
        self.__body = obj["body"]

    def apply(self, req: WebhookRequest):
        headers = self.__eval_headers(req)
        body = self.__eval_body(req)
        response = requests.post(self.__url, headers=headers, data=body)
        logger.debug(f"Got HTTP status {response.status_code}")

    def __eval_headers(self, req: WebhookRequest):
        return self.__headers

    def __eval_body(self, req: WebhookRequest):
        return self.__body
