from lanyard import Client
import asyncio

client = Client("894794517079793704")

@client.ready()
async def ready(msg):
    print( "ho")

async def main():
    await client.start()

    print(await client.fetch_user_data(894794517079793704))

asyncio.run(main())