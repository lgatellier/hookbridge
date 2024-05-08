from hookbridge.request import WebhookRequest
from hookbridge.context import ExecutionContext


class MockedHTTPRequest(WebhookRequest):
    def __init__(self, body: dict = {}, headers: dict = {}):
        super().__init__({"type": "http"})
        self.__body = body
        self.__headers = headers
        self.__context = ExecutionContext(body)

    @property
    def body(self) -> dict:
        return self.__body

    @property
    def headers(self) -> dict:
        return self.__headers

    @property
    def context(self) -> ExecutionContext:
        return self.__context
