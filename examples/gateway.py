from lanyard import GatewayClient
from lanyard.models import Presence

gateway = GatewayClient(894794517079793704)

@gateway.ready()
async def ready(data: Presence):
    print(f"Im ready! :D\n{data}")

@gateway.message()
async def message(data: Presence):
    print(f"Got presence update :D\n{data}")

gateway.start()