from fastapi import Request

from webhook_router.exceptions import NonExistingRouteException
from .routes import RoutesService

class RouterService:
    def __init__(self, routes: RoutesService) -> None:
        print('Initializing RouterService')
        self.__routes = routes

    def dispatch(self, route_name: str, req: Request):
        route = self.__routes.get_route(route_name)
        print(f'Dispatching request to route {route.name}')