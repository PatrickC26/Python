import os
import sys
from datetime import datetime

import setting

location = setting.fileLocation + 'log/'


def addlog(inData: str):
    try:
        inData = (datetime.now()).strftime('%Y/%m/%d %H:%M:%S.%s') + ' -> ' + inData
        print(inData)
        with open(location, "a") as outputFile:
            outputFile.write(inData + '\n')
        return True
    except Exception as e:
        print(e)
    return False


def addError(e: Exception):
    try:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        outS = "[ERROR] " + str(exc_type)[8: -2] + " @ -> "
        for i in range(1, len(os.path.split(exc_tb.tb_frame.f_code.co_filename))):
            fName = os.path.split(exc_tb.tb_frame.f_code.co_filename)[i]
            outS = outS + str(fName)[0: -3] + ":" + str(exc_tb.tb_lineno) + " > "

        outS = outS[0: -3]
        # print(outS)
        addlog(outS)
    except Exception as e1:
        print(e1)
    return False


def init():
    print("Starting Log Service")
    global location
    global location_status
    try:
        location = location + "log_python_" + (datetime.now()).strftime('%Y-%m-%d_%H-%M') + ".txt"
        with open(location, "x") as outputFile:
            outputFile.write('')
        addlog("Log Service Initial Successfull")
    except Exception as e:
        if "FileExistsError" in str(e.__class__):
            addlog("\n\n----------------------------------------------------------\n")
            addlog("ReStart Recording")
            addlog("Log Service Initial Successfull")
        else:
            print("Error with log")
