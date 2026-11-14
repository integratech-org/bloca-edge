import json
import logging

from pydantic import ValidationError

from bloca_edge.models import Telemetry, TelemetryMessage
from bloca_edge.ws import WSClient

logger = logging.getLogger(__name__)


async def handle_status(payload: bytes) -> None:
    data = json.loads(payload)
    logger.info("status: %s", data)


async def handle_telemetry(ws: WSClient, payload: bytes) -> None:
    try:
        telemetry = Telemetry.model_validate_json(payload)
    except ValidationError as exc:
        logger.error("Invalid telemetry data: %s", exc)
        return
    await ws.send(TelemetryMessage(payload=telemetry))
