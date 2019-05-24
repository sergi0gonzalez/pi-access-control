from resources import send_qrcode_credential, portic_signal
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time

# get the webcam:  
cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)
time.sleep(2)

try:
    while(cap.isOpened()):
        ret, frame = cap.read()
        im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      
        decodedObjects = pyzbar.decode(im)
        for obj in decodedObjects:
            #portic_signal(24)
            data = obj.data.decode().split(':')
            send_qrcode_credential(data[0], data[1])
            print('end')
            decodedObjects = []
            break
        cv2.waitKey(5)
except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
