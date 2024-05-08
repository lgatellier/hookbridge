from datetime import datetime
from dependency_injector.wiring import inject, Provide
from fastapi import Depends, FastAPI, Request
import logging

from hookbridge.configuration import HookBridgeConfig
from hookbridge.request import WebhookRequest
from hookbridge.routes.service import RouteService


api = FastAPI()
start_time = datetime.now()
logger = logging.getLogger(__name__)


@api.post("/route/{route_name}")
@inject
async def dispatch(
    route_name: str,
    req: Request,
    routes: RouteService = Depends(Provide[HookBridgeConfig.routes_service]),
):
    wrapper_req = WebhookRequest(req)
    # Awaits request body and initializes request route context
    await wrapper_req.init_context()
    call_results = routes.dispatch(route_name, wrapper_req)
    logger.debug("Final request route execution context : %s", wrapper_req.context)
    return {"route": route_name, "called_rules": [r.__dict__ for r in call_results]}


@api.get("/status")
@inject
async def status(
    routes: RouteService = Depends(Provide[HookBridgeConfig.routes_service]),
):
    delta = datetime.now() - start_time
    delta_str_without_micros = str(delta).split(".")[0]
    return {
        "status": "available",
        "route_count": routes.route_count,
        "uptime": delta_str_without_micros,
    }
