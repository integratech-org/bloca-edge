import asyncio
import logging
from functools import partial

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

    ws = WSClient(
        settings=settings,
    )

    mqtt = MQTTClient(
        settings=settings,
        handlers={
            TOPIC_STATUS: handle_status,
            TOPIC_TELEMETRY: partial(handle_telemetry, ws),
        },
    )

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(ws.run())
            tg.create_task(mqtt.run())

    finally:
        logger.info("bloca-edge server stopped")


if __name__ == "__main__":
    asyncio.run(main())
