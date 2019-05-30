import asyncio
import json
import sys
import websockets
import json
import PyKCS11
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from base64 import b64decode
import socket

async def send_cc_data(websocket, path):
	while (True):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(("127.0.0.1",5555))
		client.sendall(b"query\n")
		print('query sent')
		r = b''
		while(True):
			rp = client.recv(65535)
			r+=rp
			if len(rp)<65535:
				break
		if not r:
			print("[-] Not Received")
		else:
			response = r.decode("utf-8")
			await websocket.send(response)
		client.close()
		await asyncio.sleep(10)



if __name__ == '__main__':
	start_server = websockets.serve(send_cc_data, '127.0.0.1', 5678)
	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()
	
	

