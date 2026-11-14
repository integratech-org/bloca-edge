import logging

from pydantic import BaseModel
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed

from bloca_edge.config import Settings

logger = logging.getLogger(__name__)


class WSClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._ws = None

    async def send(self, msg: BaseModel) -> None:
        if self._ws is None:
            return
        try:
            await self._ws.send(msg.model_dump_json())
        except ConnectionClosed:
            logger.warning("WebSocket connection closed. Message not sent.")

    async def run(self) -> None:
        s = self._settings
        headers = {"Authorization": f"Bearer {s.device_token}"}

        async for websocket in connect(s.cloud_ws_url, additional_headers=headers):
            logger.info("WebSocket connected to %s", s.cloud_ws_url)
            self._ws = websocket
            try:
                async for message in websocket:
                    logger.info("Received message: %s", message)
            except ConnectionClosed:
                logger.warning("WebSocket connection closed. Reconnecting...")
                continue
