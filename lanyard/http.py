import asyncio
from typing import Optional

from aiohttp import ClientSession

from .models import Presence

from .gateway import GatewayClient

API_URL = "https://api.lanyard.rest/v1/"


class HTTPClient:
    def __init__(
        self, key: Optional[str] = None
    ) -> None:
        self.key = key

    async def connect(self):
        self.session = ClientSession()
        

    async def fetch_user_data(self, user: int):
        resp = await (await self.session.get(f"{API_URL}/users/{user}")).json()

        return Presence(resp)

    async def close(self):
        await self.session.close()
