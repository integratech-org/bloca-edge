import asyncio
import logging

import aiomqtt

from bloca_edge.config import Settings

logger = logging.getLogger(__name__)

TOPIC_STATUS = "bloca/status"
TOPIC_TELEMETRY = "bloca/telemetry"
TOPIC_CMD = "bloca/cmd"


class MQTTClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

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

                    await client.subscribe(TOPIC_TELEMETRY, qos=1)

                    async for message in client.messages:
                        print(message.payload)

            except aiomqtt.MqttError as exc:
                logger.warning("MQTT connection lost: %s. Retrying in 5s", exc)
                await asyncio.sleep(5)  # Wait before retrying
