import data
import log


def renewLog(topic, inHead, inData):
    try:
        log.addlog("[Data Renew] " + inHead + ":" + str(inData))
    except Exception as e:
        log.addError(e)

    try:
        if topic == 'A':
            allHead = ['t','h','v','r']
            for i in allHead:
                if i == inHead:
                    print("OK")
                    return {
                        't': lambda x: data.Box_1().setTemperature(int(float(inData))),
                        'h': lambda x: data.Box_1().setHumidity(int(float(inData))),
                        'v': lambda x: data.Box_1().setVoltage(int(float(inData))),
                        'r': lambda x: data.Box_1().setRFID(inData),
                    }[inHead](inData)
        elif topic == 'B':
            allHead = ['t', 'h', 'v', 'r']
            for i in allHead:
                if i == inHead:
                    print("OK")
                    return {
                        't': lambda x: data.Box_2().setTemperature(int(float(inData))),
                        'h': lambda x: data.Box_2().setHumidity(int(float(inData))),
                        'v': lambda x: data.Box_2().setVoltage(int(float(inData))),
                        'r': lambda x: data.Box_2().setWater(int(float(inData))),
                    }[inHead](inData)
        elif topic == 'C':
            allHead = ['t', 'h', 'v', 's']
            for i in allHead:
                if i == inHead:
                    print("OK")
                    return {
                        't': lambda x: data.Box_3().setTemperature(int(float(inData))),
                        'h': lambda x: data.Box_3().setHumidity(int(float(inData))),
                        'v': lambda x: data.Box_3().setVoltage(int(float(inData))),
                        's': lambda x: data.Box_3().setSpeed(int(float(inData))),
                    }[inHead](inData)

    except Exception as e:
        log.addError(e)


def dataprocess(topic, inS):
    try:
        value = ""
        head = inS[0]
        if not head.isascii():
            while not head.isascii():
                inS = inS[1:]
                head = ord(inS[0])
        else:
            if inS[-1] == '%':
                value = (inS[1:-1])
            else:
                while not inS[-1] == '%':
                    inS = inS[0:-1]
                    value = (inS[1:-1])
        # print("  Value of: " + head + "  Value is: " + (value))
        renewLog(topic, head, value)
    except Exception as e:
        log.addError(e)
