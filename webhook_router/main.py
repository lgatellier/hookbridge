from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI, Request, Depends
import logging
from os import environ as env
import sys

from .configuration import WebhookRouterConfig, setup_logging
from .router import RouterService
from . import __version__, api

setup_logging()

logger = logging.getLogger(__name__)
logger.info(f"Starting up webhook_router {__version__}")

app = api.api
app.configuration = WebhookRouterConfig()
app.configuration.wire(modules=[".api"])
