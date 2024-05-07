from dependency_injector import containers, providers
import logging
import os
from dependency_injector.wiring import Provide, inject
import yaml

from hookbridge.routes import RouteService


class WebhookGatewayConfig(containers.DeclarativeContainer):
    """
    Application dependency injection configuration
    """

    config = providers.Configuration()
    config.config_file.from_env("ROUTES_CONFIG", "routes.json")
    config.config_dir.from_env("ROUTES_CONFIG_DIR", "routes.d")

    routes_service = providers.Singleton(
        RouteService, config.config_file, config.config_dir
    )
    wiring_config = containers.WiringConfiguration(modules=[".main"])


@inject
def validate_config(
    routes: RouteService = Provide[WebhookGatewayConfig.routes_service],
):
    routes.validate_routes()


def setup_logging(
    default_path="logging.yml", default_level=logging.INFO, env_key="LOG_CFG"
):
    """
    | **@author:** Prathyush SP
    | Logging Setup
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print("Error in Logging Configuration. Using default configs")
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level, encoding="utf-8")
        print("Failed to load configuration file. Using default configs")
