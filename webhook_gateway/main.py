import logging

from .configuration import WebhookGatewayConfig, setup_logging
from . import __version__, api

setup_logging()

logger = logging.getLogger(__name__)
logger.info(f"Starting up webhook_gateway {__version__}")

app = api.api
app.configuration = WebhookGatewayConfig()
app.configuration.wire(modules=[".api"])
