import json
import logging
import numpy
import websockets

from datetime import datetime, timezone


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


WS_URI = "wss://ws-feed.exchange.coinbase.com"
SUBSCRIBE_MESSAGE = {
    "type": "subscribe",
    "channels": [
        {
            "name": "heartbeat",
            "product_ids": ["E1TH-EUR"]
        }
    ]
}


async def connect_and_subscribe(name="ws"):
    logging.info(f"Connecting {name}...")
    websocket = await websockets.connect(WS_URI)
    await websocket.send(json.dumps(SUBSCRIBE_MESSAGE))
    logging.info(f"{name} subscribed.")
    return websocket


async def read_messages(websocket, process_message_callback=None, total_messages=None, queue=None, name=None):
    latencies = []
    count_messages = 0

    try:
        while True:
            message = await websocket.recv()
            logging.info(f"Received message: {message}")

            data = json.loads(message)
            if data.get("type") == "error":
                logging.error(f"Error detected: {message}; Exiting loop.")
                break

            receipt_time = datetime.utcnow()

            if process_message_callback:
                latency = await process_message_callback(message, receipt_time)

                if latency is not None:
                    latencies.append(latency)
                    logging.info(f"{count_messages}/{total_messages} Received message with latency: {latency:.4f} ms")

            if total_messages is not None:
                count_messages += 1

            if queue is not None and name is not None:
                data = json.loads(message)
                if data.get("type") == "heartbeat":
                    sequence = data.get("sequence")
                    queue.put_nowait((name, sequence, receipt_time, message))

            if total_messages is not None and count_messages >= total_messages + 1: # 1st message is subscription message
                break

    finally:
        if latencies:
            percentiles = numpy.percentile(latencies, [50, 90, 95, 99])
            logging.info("Latency Percentiles (ms):")
            logging.info(f"50th: {percentiles[0]:.4f}")
            logging.info(f"90th: {percentiles[1]:.4f}")
            logging.info(f"95th: {percentiles[2]:.4f}")
            logging.info(f"99th: {percentiles[3]:.4f}")
