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

lineNoticeArray = ["" for z in range(0)]


# lineNoticeArray.append("MgNFuUrwed1JJ8DdoeqqOX6FlGWF3bxNxNkug76pe2t") # Test token


def line_id2token(code):
    try:
        url = "https://notify-bot.line.me/oauth/token"

        payload = {"code": code,  # code change only use onece
                   "grant_type": "authorization_code",
                   "redirect_uri": "https://willy01010.github.io/newwebsite/root/setting.html",
                   "client_id": "jlFBh91sUAOfcA2Re0AmsU",
                   "client_secret": "fEimljVLzzSgKxAePxIYaDUpGXrU4DD8ZHDZYuR2cQ4"}

        response = requests.post(url, data=payload)
        if str2json(response.text)['status'] == 200:
            return str2json(response.text)['access_token']
    except Exception as e:
        log.addError(e)
    return ""


def loadLineUser():
    # load line user
    UIDList = firebaseGET('ManageUser/UIDList')
    # UIDList = '_5ewSBItLNySuniNLI5h8Gwxhwha2,_ure9Adih1ZbdzswvnVZUdT79Wsx2,_bAU0qU8e7jXnq6ZDDjffqXVVxhv2,_Jd6P5cBc0vVUJStRuz6mV1bl02j2,_hErzSKXdV0MIoqbCne8DsJXqkGL2'
    UIDList = UIDList.split(',')
    for i in UIDList:
        lineID = firebaseGET('ManageUser/' + i + '/line')
        if (lineID.isascii()) & (lineID != ""):
            lineNoticeArray.append(lineID)
    print(lineNoticeArray)


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


def line_notify_img(token, path):
    try:
        headers = {'Authorization': f'Bearer {token}'}
        files = {'imageFile': open(path, 'rb')}
        msg_data = {'message': 'Image notification'}
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=msg_data, files=files)
        # r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload, timeout = 2)

        if debug:
            print('line Img status code: ' + str(r.status_code))
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
        ref = db.reference(dic)
        ref.set(dataS)
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


def ip2Location(ip):
    try:
        global iptable_i

        for i in range(len(iptable[0])):
            if iptable[0][i] == ip:
                return iptable[1][i]

        url = "http://api.apilayer.com/ip_to_location/"
        key = "?apikey=GzgE08ujaBF9bAm2oWgdEcAny4lpjcG6"
        loc_data = httpGET(url + ip + key)
        if (loc_data is None) | ("ERROR" in loc_data):
            log.addlog("ERROR with receiving data, HTTP code :" + loc_data[5:-1])
            return ""

        loc_data = str2json(loc_data)
        country = str(loc_data['country_name'])
        if '(' in country:
            country = country[0:country.index('(')]

        region = loc_data['region_name']
        if '(' in region:
            region = region[0:region.index('(')]

        city = loc_data['city']
        if '(' in city:
            city = city[0:city.index('(')]

        send = country + "," + region + "," + city

        iptable[0].append(ip)
        iptable[1].append(send)
        print(iptable)

        return send
    except Exception as e:
        log.addError(e)
        return ""


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
            'databaseURL': 'https://cgu-project-autobrake-default-rtdb.firebaseio.com',
            'httpTimeout': 3
        })
        loadLineUser()
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

        if data.outer().getWarning() != "":
            for i in lineNoticeArray:
                line_notify(i, data.outer().getWarning())
            data.outer().setWarning('')
        website_Host()

        # 1 sec repeat
        if ((timeStamp - millis_1sec) > 1) | (millis_1sec == 0):
            if httpCheck():
                data.timeModule().setOuterTime()
                data.outer().setInternetCheck(True)
            else:
                data.outer().setInternetCheck(False)

            # Data in Car info
            firebasePUT('CarInfo/Data/battery', data.temperature().getBatteryPercent())
            firebasePUT("CarInfo/Data/speed", data.speed().getSpeed())
            firebasePUT("CarInfo/Data/temperature", data.temperature().getAirTemperature())
            firebasePUT("CarInfo/Data/time", str(intTime()))

            # # Data in location
            firebasePUT("Map/CarLocation/Latitude", data.key().getGPS_Latitude())
            firebasePUT("Map/CarLocation/Longitude", data.key().getGPS_Longitude())

            # get user note [ONLY for exibition]
            # data.outer().setNote(firebaseGET("message/note"))

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


def firebase_listener__message_note(msgA):
    try:
        msg = msgA.data
        data.outer().setNote(msg)
        log.addlog("[Internet] message got, message is " + msg)
    except Exception as e:
        log.addError(e)


