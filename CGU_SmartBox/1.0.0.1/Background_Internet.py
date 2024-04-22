import math
import time
from datetime import datetime
from firebase_admin import db

import Internet
import log

init = True


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
    global carla, carlo, carloc, init
    try:
        data = db.reference('Map/CarLocation').get()
        carla = data['Latitude']
        carlo = data['Longitude']
        carloc = {'lat': carla, 'lng': carlo}

        if init == True:
            init = False
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

        if index != -1:
            # print(fencelist[index])
            uploadFence(index)
        else:
            if MainFence == 'undefined' or lastMainFence != 'undefined':
                # print('out fence,lastfence:', lastMainFence)
                uploadFence(-1)

        lastMainFence = MainFence
    except Exception as e:
        log.addError(e)


# notifiedTime = 0

last_notify = 0
print("last notify:", last_notify)
def uploadFence(resultIndex):
    global MainFence, fencelist, notifiedTime, last_notify
    current_time = str(datetime.now())  # the current time in HH:MM:SS.mmmmmm f
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
            if (time.time() - last_notify) > 100:
                last_notify = time.time()

                log.addlog("[Internet] Not in Fence msg send to all user :\n" + str(Internet.lineNoticeArray))
                for i in Internet.lineNoticeArray:
                    print("last notify:", last_notify)
                    Internet.line_notify(i, "代步車已超過圍籬範圍  離開之圍籬為：" + lastMainFence)

    except Exception as e:
        log.addError(e)
