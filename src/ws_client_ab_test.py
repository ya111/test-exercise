import asyncio
import json
import websockets
from datetime import datetime, timezone


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


async def connect_and_subscribe(name):
    websocket = await websockets.connect(WS_URI)
    await websocket.send(json.dumps(SUBSCRIBE_MESSAGE))
    print(f"Connected {name}")

    return websocket


async def read_messages(name, websocket, queue):
    while True:
        message = await websocket.recv()
        receipt_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        data = json.loads(message)
        if data.get("type") == "heartbeat":
            sequence = data.get("sequence")
            queue.put_nowait((name, sequence, receipt_time, message))
            # print(f"{name}: Received message at {receipt_time.isoformat()}")


async def compare_connections():
    queue1 = asyncio.Queue()
    queue2 = asyncio.Queue()

    connection1 = await connect_and_subscribe("Connection 1")
    connection2 = await connect_and_subscribe("Connection 2")

    task1 = asyncio.create_task(read_messages("Connection 1", connection1, queue1))
    task2 = asyncio.create_task(read_messages("Connection 2", connection2, queue2))

    count_messages = 0
    connection1_wins = 0
    connection2_wins = 0
    draws = 0
    max_diff = 0
    total_messages = 100


    try:
        while True:
            conn1_data = await queue1.get()
            conn2_data = await queue2.get()

            if conn1_data[1] == conn2_data[1]:  # Compare sequence numbers
                latency_diff = (conn1_data[2] - conn2_data[2]).total_seconds() * 1000
                # print(f"Message with sequence {conn1_data[1]}: Time difference is {latency_diff:.4f} ms")
                if abs(latency_diff) > max_diff: 
                    max_diff = abs(latency_diff)
                if (conn1_data[2] - conn2_data[2]).total_seconds() > 0:
                    connection1_wins += 1
                elif (conn1_data[2] - conn2_data[2]).total_seconds() < 0:
                    connection2_wins += 1
                elif (conn1_data[2] - conn2_data[2]).total_seconds() == 0:
                    draws += 1
                count_messages += 1 # success attempt -> +1
            else:
                # If not matched, enqueue the later message back for further comparison
                if conn1_data[1] < conn2_data[1]:
                    queue2.put_nowait(conn2_data)
                else:
                    queue1.put_nowait(conn1_data)

            print (f"{count_messages}/{total_messages}")
            if count_messages >= total_messages:
                break
    finally:
        print(f"conn1 wins: {connection1_wins}")
        print(f"conn2 wins: {connection2_wins}")
        print(f"draws: {draws}")
        print(f"max diff: {max_diff:.4f} ms")


if __name__ == "__main__":
    asyncio.run(compare_connections())