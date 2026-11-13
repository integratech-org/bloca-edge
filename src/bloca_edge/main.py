import asyncio
import logging

from bloca_edge.config import get_settings
from bloca_edge.handlers import handle_status, handle_telemetry
from bloca_edge.mqtt import TOPIC_STATUS, TOPIC_TELEMETRY, MQTTClient

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
    )
    settings = get_settings()
    logger.info("Starting bloca-edge")

    mqtt = MQTTClient(
        settings=settings,
        handlers={TOPIC_STATUS: handle_status, TOPIC_TELEMETRY: handle_telemetry},
    )

    async with asyncio.TaskGroup() as tg:
        tg.create_task(mqtt.run())


if __name__ == "__main__":
    asyncio.run(main())
