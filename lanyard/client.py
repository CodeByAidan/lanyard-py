from .http import HTTPClient
from .gateway import GatewayClient
from typing import Optional, Callable, Any, Awaitable
from .models import Presence
import asyncio
from aiohttp import ClientSession

coro = Callable[[Any, Any], Awaitable[Any]]

class Client:
    def __init__(self, ids: Optional[str] = None, key: Optional[str] = None):
        self.key = key
        self.ids = ids

        self.http = HTTPClient(session=None)
        self.ws = GatewayClient(ids)
        self.loop = asyncio.get_event_loop()
        self._closed = False

    async def login(self):
        session = ClientSession()
        self.http.session = session

    async def connect(self):
        while not self._closed:
            await self.ws.connect()
    
    async def start(self):
        await self.login()
        await self.connect()

    async def fetch_user_data(self, user: int):
        resp = await self.http.fetch_user_data(user)

        return Presence(resp)

    def message(self):
        def wrapper(func: coro):
            self.ws.__event_function = func

        return wrapper

    def ready(self):
        def wrapper(func: coro):
            self.ws.__ready_function = func

        return wrapper