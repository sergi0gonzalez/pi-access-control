from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from cryptography.hazmat.primitives.hashes import SHA256
from chirpsdk import ChirpConnect
import time

chirp = ChirpConnect()

chirp.start(send=True, receive=False)

key = b'\r1\x01\x8c\xf3\xe7!@\xaf\xf5\x16\xbc\xb4\xba7\x9bx\xf2\x11\xe2\x9f\xeaW@{n\x10\x96h\xe0\xc6\x0c'
totp = TOTP(key, 8, SHA256(), 30, backend=default_backend())
totp_value = totp.generate(time.time())
identifier = 'test@ua.pt:'+totp_value.decode()

payload = chirp.new_payload(identifier.encode())

chirp.send(payload, blocking=True)
chirp.stop()
