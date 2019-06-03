from cc_citizen_data import Citizen_Data, CC_NOT_PRESENT, DEVICE_REMOVED
import asyncio
import websockets
import time
import json

async def send_cc_data(websocket, path):
    c = Citizen_Data()

    while True:
        try:
            c.open_session()
            print('After open')
            break
        except (CC_NOT_PRESENT, DEVICE_REMOVED):
            time.sleep(1)
    name, id_number = c.get_name_id()
    photo_bytes = c.get_photo_png_bytes()

    msg = {'name': name, 'civilian_id': id_number, 'image_bytes': photo_bytes.hex()}

    await websocket.send(json.dumps(msg))
    await asyncio.sleep(2)


start_server = websockets.server.serve(send_cc_data, 'localhost', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
