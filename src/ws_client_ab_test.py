import asyncio
import logging

from src.ws_utils import connect_and_subscribe, read_messages


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def compare_connections(total_messages):
    queue1 = asyncio.Queue()
    queue2 = asyncio.Queue()

    connection1 = await connect_and_subscribe("Connection 1")
    connection2 = await connect_and_subscribe("Connection 2")
    task1 = asyncio.create_task(read_messages(websocket=connection1, queue=queue1, name="Connection 1"))
    task2 = asyncio.create_task(read_messages(websocket=connection2, queue=queue2, name="Connection 2"))

    count_messages = 0
    connection1_wins = 0
    connection2_wins = 0
    draws = 0
    max_diff = 0

    try:
        while True:
            conn1_data = await queue1.get()
            conn2_data = await queue2.get()

            if conn1_data[1] == conn2_data[1]:  # Compare sequence numbers
                latency_diff = (conn1_data[2] - conn2_data[2]).total_seconds() * 1000
                # logging.info(f"Message with sequence {conn1_data[1]}: Time difference is {latency_diff:.4f} ms")
                if abs(latency_diff) > max_diff: 
                    max_diff = abs(latency_diff)
                if (conn1_data[2] - conn2_data[2]).total_seconds() > 0:
                    connection1_wins += 1
                elif (conn1_data[2] - conn2_data[2]).total_seconds() < 0:
                    connection2_wins += 1
                elif (conn1_data[2] - conn2_data[2]).total_seconds() == 0:
                    draws += 1
                count_messages += 1 # success attempt -> +1
                logging.info(f"{count_messages}/{total_messages} — seq={conn1_data[1]}; conn1={conn1_data[2]}, conn2={conn2_data[2]}; Time difference is {latency_diff:.4f} ms")

            else:
                # If not matched, enqueue the later message back for further comparison
                if conn1_data[1] < conn2_data[1]:
                    queue2.put_nowait(conn2_data)
                else:
                    queue1.put_nowait(conn1_data)

            if count_messages >= total_messages:
                break
    finally:
        logging.info(f"conn1 wins: {connection1_wins}")
        logging.info(f"conn2 wins: {connection2_wins}")
        logging.info(f"draws: {draws}")
        logging.info(f"max diff: {max_diff:.4f} ms")