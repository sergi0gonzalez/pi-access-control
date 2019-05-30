from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from cryptography.hazmat.primitives.hashes import SHA256
from chirpsdk import ChirpConnect
import time

chirp = ChirpConnect()

chirp.start(send=True, receive=False)

key = b'}\x11\xf4b\xf8\xc8$\x01Hh\x95m\xa8\xb0\x1a~\xbb-\x81\x04\xc7\xb8\xa4%\x86\x87\xda\\ja\x92R'
totp = TOTP(key, 8, SHA256(), 30, backend=default_backend())
totp_value = totp.generate(time.time())
identifier = 'test@ua.pt:'+totp_value.decode()

payload = chirp.new_payload(identifier.encode())

chirp.send(payload, blocking=True)
chirp.stop()
