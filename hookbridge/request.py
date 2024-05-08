from fastapi import Request
import json
import logging
from starlette.datastructures import Headers
from typing import Dict

from hookbridge.context import ExecutionContext

logger = logging.getLogger(__name__)


class WebhookRequest(Request):
    def __init__(self, req: Request) -> None:
        self.__req = req
        self.__body = None
        self.__context = ExecutionContext()

    @property
    def headers(self) -> Headers:
        return self.__req.headers

    @property
    def cookies(self) -> Dict[str, str]:
        return self.__req.cookies

    @property
    def body(self) -> bytes:
        return self.__body

    @property
    def context(self) -> ExecutionContext:
        return self.__context

    async def await_body(self):
        self.__body = json.loads(await self.__req.body())
