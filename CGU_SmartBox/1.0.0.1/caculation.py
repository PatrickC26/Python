import numpy as np

try:
    import picamera
except:
    pass
import data
import log

RFID = ["191-174-71-3", "179-46-85-3", "94-146-43-3", "245-56-157-65"]
TAG = ["ABC", "DEF", "GREF", "OK"]


lastRFIDValue = ""
def loop():
    if data.Box_1().getRFID() == lastRFIDValue:
        index = RFID.index(data.Box_1().getRFID())
        if index < 4:
            data.Box_1().setMSG(TAG[index])
        else:
            data.Box_1().setMSG("NO")
