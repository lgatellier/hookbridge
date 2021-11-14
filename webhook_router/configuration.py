from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
import logging
from logging import config
import os
import yaml

from . import routes, router

class WebhookRouterConfig(containers.DeclarativeContainer):
    '''
    Application dependency injection configuration
    '''
    config = providers.Configuration()
    config.config_file.from_env('ROUTER_CONFIG', 'routes.json')

    routes_service = providers.Singleton(routes.RouteService, config.config_file)
    router_service = providers.Singleton(router.RouterService, routes_service)

    wiring_config = containers.WiringConfiguration(modules=[".main"])

def setup_logging(default_path='logging.yml', default_level=logging.INFO, env_key='LOG_CFG'):
    '''
    | **@author:** Prathyush SP
    | Logging Setup
    '''
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level, encoding='utf-8')
        print('Failed to load configuration file. Using default configs')
