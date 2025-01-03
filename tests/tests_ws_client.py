import allure
import asyncio
import json
import pytest
import websockets


@pytest.fixture
def uri():
    return "wss://ws-feed.exchange.coinbase.com"


@allure.title("WS Connection")
@allure.description("Test to verify if the first message is a subscription confirmation.")
@pytest.mark.asyncio
async def test_first_message_is_subscription(uri):
    subscribe_message = {
        "type": "subscribe",
        "channels": [
            {
                "name": "heartbeat",
                "product_ids": ["ETH-EUR"]
            }
        ]
    }

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

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(subscribe_message))
        
        response = await websocket.recv()

        message = json.loads(response)

        assert message['type'] == 'subscriptions', f"Unexpected message type: expected 'subscriptions, actual: {message['type']}"
        assert 'channels' in message, "Expected an channels field in response"
        assert message == expected_message, f"Message is not expected, current message is {message}"


@allure.title("WS connection with invalid product ID")
@allure.description("Test to validate behavior when subscribing with an invalid product ID.")
@pytest.mark.asyncio
async def test_invalid_product_id(uri):
    uri = "wss://ws-feed.exchange.coinbase.com"
    invalid_subscribe_message = {
        "type": "subscribe",
        "channels": [
            {
                "name": "heartbeat",
                "product_ids": ["INVALID-ID"]
            }
        ]
    }

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(invalid_subscribe_message))
        
        response = await websocket.recv()

        error_message = json.loads(response)

        assert error_message['type'] == 'error', f"Unexpected message type: expected 'error, actual: {error_message['type']}"
        assert 'message' in error_message, "Expected an error message field in response"
        assert 'Failed to subscribe' in error_message['message'], f"Unexpected error message: {error_message['message']}"
        assert 'is not a valid product' in error_message['reason'], f"Unexpected error reason: {error_message['reason']}"


@allure.title("Heartbeat validation")
@allure.description("Test to verify the format of the second message received (expected: heartbeat message).")
@pytest.mark.asyncio
async def test_second_message_format(uri):
    uri = "wss://ws-feed.exchange.coinbase.com"
    subscribe_message = {
        "type": "subscribe",
        "channels": [
            {
                "name": "heartbeat",
                "product_ids": ["ETH-EUR"]
            }
        ]
    }

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(subscribe_message))
        
        # should be ignored, there is subscription confirmation
        await websocket.recv()
        
        second_response = await websocket.recv()
        second_message = json.loads(second_response)

        expected_fields = {
            "type": str,
            "last_trade_id": int,
            "product_id": str,
            "sequence": int,
            "time": str
        }

        assert second_message['type'] == 'heartbeat', f"Unexpected message type: expected 'heartbeat, actual: {second_message['type']}"

        for field, field_type in expected_fields.items():
            assert field in second_message, f"Field '{field}' is missing in the message."
            assert isinstance(second_message[field], field_type), f"Field '{field}' is not of type {field_type.__name__}."

        assert second_message['product_id'] == 'ETH-EUR', "The 'product_id' field is not 'ETH-EUR'."