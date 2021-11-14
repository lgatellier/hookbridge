from fastapi import Request
import logging

from webhook_router.exceptions import NonExistingRouteException
from .routes import RouteService

logger = logging.getLogger(__name__)

class RouterService:
    def __init__(self, routes: RouteService) -> None:
        logger.info('Initializing RouterService')
        self.__routes = routes

    def dispatch(self, route_name: str, req: Request):
        route = self.__routes.get_route(route_name)
        logger.debug(f'Dispatching request to route {route.name}')