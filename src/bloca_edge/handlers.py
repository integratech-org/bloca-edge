import json
import logging

logger = logging.getLogger(__name__)


async def handle_status(payload: bytes) -> None:
    data = json.loads(payload)
    logger.info("status: %s", data)


async def handle_telemetry(payload: bytes) -> None:
    data = json.loads(payload)
    logger.info("telemetry: %s", data)
