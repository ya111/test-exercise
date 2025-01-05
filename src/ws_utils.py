import websockets
import json

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

async def connect_and_subscribe(name="master"):
    print(f"Connecting {name}...")
    websocket = await websockets.connect(WS_URI)
    await websocket.send(json.dumps(SUBSCRIBE_MESSAGE))
    print(f"{name} subscribed.")
    return websocket
