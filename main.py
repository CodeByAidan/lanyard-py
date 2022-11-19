from lanyard.gateway import GatewayClient

wss = GatewayClient(894794517079793704)

@wss.message()
async def yummers(data):
    print(f"Got message!!\n{data}")

@wss.ready()
async def ready(data):
    print("Ready :)")


wss.start()