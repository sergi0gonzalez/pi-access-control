from chirpsdk import ChirpConnect, CallbackSet
from resources import send_credential

class Callbacks(CallbackSet):

    def on_received(self, payload, channel):
        if payload is None:
            print('Decode failed!')
        else:
            payload = ''.join([chr(tmp) for tmp in payload])
            data = payload.split(':')
            send_credential(data[0], data[1])


chirp = ChirpConnect()
chirp.set_callbacks(Callbacks())

chirp.start(send=False, receive=True)
try:
    while(True):
        pass
except KeyboardInterrupt:
    chirp.stop()
    print('Exiting...')
