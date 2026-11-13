import asyncio
import logging

from bloca_edge.config import get_settings
from bloca_edge.handlers import handle_status, handle_telemetry
from bloca_edge.mqtt import TOPIC_STATUS, TOPIC_TELEMETRY, MQTTClient
from bloca_edge.ws import WSClient

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
    )
    settings = get_settings()

    logger.info("bloca-edge server starting")

    mqtt = MQTTClient(
        settings=settings,
        handlers={TOPIC_STATUS: handle_status, TOPIC_TELEMETRY: handle_telemetry},
    )

    ws = WSClient(
        settings=settings,
    )

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(mqtt.run())
            tg.create_task(ws.run())
    finally:
        logger.info("bloca-edge server stopped")


if __name__ == "__main__":
    asyncio.run(main())
