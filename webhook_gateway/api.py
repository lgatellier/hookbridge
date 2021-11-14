from datetime import datetime
from dependency_injector.wiring import inject, Provide
from fastapi import Depends, FastAPI, Request

from .configuration import WebhookGatewayConfig
from .request import WebhookRequest
from .router import RouterService
from .routes.service import RouteService


api = FastAPI()
start_time = datetime.now()


@api.post("/route/{route_name}")
@inject
async def dispatch(
    route_name: str,
    req: Request,
    router_service: RouterService = Depends(
        Provide[WebhookGatewayConfig.router_service]
    ),
):

    wrapper_req = WebhookRequest(req)
    await wrapper_req.init()  # Awaits request body
    router_service.dispatch(route_name, wrapper_req)
    return {"message": "Hello router", "route": route_name}


@api.get("/status")
@inject
async def status(
    routes_service: RouteService = Depends(
        Provide[WebhookGatewayConfig.routes_service]
    ),
):
    delta = datetime.now() - start_time
    delta_str_without_micros = str(delta).split(".")[0]
    return {
        "status": "available",
        "route_count": routes_service.route_count,
        "uptime": delta_str_without_micros,
    }
