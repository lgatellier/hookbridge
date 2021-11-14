from dependency_injector.wiring import inject, Provide
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from webhook_router.exceptions import NonExistingRouteException

from .router import RouterService
from .configuration import WebhookRouterConfig

app = FastAPI()

@app.post('/route/{route_name}')
@inject
async def dispatch(
        route_name: str,
        req: Request,
        router_service: RouterService = Depends(Provide[WebhookRouterConfig.router_service])):
    try:
        router_service.dispatch(route_name, req)
        return {
            "message": "Hello router",
            "route": route_name
        }
    except NonExistingRouteException as ex:
        return JSONResponse(status_code=404, content={"message": str(ex)})

@app.get('/status')
async def status():
    return { "message": "Hello World" }