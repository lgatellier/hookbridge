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
        self.__context = None

    @property
    def headers(self) -> Headers:
        return self.__req.headers

    @property
    def cookies(self) -> Dict[str, str]:
        return self.__req.cookies

    @property
    def context(self) -> ExecutionContext:
        return self.__context

    async def init_context(self):
        self.__context = ExecutionContext(input=json.loads(await self.__req.body()))
