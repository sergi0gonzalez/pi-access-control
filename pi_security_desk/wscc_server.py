from cc_citizen_data import Citizen_Data, CC_NOT_PRESENT
from wand.image import Image
import asyncio
import websockets
import sys
import time
import json
import io

c = Citizen_Data()
connected = set()

async def send_cc_data(websocket, path):
    connected.add(websocket)

    while True:
        try:
            c.open_session()
            break
        except CC_NOT_PRESENT:
            time.sleep(1)
    name, id_number = c.get_name_id()
    photo_bytes = c.get_photo_bytes()

    with Image(blob=photo_bytes) as img:
        png_photo = img.convert('png')

    msg = {'name': name, 'civilian_id': id_number, 'image_bytes': png_photo.make_blob().hex()}

    await websocket.send(json.dumps(msg))
    await asyncio.sleep(10)


start_server = websockets.server.serve(send_cc_data, 'localhost', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
