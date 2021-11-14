from datetime import datetime
from dependency_injector.wiring import inject, Provide
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
import json
from starlette.types import Message

from webhook_router.routes.service import RouteService

from .configuration import WebhookRouterConfig
from .router import RouterService

api = FastAPI()
start_time = datetime.now()


@api.post("/route/{route_name}")
@inject
async def dispatch(
    route_name: str,
    req: Request,
    router_service: RouterService = Depends(
        Provide[WebhookRouterConfig.router_service]
    ),
):

    req.json_body = json.loads(await req.body())
    router_service.dispatch(route_name, req)
    return {"message": "Hello router", "route": route_name}


@api.get("/status")
@inject
async def status(
    routes_service: RouteService = Depends(Provide[WebhookRouterConfig.routes_service]),
):
    delta = datetime.now() - start_time
    delta_str_without_micros = str(delta).split(".")[0]
    return {
        "status": "available",
        "route_count": routes_service.route_count,
        "uptime": delta_str_without_micros,
    }
