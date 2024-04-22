from multiprocessing import Process
import time
import subprocess
import MQTT
import Internet
import data
import log
import caculation


def work1():  # MQTT broker
    try:
        # Once we have told the MQTT.client to connect, let the MQTT.client object run itself
        MQTT.client.loop_forever()
        MQTT.client.disconnect()

    except Exception as e:
        log.addError(e)
        time.sleep(1)
        work1()


def work2():  # MQTT client
    while True:
        try:
            MQTT.sendRequest()
        except Exception as e:
            log.addError(e)


internetInitSuccessful = False
def work3():  # Internet
    global internetInitSuccessful
    while True:
        try:
            if internetInitSuccessful:
                Internet.loop()
            else:
                internetInitSuccessful = Internet.init()
        except Exception as e:
            log.addError(e)


def work4():  # Status
    timestamp_2 = 0
    while True:
        try:
            if (time.time() - timestamp_2) > 1:
                # print("renew work")
                data.timeModule().renewALLStatus()
                timestamp_2 = time.time()
        except Exception as e:
            log.addError(e)

        time.sleep(0.2)



def work6():  # Calculation
    while True:
        try:
            caculation.loop()
            time.sleep(0.05)
        except Exception as e:
            log.addError(e)

        time.sleep(0.2)


def init():
    log.init()
    MQTT.init()
    # caculation.init()
    global internetInitSuccessful
    internetInitSuccessful = Internet.init(True)

    data.outer().setWarning("")
    data.Box_1().setRFID("")


if __name__ == '__main__':
    init()

    processlist = [Process(target=work1),
                   Process(target=work2),
                   Process(target=work3),
                   Process(target=work4),
                   Process(target=work6)]
    # Process(target=work5)]

    for t in processlist:
        t.start()

    for t in processlist:
        t.join()
