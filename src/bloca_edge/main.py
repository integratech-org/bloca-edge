import asyncio
import logging

from bloca_edge.config import get_settings
from bloca_edge.mqtt import MQTTClient

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
    )
    settings = get_settings()
    logger.info("Starting bloca-edge (device_id=%s)", settings.device_id)

    mqtt = MQTTClient(settings)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(mqtt.run())


if __name__ == "__main__":
    asyncio.run(main())
