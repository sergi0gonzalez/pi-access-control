from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from resources import send_rfid_credential
import time

pn532 = Pn532_i2c()
pn532.SAMconfigure()

while True:
    card_data = pn532.read_mifare()
    tmp = bytes(card_data.get_data())
    tag = tmp.hex()[14:]
    #print(tag)
    send_rfid_credential(tag)
    time.sleep(1)
