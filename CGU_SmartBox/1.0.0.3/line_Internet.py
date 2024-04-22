import socket
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import time
import requests
import json
import datetime

import log
import data
import setting

fileLocation = setting.fileLocation

debug = False
# debug = True


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


lineNoticeArray = ["" for _ in range(0)]

lineNotifyTime = [datetime.datetime.now() for _ in range(0)]


def line_id2token( code, redirect_uri):
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
        else:
            print(response.text)
    except Exception as e:
        log.addError(e)
    return ""


def line_notify( token, msg):
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


def httpCheck( printing=False):
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


def firebaseGET( dic: str):
    try:
        ref = db.reference(dic)
        returnS = str(ref.get(dic))
        return returnS[returnS.index("'") + 1: returnS.rindex(",") - 1]
    except Exception as e:
        log.addError(e)
        return ""


def firebasePUT( dic: str, dataS):
    try:
        # if "/" in dataS:
        #     dataS = dataS.replace("/", "-")
        dataS = str(dataS)
        ref = db.reference(dic)
        ref.set(dataS)
    except Exception as e:
        log.addError(e)


def init( printing=False):
    global lineNoticeArray, lineNotifyTime

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

        longtime = datetime.datetime.now() + datetime.timedelta(hours=100, minutes=0, seconds=0)
        lineNoticeArray.append("ZtA7tY747TIICjLyuhC9uNSPtEGwuYY8uyVJzNInAxi")  # Test token
        lineNoticeArray.append("onwpc2MGbQO6jbh7etqHqz9NBOoh4aWfBYiaQNtZ5bx")  # Test token
        lineNotifyTime.append(longtime)
        lineNotifyTime.append(longtime)

        print(lineNoticeArray)
        print(lineNotifyTime)

        return True
    except Exception as e:
        log.addError(e)
        return False


millis_1sec = 0


def loop():
    global millis_1sec
    try:
        timeStamp = datetime.datetime.now().timestamp()

        # 0.5 sec repeat
        # print(lineNoticeArray)

        sthCleaned = False
        for i in range(len(lineNotifyTime) - 1, -1, -1):
            oktime = datetime.datetime.now() + datetime.timedelta(hours=0, minutes=-10, seconds=0)
            if lineNotifyTime[i] < oktime:
                print("delete :", lineNoticeArray[i])
                line_notify(lineNoticeArray[i], "權杖已過期，感謝您的蒞臨")
                lineNoticeArray.pop(i)
                lineNotifyTime.pop(i)
                sthCleaned = True

        if sthCleaned:
            print(lineNoticeArray)
            print(lineNotifyTime)

        if data.outer().getWarning() != "":
            print("warning: ", data.outer().getWarning(), ' to ', lineNoticeArray)
            for i in lineNoticeArray:
                line_notify(i, data.outer().getWarning())

            data.outer().setWarning('')

        # 1 sec repeat
        if ((timeStamp - millis_1sec) > 1) | (millis_1sec == 0):
            if httpCheck():
                data.outer().setInternetCheck(True)
            else:
                data.outer().setInternetCheck(False)

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


def firebase_listener__LINE( msgA):
    try:
        msg = msgA.data
        if msg != '':
            # if debug:
            print('LINE msg: ' + msg)
            msg = msg[msg.index(','):]
            id = msg.split(',')[1]
            redirect_uri = msg.split(',')[2].split('?')[0]
            print(redirect_uri)
            token = line_id2token(id, redirect_uri)
            if (token is not None) & (token != ''):
                lineNoticeArray.append(token)
                lineNotifyTime.append(datetime.datetime.now())
                line_notify(lineNoticeArray[-1], "連線成功！")
                firebasePUT('user/line', '')
            else:
                token = firebaseGET('user/token').split(',')[0]
                if (token is not None) & (token != ''):
                    lineNoticeArray.append(token)
                    lineNotifyTime.append(datetime.datetime.now())
                    line_notify(lineNoticeArray[-1], "連線成功！")
                else:
                    print("Error with receiving token")

            print(lineNoticeArray)
            print(lineNotifyTime)

    except Exception as e:
        log.addError(e)


def firebase_listener():
    db.reference('user/line').listen(firebase_listener__LINE)



if False:
# if True:
    if __name__ == '__main__':
        debug = True
        log.init()
        print("Starting Init Func")
        internetInitSuccessful = init(True)
        print('internetInitSuccessful: ', internetInitSuccessful)
        print(lineNoticeArray)
        while 1:
            try:
                if internetInitSuccessful:
                    loop()
                else:
                    internetInitSuccessful = init()
            except Exception as e:
                log.addError(e)




