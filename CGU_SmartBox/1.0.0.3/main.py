from multiprocessing import Process
import time
import MQTT

print("internet called from main.py")

import Internet
import data
import log
import caculation


InternetUser = Internet.Internet()


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
                InternetUser.loop()
            else:
                print("Internet initial from work3")
                internetInitSuccessful = InternetUser.init()
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


import subprocess
import line_server
def work7():  # Calculation
    while True:
        try:
            line_server.main()
            # subprocess.run('/Users/slothsmba/Documents/Codes/Python/pythonProject/CGU_SmartBox/1.0.0.3/line_server.py')
            # reply = subprocess.run('python/home/pi/Desktop/line_code/line_server.py')
            # print(reply)
        except Exception as e:
            log.addError(e)

        time.sleep(0.2)


def init():
    log.init()
    MQTT.init()
    # caculation.init()
    global internetInitSuccessful
    print("Internet initial from init()")
    internetInitSuccessful = InternetUser.init(True)

    data.outer().setWarning("")
    data.Box_1().setRFID("")


if __name__ == '__main__':
    init()

    processlist = [Process(target=work1),
                   Process(target=work2),
                   Process(target=work3),
                   Process(target=work4),
                   Process(target=work6),
                   Process(target=work7)]
    # Process(target=work5)]

    for t in processlist:
        t.start()

    for t in processlist:
        t.join()
