import json
import typing
from fastapi import Request
from starlette.datastructures import Headers


class WebhookRequest(Request):
    def __init__(self, req: Request) -> None:
        self.__req = req
        self.__body = None

    @property
    def headers(self) -> Headers:
        return self.__req.headers

    @property
    def cookies(self) -> typing.Dict[str, str]:
        return self.__req.cookies

    @property
    def body(self) -> bytes:
        return self.__body

    @property
    def variables(self):
        return self.__variables

    @variables.setter
    def variables(self, variables):
        self.__variables = variables

    async def init(self):
        self.__body = json.loads(await self.__req.body())