def firebase_listener__requestOFF(msgA):
    try:
        msg = msgA.data
        # Receive ON/OFF Requests
        if data.key().get_ON_OFF_Status():
            if debug:
                print('requestOFF: ' + msg)
            if 'POSITIVE' in msg:
                firebasePUT('on_off/requestOFF', 'ING')
                firebasePUT('on_off/time', nowTime())
                data.outer.requestOFF().setString(msg + '^' + ip2Location(msg[msg.index('^') + 1:]))
                log.addlog("[Internet] Response system turned OFF request")
    except Exception as e:
        log.addError(e)


def firebase_listener__requestON(msgA):
    try:
        msg = msgA.data
        # Receive ON/OFF Requests
        if not data.key().get_ON_OFF_Status():
            if debug:
                print('requestON: ' + msg)
            if 'POSITIVE' in msg:
                firebasePUT('on_off/requestON', 'ING')
                # firebasePUT('on_off/requestOFF', '')
                firebasePUT('on_off/time', nowTime())
                data.key().set_ON_OFF_Status(True)
                data.outer.requestON().setString(msg + '^' + ip2Location(msg[msg.index('^') + 1:]))
                log.addlog("[Internet] Response system turned ON request")
    except Exception as e:
        log.addError(e)


def firebase_listener__LINE(msgA):
    try:
        msg = msgA.data
        if msg != '':
            if debug:
                print('LINE msg: ' + msg)
            user = msg[:msg.index(',')]
            id = msg[msg.rindex(',') + 1:]
            token = line_id2token(id)
            if token is not None:
                firebasePUT('ManageUser/_' + user + '/line/', token)
                firebasePUT('ManageUser/LineNotify_code', '')
                lineNoticeArray.append(token)
    except Exception as e:
        log.addError(e)


def firebase_listener__displayMode(msgA):
    try:
        msg = str(msgA.data)
        if msg != '':
            if debug:
                print('stop : ' + msg)
            data.motor().setBrakeValue(int(msg))
    except Exception as e:
        log.addError(e)


init_status = True
carlo = ""
carla = ""
carloc = ""

rad = []
FLo = []
FLa = []
fencelist = []
seqnum = ""
MainFence = ""
lastMainFence = "！首次開機！"

current = ""
on_off = ""

import math


def on_off_callback(event):
    try:
        # print('on_off()', event.data)
        on_off_get()
    except Exception as e:
        log.addError(e)


def fence_callback(event):
    try:
        global MainFence
        # print('fence()', event.data)
        MainFence = db.reference('CarInfo/Fence').get()['MainFence']
        print('MainFence:', MainFence)
        fenceget()
    except Exception as e:
        log.addError(e)


def CarLocation_callback(event):
    try:
        # print('CarLocation()', event.data)
        CarLocationget()
    except Exception as e:
        log.addError(e)


def on_off_get():
    global current, on_off
    try:
        ref = db.reference('on_off')
        data = ref.get()
        current = data['current']
        if "," in data[current]:
            on_off = False  # 關機
        else:
            on_off = True  # 開機
    except Exception as e:
        log.addError(e)

    # print('current:', current)
    # print('on_off:', on_off)


def fenceget():
    global rad, FLo, FLa, fencelist, seqnum
    rad = []
    FLo = []
    FLa = []
    fencelist = []
    seqnum = ""
    try:
        data = db.reference('Map/Fence').get()
        seqnum = data['seqnum'].split(',')
        for key in seqnum:
            rad.append(data[key]['Radius'])
            FLo.append(data[key]['Longitude'])
            FLa.append(data[key]['Latitude'])
            fencelist.append(data[key]['Name'])

        # call calculate out or in
        calc()
    except Exception as e:
        log.addError(e)

    # print('rad:', rad)
    # print('FLo:', FLo)
    # print('FLa:', FLa)
    # print('fencelist:', fencelist)


def CarLocationget():
    global carla, carlo, carloc, init_status
    try:
        data = db.reference('Map/CarLocation').get()
        carla = data['Latitude']
        carlo = data['Longitude']
        carloc = {'lat': carla, 'lng': carlo}

        if init_status == True:
            init_status = False
        else:
            # call calculate out or in
            calc()

    except Exception as e:
        log.addError(e)

    # print('carla:', carla)
    # print('carlo:', carlo)
    # print('carloc:', carloc)


def calculate_distance(lat1, lon1, lat2, lon2):
    try:
        # 將經緯度轉換為弧度
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        # 計算差值
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        # 使用 Haversine 公式計算距離
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        # 設定地球半徑
        r = 6371
        # 計算距離（單位為公里）
        distance = c * r
        return distance
    except Exception as e:
        log.addError(e)
        return -1


