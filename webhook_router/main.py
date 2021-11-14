from os import environ as env
from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI, Request, Depends

from .configuration import WebhookRouterConfig
from .router import RouterService
from . import __version__, api


print(f'Starting up webhook_router {__version__}')

app = api.app
app.configuration = WebhookRouterConfig()
app.configuration.wire(modules=['.api'])
