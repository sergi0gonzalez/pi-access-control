from chirpsdk import ChirpConnect, CallbackSet
chirp = ChirpConnect()
chirp.start(send=True, receive=True)

identifier='Hello'
payload = bytearray([ord(ch) for ch in identifier])
chirp.send(payload, blocking=True)
