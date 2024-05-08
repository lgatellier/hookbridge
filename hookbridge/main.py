import logging

from hookbridge.configuration import (
    HookBridgeConfig,
    setup_logging,
    validate_config,
)
from hookbridge import __version__, api

setup_logging()

logger = logging.getLogger(__name__)
logger.info(f"Starting up HookBridge {__version__}")

app = api.api
app.configuration = HookBridgeConfig()
app.configuration.init_resources()
app.configuration.wire(
    modules=["hookbridge", "hookbridge.configuration", "hookbridge.api"]
)
validate_config()
