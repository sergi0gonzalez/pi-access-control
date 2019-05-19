import asyncio
import json
import logging
import sys
import websockets
import json

import PyKCS11
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
import citizen_card


from base64 import b64decode

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def json_to_payload(message):
    return json.dumps(message)


async def send_cc_data(websocket):
    while (True):
        await asyncio.sleep(1)
        message = citizen_card.get_user_name()
        await websocket.send(json_to_payload(message))
        logger.debug(f'Sent message to server: {message}')


async def consumer(message):
    json_message = json.loads(message)
    logger.debug(f'Server message received: {json_message}')

    if (json_message['event'] == 'beep'):
        print("\a")


async def consumer_handler(websocket):
    async for message in websocket:
        await consumer(message)


async def handler(uri, client_id):
    async with websockets.connect(uri) as websocket:
        message = {
            'event': 'authentication',
            'client_id': client_id,
            'client_mode': 'desktop'
        }

        await websocket.send(json_to_payload(message))

        consumer_task = asyncio.ensure_future(
            consumer_handler(websocket))
        producer_task = asyncio.ensure_future(
            send_cc_data(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        handler('ws://localhost:8000/ws', sys.argv[1])
    )