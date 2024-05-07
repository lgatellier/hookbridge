import logging

from webhook_gateway.configuration import (
    WebhookGatewayConfig,
    setup_logging,
    validate_config,
)
from webhook_gateway import __version__, api

setup_logging()

logger = logging.getLogger(__name__)
logger.info(f"Starting up webhook_gateway {__version__}")

app = api.api
app.configuration = WebhookGatewayConfig()
app.configuration.init_resources()
app.configuration.wire(modules=["webhook_gateway", "webhook_gateway.configuration", "webhook_gateway.api"])
validate_config()
