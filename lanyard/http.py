from aiohttp import ClientSession
import asyncio
from typing import Optional

API_URL = "https://api.lanyard.rest/v1/"

class HTTPClient:
    def __init__(self, session: ClientSession = None,key: Optional[str] = None) -> None:
        self.key = key
        self.session = session

    async def fetch_user_data(self, user: int):
        resp = await (await self.session.get(f"{API_URL}/users/{user}")).json()

        return resp

    async def close(self):
        await self.session.close()
