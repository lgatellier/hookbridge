from fastapi import Request


class MockedHTTPRequest(Request):
    def __init__(self, body: dict = {}, headers: dict = {}):
        super().__init__({"type": "http"})
        self.__body = body
        self.__headers = headers

    @property
    def body(self) -> dict:
        return self.__body

    @property
    def headers(self) -> dict:
        return self.__headers
