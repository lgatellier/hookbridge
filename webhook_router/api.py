from dependency_injector.wiring import inject, Provide
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
import json
from starlette.types import Message

from .configuration import WebhookRouterConfig
from .router import RouterService

api = FastAPI()

@api.post('/route/{route_name}')
@inject
async def dispatch(
        route_name: str,
        req: Request,
        router_service: RouterService = Depends(Provide[WebhookRouterConfig.router_service])):

        req.json_body = json.loads(await req.body())
        router_service.dispatch(route_name, req)
        return {
            "message": "Hello router",
            "route": route_name
        }

@api.get('/status')
async def status():
    return { "message": "Hello World" }
