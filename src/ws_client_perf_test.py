import json
from datetime import datetime
import logging

from src.ws_utils import connect_and_subscribe, read_messages


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def process_perf_message(message, receipt_time):
    message_data = json.loads(message)
    if 'time' in message_data:
        server_time = datetime.fromisoformat(message_data['time'].replace('Z', ''))
        logging.info(f"receipt_time: {receipt_time}")
        logging.info(f"server_time: {server_time}")
        latency = (receipt_time - server_time).total_seconds() * 1000  # Convert to milliseconds
        return latency
    return None


async def perf_test(total_messages):
    websocket = await connect_and_subscribe()
    await read_messages(websocket, process_perf_message, total_messages=total_messages)