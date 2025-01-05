import json
from datetime import datetime

from src.ws_utils import connect_and_subscribe, read_messages


async def process_perf_message(message, receipt_time):
    message_data = json.loads(message)
    if 'time' in message_data:
        server_time = datetime.fromisoformat(message_data['time'].replace('Z', ''))
        print(receipt_time)
        print(server_time)
        latency = (receipt_time - server_time).total_seconds() * 1000  # Convert to milliseconds
        return latency
    return None


async def perf_test(total_messages):
    websocket = await connect_and_subscribe()
    await read_messages(websocket, process_perf_message, total_messages=total_messages)