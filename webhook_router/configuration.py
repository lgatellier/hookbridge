from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from . import routes, router

class WebhookRouterConfig(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.config_file.from_env('ROUTER_CONFIG')

    routes_service = providers.Singleton(routes.RouteService, config.config_file)
    router_service = providers.Singleton(router.RouterService, routes_service)

    wiring_config = containers.WiringConfiguration(modules=[".main"])
