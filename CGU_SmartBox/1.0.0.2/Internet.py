import socket

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import time
import requests
import json
import log
import datetime
import data
import setting

fileLocation = setting.fileLocation

debug = False
# debug = True

iptable = [[0 for j in range(0)] for i in range(2)]  # [2][0]
iptable_i = 0

lineNoticeArray = ["" for _ in range(0)]
lineNotifyTime = [datetime.datetime.now() for _ in range(0)]

longtime = datetime.datetime.now() + datetime.timedelta(hours=100, minutes=0, seconds=0)
lineNoticeArray.append("ZtA7tY747TIICjLyuhC9uNSPtEGwuYY8uyVJzNInAxi") # Test token
lineNoticeArray.append("ZtA7tY747TIICjLyuhC9uNSPtEGwuYY8uyVJzNInAxi") # Test token
lineNotifyTime.append(longtime)
lineNotifyTime.append(longtime)

print(lineNoticeArray)
print(lineNotifyTime)

def line_id2token(code, redirect_uri):
    try:
        url = "https://notify-bot.line.me/oauth/token"
        payload = {"code": code,  # code change only use onece
                   "grant_type": "authorization_code",
                   "redirect_uri": redirect_uri,
                   "client_id": "8WoeLWgF3I2KpSsr4RH8hX",
                   "client_secret": "nEdlAN1lHwUjAahutASBh2hBN4knjr7HZkmhWE6qM0D"}

        response = requests.post(url, data=payload)
        if str2json(response.text)['status'] == 200:
            return str2json(response.text)['access_token']
    except Exception as e:
        log.addError(e)
    return ""


def line_notify(token, msg):
    try:
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload, timeout=2)
        if debug:
            print('line sending msg: ' + msg)
            print('line status code: ' + str(r.status_code))
        return r.status_code == 200
    except Exception as e:
        log.addError(e)
        return False


def httpGET(url):
    try:
        response = requests.get(url, timeout=2)
        # Check if the request was successful
        if debug:
            print('httpGET with response code: ' + str(response.status_code))
        if response.status_code == 200:
            return str(response.json())
        else:
            log.addlog(
                "[Internet] ERROR in httpGET, with error code :" + str(response.status_code) + ", with url:" + url)
            return 'ERROR' + str(response.status_code)
    except requests.exceptions.ReadTimeout as e:
        log.addError(e)
        try:  # Second try
            response = requests.get(url, timeout=2)
            # Check if the request was successful
            if debug:
                print('httpGET second chance with response code: ' + str(response.status_code))
            if response.status_code == 200:
                return str(response.json())
        except requests.exceptions.ReadTimeout as e1:
            log.addError(e1)


def httpCheck(printing=False):
    try:
        conn = socket.create_connection((socket.gethostbyname("www.google.com"), 80), timeout=0.5)
        conn.close()
        return True
    except requests.exceptions.ConnectionError as e:
        if printing:
            print("No Connection.. (Connection)")
        return False
    except requests.exceptions.ReadTimeout as e:
        if printing:
            print("No Connection.. (ReadTimeout)")
        return False
    except Exception as e:
        if printing:
            print(e)
        return False


# def httpPUT(url, dataS: str):
#     response = requests.put(url, dataS, timeout = 2)
#     # Check the response status code
#     if response.status_code != 200:
#         print('httpPUT: errorCode ')
#         print(response.status_code)
#     return response.status_code == 200


def firebaseGET(dic: str):
    try:
        ref = db.reference(dic)
        returnS = str(ref.get(dic))
        return returnS[returnS.index("'") + 1: returnS.rindex(",") - 1]
    except Exception as e:
        log.addError(e)
        return ""


def firebasePUT(dic: str, dataS):
    try:
        # if "/" in dataS:
        #     dataS = dataS.replace("/", "-")
        dataS = str(dataS)
        ref = db.reference(dic)
        ref.set(dataS)
    except Exception as e:
        log.addError(e)


def firebaseUpdate(RFID, RFID_Time, humidity, humidityTime, temperature, temperatureTime, voltage, voltageTime,
                   humidity2, humidityTime2, temperature2, temperatureTime2,
                   humidity3, humidityTime3, temperature3, temperatureTime3, water, waterTime, speed, speedTime):
    try:
        ref = db.reference('info')
        ref.update({
            "Box_1": {
                "RFID": {
                    "value": str(RFID),
                    "time": RFID_Time
                },
                "humidity": {
                    "value": str(humidity),
                    "time": humidityTime
                },
                "temperature": {
                    "value": str(temperature),
                    "time": temperatureTime
                },
                "voltage": {
                    "value": str(voltage),
                    "time": voltageTime
                },
                'time': str(data.timeModule().getBox1Status()) + "," + data.timeModule().getBox1Time()
            },
            "Box_2": {
                "humidity": {
                    "value": str(humidity2),
                    "time": humidityTime2
                },
                "temperature": {
                    "value": str(temperature2),
                    "time": temperatureTime2
                },
                'time': str(data.timeModule().getBox2Status()) + "," + data.timeModule().getBox2Time()
            },
            "Box_3": {
                "humidity": {
                    "value": str(humidity3),
                    "time": humidityTime3
                },
                "temperature": {
                    "value": str(temperature3),
                    "time": temperatureTime3
                },
                "water": {
                    "value": str(water),
                    "time": waterTime
                },
                "speed": {
                    "value": str(speed),
                    "time": speedTime
                },
                'time': str(data.timeModule().getBox3Status()) + "," + data.timeModule().getBox3Time()
            }
        })
    except Exception as e:
        log.addError(e)


def nowTime():
    now = datetime.datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    return time_string


