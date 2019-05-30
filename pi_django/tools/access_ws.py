import asyncio
import websockets

connected = set()

async def transfer(websocket, path):
    connected.add(websocket)

    try:
        msg = await websocket.recv()
        try:
            await asyncio.wait([ws.send(msg) for ws in connected])
        finally:
            connected.remove(websocket)
    except websockets.exceptions.ConnectionClosed:
        connected.clear()

start_server = websockets.serve(transfer, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
