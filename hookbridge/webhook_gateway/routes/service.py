from collections import OrderedDict
from glob import glob
import json
import logging
from os import access, R_OK
from os.path import abspath, isfile

from hookbridge.routes.rules.output import CallResult

from hookbridge.routes.route import Route
from hookbridge.routes.validator import validate_route
from hookbridge.routes.exceptions import NonExistingRouteException
from hookbridge.request import WebhookRequest

logger = logging.getLogger(__name__)


class RouteService:
    def __init__(self, config_file="./routes.json", config_dir="./routes.d"):
        logger.info("Initializing RouteService")

        readable_config_files = RouteService.list_readable_config_files(
            config_file, config_dir
        )
        assert len(config_file) > 0

        self.__routes = {}
        for file in readable_config_files:
            self.__routes = self.__routes | RouteService.parse_routes_file(file)

        logger.info(
            "RouteService is ready, %d routes loaded", len(self.__routes.keys())
        )

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

    @staticmethod
    def list_readable_config_files(
        config_file="./routes.json", config_dir="./routes.d"
    ) -> list[str]:
        logger.info("Listing available route files")
        config_file_list = [config_file, *glob(f"{config_dir}/*.json")]
        readable_config_files = [
            abspath(f) for f in config_file_list if isfile(f) and access(f, R_OK)
        ]
        logger.debug(
            "Found %d readable route files : %s",
            len(readable_config_files),
            readable_config_files,
        )
        return readable_config_files

    @staticmethod
    def parse_routes_file(config_file: str) -> dict[str, Route]:
        logger.info(f"Loading route file '{config_file}'")
        with open(config_file, "r") as file:
            cfg = json.load(file, object_pairs_hook=OrderedDict)
            return {k: Route(k, v) for k, v in cfg.items()}
