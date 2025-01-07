from src.ws_utils import connect_and_subscribe, read_messages


async def ws_reader(total_messages):
    websocket = await connect_and_subscribe()
    await read_messages(websocket=websocket, total_messages=total_messages)
