from lanyard import GatewayClient
from lanyard.models import Presence

gateway = GatewayClient(894794517079793704, 921662807848669204)

# The ready and message data come in raw json, but you can make it an object through the Presence class like so below

@gateway.ready()
async def ready(data):        
    presences = [Presence(data[id]) for id in gateway.ids] # With ready event, you gotta do this since it sends both id's and their specific info at once.
    
    print(f"Ready! subscribed to: {', '.join(data.username for data in presences)}")


@gateway.message()
async def message(data):
    data = Presence(data) # We dont need to do what we did above because the lanyard only sends the data of the one person who's status changed.

    print(f"Got presence update :D\nUpdated: {data.username}'s status is now: {data.status}")

gateway.start()