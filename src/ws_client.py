import asyncio
import json
import websockets

from ws_utils import connect_and_subscribe


async def read_messages(websocket):
    while True:
        message = await websocket.recv()
        print("Received message:", message)


async def main():
    websocket = await connect_and_subscribe()
    await read_messages(websocket)


if __name__ == "__main__":
    asyncio.run(main())