def intTime():
    t = nowTime().replace("-", '').replace(':', '').replace(' ', '')
    return t[0: t.index('.')]


def str2json(str_data: str):
    str_data = str_data.replace("'", '"')
    str_data = str_data.replace("[", '')
    str_data = str_data.replace("]", '')
    str_data = str_data.replace('False', "0")
    str_data = str_data.replace('Ture', "1")
    return json.loads(str_data)


def init(printing=False):
    retryRemain = 5
    if printing:
        print("Checking Internet")

    while retryRemain > 0:
        if not httpCheck(printing):
            if printing:
                print("No Internet Currently, retrying... remain: ", retryRemain)
            time.sleep(0.1)
            retryRemain -= 1
        else:
            break

    if retryRemain <= 0:
        if printing:
            print("Internet FAILED")
        return False

    print("Starting Internet Service")

    try:
        # Load the Firebase API key from a file
        cred = credentials.Certificate(fileLocation + "src/key.json")
        # Initialize the Firebase client
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://smartbox-mbswai-default-rtdb.firebaseio.com/',
            'httpTimeout': 3
        })
        firebase_listener()
        log.addlog("Internet Service Initial Successful")
        return True
    except Exception as e:
        log.addError(e)
        return False


millis_10min = 0
millis_1sec = 0


def loop():
    try:
        global millis_10min
        global millis_1sec

        timeStamp = datetime.datetime.now().timestamp()

        # 0.5 sec repeat

        for i in range(len(lineNotifyTime) - 1, -1, -1):
            oktime = datetime.datetime.now() + datetime.timedelta(hours=0, minutes=-10, seconds=0)
            if lineNotifyTime[i] < oktime:
                line_notify(lineNoticeArray[i], "權杖已過期，感謝您的蒞臨")
                lineNoticeArray.pop(i)
                lineNotifyTime.pop(i)

        if data.outer().getWarning() != "":
            for i in lineNoticeArray:
                line_notify(i, data.outer().getWarning())
            data.outer().setWarning('')

            print(lineNoticeArray)
            print(lineNotifyTime)

        # 1 sec repeat
        if ((timeStamp - millis_1sec) > 1) | (millis_1sec == 0):
            if httpCheck():
                data.outer().setInternetCheck(True)
            else:
                data.outer().setInternetCheck(False)

            firebaseUpdate(data.Box_1().getRFID(), data.Box_1().getRFIDTime(),
                           data.Box_1().getHumidity(), data.Box_1().getHumidityTime(),
                           data.Box_1().getTemperature(), data.Box_1().getTemperatureTime(),
                           data.Box_1().getVoltage(), data.Box_1().getVoltageTime(),
                           data.Box_2().getHumidity(), data.Box_2().getHumidityTime(),
                           data.Box_2().getTemperature(), data.Box_2().getTemperatureTime(),
                           data.Box_3().getHumidity(), data.Box_3().getHumidityTime(),
                           data.Box_3().getTemperature(), data.Box_3().getTemperatureTime(),
                           data.Box_2().getWater(), data.Box_2().getWaterTime(),
                           data.Box_3().getSpeed(), data.Box_3().getSpeedTime())

            millis_1sec = timeStamp

        # dynamic delay
        try:
            delayTime = 300 + timeStamp - datetime.datetime.now().timestamp()
            if delayTime > 0:
                time.sleep(delayTime / 1000.0)
                # print('delayTime :' + str(delayTime))
        except Exception as e:
            log.addError(e)

    except Exception as e:
        log.addError(e)


def firebase_listener__LINE(msgA):
    try:
        msg = msgA.data
        if msg != '':
            if debug:
                print('LINE msg: ' + msg)
            msg = msg[msg.index(','):]
            id = msg.split(',')[1]
            redirect_uri = msg.split(',')[2].split('?')[0]
            print(redirect_uri)
            token = line_id2token(id, redirect_uri)
            if (token is not None) | (token != ''):
                lineNoticeArray.append(token)
                lineNotifyTime.append(datetime.datetime.now())
                line_notify(lineNoticeArray[-1], "連線成功！")
                print("get token with: " + token)
                firebasePUT('user/line', '')
            else:
                token = firebaseGET('user/token').split(',')[0]
                lineNoticeArray.append(token)
                lineNotifyTime.append(datetime.datetime.now())
                print("get token from firebase user: " + token)

    except Exception as e:
        log.addError(e)


def firebase_listener__Servo(msgA):
    try:
        msg = msgA.data
        if msg != '':
            if debug:
                print('Servo : ' + msg)
            data.Box_2().setServo(int(msg))
    except Exception as e:
        log.addError(e)


def firebase_listener__RFID_msg(msgA):
    try:
        msg = msgA.data
        if msg != '':
            if debug:
                print('Servo : ' + msg)
            data.Box_1().setRFIDinfo(msg)
    except Exception as e:
        log.addError(e)


def firebase_listener():
    db.reference('user/line').listen(firebase_listener__LINE)
    db.reference('control/servo').listen(firebase_listener__Servo)
    db.reference('control/RFIDInfo').listen(firebase_listener__RFID_msg)


# if False:
if True:
    if __name__ == '__main__':
        debug = True
        log.init()
        print("Starting Init Func")
        internetInitSuccessful = init()
        print(internetInitSuccessful)
        while 1:
            try:
                if internetInitSuccessful:
                    loop()
                else:
                    internetInitSuccessful = init()
            except Exception as e:
                log.addError(e)

# print(init())
# while 1:
#     try:
#         print(lineNoticeArray)
#         for i in lineNoticeArray:
#             line_notify(i, data.outer().getWarning())
#             line_notify_img(i, "/Users/slothsmba/Desktop/a.png")
#     except Exception as e:
#         log.addError(e)
