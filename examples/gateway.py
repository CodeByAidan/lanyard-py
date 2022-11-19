from lanyard import GatewayClient

gateway = GatewayClient([894794517079793704])

@gateway.ready()
async def ready(data):
    print("Im ready! :D")

@gateway.message()
async def message(data):
    print("Got presence update :D")

gateway.start()