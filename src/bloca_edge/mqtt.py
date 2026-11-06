import asyncio
import logging
from collections.abc import Awaitable, Callable

import aiomqtt

from bloca_edge.config import Settings

logger = logging.getLogger(__name__)

TOPIC_STATUS = "bloca/status"
TOPIC_TELEMETRY = "bloca/telemetry"
TOPIC_CMD = "bloca/cmd"

Handler = Callable[[bytes], Awaitable[None]]


class MQTTClient:
    def __init__(self, settings: Settings, handlers: dict[str, Handler]) -> None:
        self._settings = settings
        self._handlers = handlers

    async def run(self) -> None:
        s = self._settings

        while True:
            try:
                async with aiomqtt.Client(
                    hostname=s.mqtt_host,
                    port=s.mqtt_port,
                    username=s.mqtt_username,
                    password=s.mqtt_password,
                    identifier=s.mqtt_client_id,
                    clean_session=s.mqtt_clean_session,
                    keepalive=s.mqtt_keepalive,
                ) as client:
                    logger.info("MQTT connected to %s:%d", s.mqtt_host, s.mqtt_port)

                    for topic in self._handlers:
                        await client.subscribe(topic, qos=1)

                    async for message in client.messages:
                        handler = self._handlers.get(str(message.topic))
                        if handler is None:
                            continue
                        try:
                            await handler(bytes(message.payload))
                        except Exception:
                            logger.exception(
                                "Error handling message on topic %s", message.topic
                            )

            except aiomqtt.MqttError as exc:
                logger.warning("MQTT connection lost: %s. Retrying in 5s", exc)
                await asyncio.sleep(5)  # Wait before retrying
