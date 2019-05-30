from resources import send_credential, portic_signal
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time

# get the webcam:  
cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)
time.sleep(2)

font = cv2.FONT_HERSHEY_SIMPLEX

try:
    while(cap.isOpened()):
        ret, frame = cap.read()
        im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      
        decodedObjects = pyzbar.decode(im)
        for obj in decodedObjects:
            portic_signal(24)
            data = obj.data.decode().split(':')
            send_credential(data[0], data[1])
            time.sleep(2)
except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
