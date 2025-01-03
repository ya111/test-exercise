import asyncio
import json
import numpy
import websockets
from datetime import datetime


WS_URI = "wss://ws-feed.exchange.coinbase.com"
SUBSCRIBE_MESSAGE = {
    "type": "subscribe",
    "channels": [
        {
            "name": "ticker",
            "product_ids": ["ETH-EUR"]
        }
    ]
}


async def connect_and_subscribe():
    websocket = await websockets.connect(WS_URI)
    await websocket.send(json.dumps(SUBSCRIBE_MESSAGE))
    return websocket


async def read_messages(websocket):
    latencies = []
    count_messages = 0
    total_messages = 10

    try:
        while True:
            message = await websocket.recv()
            receipt_time = datetime.utcnow() #now doesn't work cause my timezone is UTC+3 :/
            message_data = json.loads(message)
            # print(message_data)
            if 'time' in message_data:
                server_time = datetime.fromisoformat(message_data['time'].replace('Z', ''))
                latency = (receipt_time - server_time).total_seconds() * 1000  # Convert to milliseconds
                latencies.append(latency)
                count_messages += 1
                print(f"{count_messages}/{total_messages} Received message with latency: {latency:.4f} ms")

            if count_messages >= total_messages:
                break

    finally:
        # Calculate percentiles
        percentiles = numpy.percentile(latencies, [50, 90, 95, 99])
        print("Latency Percentiles (ms):")
        print(f"50th: {percentiles[0]:.4f}")
        print(f"90th: {percentiles[1]:.4f}")
        print(f"95th: {percentiles[2]:.4f}")
        print(f"99th: {percentiles[3]:.4f}")


async def main():
    websocket = await connect_and_subscribe()
    await read_messages(websocket)


if __name__ == "__main__":
    asyncio.run(main())