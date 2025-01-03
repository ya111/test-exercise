import asyncio
import json
import websockets

WS_URI = "wss://ws-feed.exchange.coinbase.com"
SUBSCRIBE_MESSAGE = {
    "type": "subscribe",
    "channels": [
        {
            "name": "heartbeat",
            "product_ids": ["ETH-EUR"]
        }
    ]
}

async def connect_and_subscribe():
    websocket = await websockets.connect(WS_URI)
    await websocket.send(json.dumps(SUBSCRIBE_MESSAGE))
    return websocket

async def read_messages(websocket):
    while True:
        message = await websocket.recv()
        print("Received message:", message)

async def main():
    websocket = await connect_and_subscribe()
    await read_messages(websocket)

if __name__ == "__main__":
    asyncio.run(main())