def calc():
    try:
        print('calc')
        global carla, carlo, carloc, rad, FLo, FLa, fencelist, seqnum, MainFence, lastMainFence
        compute = []

        for i in range(len(seqnum)):
            if calculate_distance(float(carla), float(carlo), float(FLa[i]), float(FLo[i])) <= float(rad[i]) / 1000.0:
                compute.append(True)
            else:
                compute.append(False)

        # print('compute:', compute)
        index = compute.index(True) if True in compute else -1

        lastMainFence = MainFence

        if index != -1:
            # print(fencelist[index])
            uploadFence(index)
        else:
            # if MainFence == 'undefined' or lastMainFence != 'undefined':
            #     # print('out fence,lastfence:', lastMainFence)
            #     uploadFence(-1)
            # else:
            #     print("else")
            uploadFence(-1)


        print("lastMainFence",lastMainFence)
    except Exception as e:
        log.addError(e)


notifiedTime = 0


def uploadFence(resultIndex):
    global MainFence, fencelist, notifiedTime, lastMainFence
    current_time = str(datetime.datetime.now())  # the current time in HH:MM:SS.mmmmmm f
    current_time = current_time[:current_time.find('.')]
    try:
        if resultIndex != -1:
            print('uploadFence:', fencelist[resultIndex])
            db.reference('CarInfo/Fence').update({
                'MainFence': fencelist[resultIndex],
                'FenceCalcTime': current_time
            })
        else:
            print('uploadFence:', 'no fence')
            db.reference('CarInfo/Fence').update({
                'MainFence': 'undefined',
                'FenceCalcTime': current_time
            })
            if (time.time() - notifiedTime) > 1:
                notifiedTime = time.time()
                log.addlog("[Internet] Not in Fence msg send to all user :\n" + str(lineNoticeArray))
                for i in lineNoticeArray:
                    line_notify(i, "代步車已超過圍籬範圍 \n離開之圍籬為：" + lastMainFence +
                                # "\nGPS: " + data.key().getGPS_plainText() +
                                "\n查看詳細資訊：https://willy01010.github.io/newwebsite/root/maps.html")
    except Exception as e:
        log.addError(e)


def firebase_listener():
    db.reference('message/note').listen(firebase_listener__message_note)
    db.reference('on_off/requestOFF').listen(firebase_listener__requestOFF)
    db.reference('on_off/requestON').listen(firebase_listener__requestON)
    db.reference('ManageUser/LineNotify_code').listen(firebase_listener__LINE)
    db.reference('mode/display_mode/stop').listen(firebase_listener__displayMode)

    db.reference('on_off').listen(on_off_callback)
    db.reference('Map/CarLocation').listen(CarLocation_callback)
    db.reference('Map/Fence').listen(fence_callback)


previous_send_ON_OFF = False  # ON -> True, OFF -> False
previous_send_LOCK = False  # LOCK -> True, UNLOCK -> False
previous_OFF_response = ''


def website_Host():
    try:
        global previous_send_ON_OFF
        global previous_send_LOCK
        global previous_OFF_response
        if debug:
            print('Internet Hosting')

        # Send ON OFF Status
        # ON -> True, OFF -> False
        if previous_send_ON_OFF ^ data.key().get_ON_OFF_Status():
            if data.key().get_ON_OFF_Status():  # Turn ON
                current_num = str(firebaseGET('on_off/current'))
                current_num = str(int(current_num) + 1)
                firebasePUT('on_off/current', current_num)
                firebasePUT('on_off/' + current_num, nowTime())
                firebasePUT('on_off/requestON', '')
                firebasePUT('on_off/time', nowTime())
                log.addlog("[Internet] Announce system turned ON")
            else:  # Turn OFF
                current_num = str(firebaseGET('on_off/current'))
                firebasePUT('on_off/' + current_num, str(firebaseGET('on_off/' + current_num)) + "," + nowTime())
                log.addlog("[Internet] Announce system turned OFF")
                firebasePUT('on_off/status', "LOCK")
                firebasePUT('on_off/time', nowTime())
            previous_send_ON_OFF = data.key().get_ON_OFF_Status()

        # Send LOCK Status
        current_send_LOCK = bool(data.motor().getBrakeValue() == 0)  # LOCK -> True, UNLOCK -> False
        if previous_send_LOCK ^ current_send_LOCK:
            if current_send_LOCK:  # LOCK
                firebasePUT('on_off/status', "LOCK")
                log.addlog("[Internet] Announce system LOCK")
            else:  # UNLOCK
                firebasePUT('on_off/status', "UNLOCK")
                log.addlog("[Internet] Announce system UNLOCK")
        previous_send_LOCK = current_send_LOCK

        # Transmit OFF Response
        current_OFF_response = data.outer.requestOFF().getResponse()
        if current_OFF_response != previous_OFF_response:
            firebasePUT('on_off/requestOFF', '')
            firebasePUT('on_off/responseOFF', current_OFF_response)
            firebasePUT('on_off/time', nowTime())
            previous_OFF_response = ''
            data.outer.requestOFF().setResponse('')
            log.addlog("[Internet] Post system turned OFF response")
    except Exception as e:
        log.addError(e)


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
