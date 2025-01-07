import allure
import pytest
import logging

from src.ws_utils import connect_and_subscribe, read_messages
from src.ws_client import ws_reader


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.fixture
def uri():
    return "wss://ws-feed.exchange.coinbase.com"


@pytest.fixture
def subscribe_message():
    subscribe_message = {
        "type": "subscribe",
        "channels": [
            {
                "name": "heartbeat",
                "product_ids": ["ETH-EUR"]
            }
        ]
    }
    return subscribe_message


@allure.title("WS Connection")
@allure.description("Test to verify if the first message is a subscription confirmation.")
@pytest.mark.asyncio
async def test_first_message_is_subscription(uri, subscribe_message):        
    expected_message = {
        "type": "subscriptions",
        "channels": [
            {
                "name": "heartbeat",
                "product_ids": ["ETH-EUR"],
                "account_ids": None
            }
        ]
    }
    
    websocket = await connect_and_subscribe(name="test", subscribe_message=subscribe_message)
    received_messages = await read_messages(websocket=websocket, total_messages=3)

    assert received_messages[0] == expected_message, f"received message is:  '{received_messages[0]}' "
    assert received_messages[0]['type'] == 'subscriptions', f"Unexpected message type: expected 'subscriptions, actual: {received_messages[0]['type']}"
    assert 'channels' in received_messages[0], "Expected an channels field in response"
    assert received_messages[0] == expected_message, f"Message is not expected, current message is {received_messages[0]}"


@allure.title("WS connection with invalid product ID")
@allure.description("Test to validate behavior when subscribing with an invalid product ID.")
@pytest.mark.asyncio
async def test_invalid_product_id(uri):
    invalid_subscribe_message = {
        "type": "subscribe",
        "channels": [
            {
                "name": "heartbeat",
                "product_ids": ["INVALID-ID"]
            }
        ]
    }

    websocket = await connect_and_subscribe(name="test", subscribe_message=invalid_subscribe_message)
    received_messages = await read_messages(websocket=websocket, total_messages=3)

    assert received_messages[0]['type'] == 'error', f"Unexpected message type: expected 'error, actual: {received_messages[0]['type']}"
    assert 'message' in received_messages[0], "Expected an error message field in response"
    assert 'Failed to subscribe' in received_messages[0]['message'], f"Unexpected error message: {received_messages[0]['message']}"
    assert 'is not a valid product' in received_messages[0]['reason'], f"Unexpected error reason: {received_messages[0]['reason']}"


@allure.title("Heartbeat validation")
@allure.description("Test to verify the format of the second message received (expected: heartbeat message).")
@pytest.mark.asyncio
async def test_second_message_format(uri, subscribe_message):
    websocket = await connect_and_subscribe(name="test", subscribe_message=subscribe_message)
    received_messages = await read_messages(websocket=websocket, total_messages=3)

    expected_fields = {
        "type": str,
        "last_trade_id": int,
        "product_id": str,
        "sequence": int,
        "time": str
    }

    assert received_messages[1]['type'] == 'heartbeat', f"Unexpected message type: expected 'heartbeat, actual: {received_messages[1]['type']}"

    for field, field_type in expected_fields.items():
        assert field in received_messages[1], f"Field '{field}' is missing in the message."
        assert isinstance(received_messages[1][field], field_type), f"Field '{field}' is not of type {field_type.__name__}."

    assert received_messages[1]['product_id'] == 'ETH-EUR', "The 'product_id' field is not 'ETH-EUR'."