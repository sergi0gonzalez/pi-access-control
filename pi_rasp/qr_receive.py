from resources import send_qrcode_credential, portic_signal
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time

# get the webcam:  
cap = cv2.VideoCapture(0)

#cap.set(3,640)
cap.set(3,1024)
#cap.set(4,480)
cap.set(3, 768)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
time.sleep(1)

ignore = True

try:
    while(cap.isOpened()):
        ret, frame = cap.read()
        im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      
        decodedObjects = pyzbar.decode(im)
        if not ignore and len(decodedObjects) == 0:
            ignore = True
        if ignore and len(decodedObjects) > 0:
            portic_signal(24, 'empty')
            for obj in decodedObjects:
                data = obj.data.decode().split(':')
                send_qrcode_credential(data[0], data[1])
                break
            ignore = False
            time.sleep(1)
except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
