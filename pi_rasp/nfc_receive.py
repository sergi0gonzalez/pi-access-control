import socket
import sys
from resources import send_nfc_credential

def recv_bytes(the_socket):
	total_data=[]
	while True:
		data = the_socket.recv(8192)
		if not data: break
		total_data.append(data)
	return total_data

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', 10000)
	print('starting up on {} port {}'.format(*server_address))
	sock.bind(server_address)
	sock.listen(1)

	while True:
		print('waiting for a connection')
		conn, client_address = sock.accept()
		try:
			print('connection from', client_address)
			all_data = b''
			while(True):
				dt = conn.recv(65535)
				all_data += dt
				if len(dt)<65535:
					break
			
			all_data = all_data.decode("utf-8")
			print(all_data)
			data = all_data.split(":")
			send_nfc_credential(data[0], data[1])	
		finally:
			print('connection closed')
			conn.close()
	
