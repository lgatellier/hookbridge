import json
import logging
from os import access, R_OK
from os.path import isfile

from webhook_gateway.routes.rules.output import CallResult

from .route import Route
from .validator import validate_route
from .exceptions import NonExistingRouteException
from ..request import WebhookRequest

logger = logging.getLogger(__name__)


class RouteService:
    def __init__(self, config_file="./routes.json"):
        logger.info("Initializing RouteService")
        assert (
            config_file is not None
            and isfile(config_file)
            and access(config_file, R_OK)
        ), f"File {config_file} does not exist or is not readable"

        logger.info(f"Loading routes file '{config_file}'")
        with open(config_file, "r") as file:
            cfg = json.load(file)
            self.__routes = {k: Route(k, v) for k, v in cfg.items()}
        logger.info("RouteService is ready")

    @property
    def route_count(self):
        return len(self.__routes)

    def validate_routes(self):
        # Validate routes configuration
        for r in self.__routes.values():
            validate_route(r)

    def get_route(self, route_name) -> Route:
        logger.debug(f"Looking for route {route_name}")
        if route_name not in self.__routes:
            raise NonExistingRouteException(route_name)
        return self.__routes[route_name]

    def dispatch(self, route_name: str, req: WebhookRequest) -> list[CallResult]:
        route = self.get_route(route_name)
        logger.debug(f"Dispatching request to route {route.name}")

        route.validate_auth(req)
        route.validate_inputs(req)
        return route.dispatch(req)
