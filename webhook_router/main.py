import logging

from .configuration import WebhookRouterConfig, setup_logging
from . import __version__, api

setup_logging()

logger = logging.getLogger(__name__)
logger.info(f"Starting up webhook_router {__version__}")

app = api.api
app.configuration = WebhookRouterConfig()
app.configuration.wire(modules=[".api"])
