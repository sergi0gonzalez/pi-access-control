from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from cryptography.hazmat.primitives.hashes import SHA256
from chirpsdk import ChirpConnect
import time

chirp = ChirpConnect()

chirp.start(send=True, receive=False)

key = b'\xc9~I)\xef@\x1f\x16W\xd7\xe9)V\x01\x84d\x97\x9a\xe8K\xc2(\xb2\xac?c\xc5\xf1\x9c\xb0@\x12'
totp = TOTP(key, 8, SHA256(), 30, backend=default_backend())
totp_value = totp.generate(time.time())
identifier = 'teste@2:'+totp_value.decode()

payload = chirp.new_payload(identifier.encode())

chirp.send(payload, blocking=True)
chirp.stop()
