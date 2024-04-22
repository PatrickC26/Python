import socket

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests


def httpGET(url):
    try:
        response = requests.get(url, timeout=2)
        # Check if the request was successful
        print('httpGET with response code: ' + str(response.status_code))
        if response.status_code == 200:
            return str(response.json())
        else:
            return 'ERROR' + str(response.status_code)
    except requests.exceptions.ReadTimeout as e:
        try:  # Second try
            response = requests.get(url, timeout=2)
            # Check if the request was successful
            print('httpGET second chance with response code: ' + str(response.status_code))
            if response.status_code == 200:
                return str(response.json())
        except requests.exceptions.ReadTimeout as e1:
            pass


def httpCheck(printing=False):
    try:
        conn = socket.create_connection((socket.gethostbyname("www.google.com"), 80), timeout=1)
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


def firebaseGET(dic: str):
    try:
        ref = db.reference(dic)
        returnS = str(ref.get(dic))
        returnS = returnS.replace('|NL|', "\n")
        returnS = returnS.replace('|TAB|', "\t")
        return returnS[returnS.index("'") + 1: returnS.rindex(",") - 1]
    except Exception as e:
        pass
        return ""


def firebasePUT(dic: str, dataS):
    try:
        dataS = dataS.replace("\n", '|NL|')
        dataS = dataS.replace("\t", '|TAB|')
        ref = db.reference(dic)
        ref.set(dataS)
    except Exception as e:
        pass


import datetime
def nowDate():
    now = datetime.datetime.now()
    time_string = now.strftime("%Y_%m_%d %H=%M=%S")
    return time_string


import json
def str2json(str_data: str):
    str_data = str_data.replace("'", '"')
    str_data = str_data.replace("[", '')
    str_data = str_data.replace("]", '')
    str_data = str_data.replace('False', "0")
    str_data = str_data.replace('Ture', "1")
    return json.loads(str_data)


def nameListener(msg):
    return firebaseGET('ManageUser/Name')


import time
def init(printing=False):
    retryRemain = 5

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
        print("Internet FAILED")
        return False

    print("Starting Internet Service")

    try:
        cred = credentials.Certificate(file_path + "key.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://mediapipe-cgu-default-rtdb.firebaseio.com/',
            'httpTimeout': 3
        })

        return True
    except Exception as e:
        return False

file_path = "/Users/slothsmba/Desktop/mediaPipe/"


while not init():
    pass
print("Internet Service Started")
