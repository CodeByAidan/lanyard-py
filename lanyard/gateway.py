import asyncio
import json
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from aiohttp import ClientSession, ClientWebSocketResponse

from .models import Presence

GW_URL = "wss://api.lanyard.rest/socket"

CoroFunc = Callable[[Any, Any], Awaitable[Any]]


class Opcodes:
    EVENT = 0
    HELLO = 1
    INITIALIZE = 2
    HEARTBEAT = 3


class GatewayClient:
    if TYPE_CHECKING:
        ws: ClientWebSocketResponse

    def __init__(self, ids: list[int]) -> None:
        self.ids = [str(id) for id in ids]
        self._loop = asyncio.get_event_loop()
        self.__event_function: CoroFunc = None
        self.__ready_function: CoroFunc = None
        self._last_status = {}

    async def heartbeat(self):
        while True:
            await self.ws.send_json({"op": Opcodes.HEARTBEAT, "d": None})
            await asyncio.sleep(self.heartbeat_interval / 1000)

    def message(self):
        def wrapper(func: CoroFunc):
            self.__event_function = func

        return wrapper

    def ready(self):
        def wrapper(func: CoroFunc):
            self.__ready_function = func

        return wrapper

    async def _initilize(self, data):
        await self.ws.send_json(
            {
                "op": Opcodes.INITIALIZE,
                "d": {"subscribe_to_ids": self.ids},
            }
        )

        self.heartbeat_interval = data["heartbeat_interval"]
        self._loop.create_task(self.heartbeat())

    def handle_events(self, data):
        if data["t"] == "INIT_STATE":
            ids = [data['d'][id] for id in self.ids]
            for user in ids:
                self._last_status[user['discord_user']['id']] = user['discord_status']

            self._loop.create_task(self.__ready_function(data['d']))
            del ids
        elif data['d']['discord_status'] == self._last_status[data['d']['discord_user']['id']]:
            return

        else:
            self._loop.create_task(self.__event_function(data['d']))

    async def connect(self):
        self.session = ClientSession()
        self.ws = await self.session.ws_connect(GW_URL)

        while True:
            data = await self.ws.receive()

            if isinstance(data.data, int) and len(str(data.data)) == 4:
                print(
                    f"The websocket did a fucky-wucky owo! Found: {data.data}: {data.extra}"
                )
                continue
            elif isinstance(data.data, type(None)):
                if data.type == 0x101:
                    return None

            data = json.loads(data.data)

            if data["op"] == Opcodes.HELLO:
                await self._initilize(data["d"])

            elif data["op"] == Opcodes.EVENT:
                self.handle_events(data)

    async def close(self):
        await self.ws.close()
        await self.session.close()

    def start(self):
        self._loop.run_until_complete(self.connect())
