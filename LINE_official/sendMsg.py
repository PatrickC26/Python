import time
print(time.time(), "event start")
import requests

def send_line_message(channel_access_token, user_id):
    # Message payload
    message_data = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": "Hello, this is a message from your LINE bot!"
            }
        ]
    }

    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}'
    }

    # Send POST request to LINE API
    response = requests.post(
        'https://api.line.me/v2/bot/message/push',
        headers=headers,
        json=message_data
    )

    # Check the response status
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")
# find it in the LINE Developers Console/messaging API/bottom of the page
channel_access_token_public = 'ufRWLckiARfsXwB0JN2DjEcFVUtFzPpphhR6YhCAIYou9T8Y3mZ0qTOEQVCB/QPuLiS08ybRL2XEj20AW4dX2loBM3jZkNE4nWom+KyhDlSn3tQZD4afDPns0OmYHME3tNrWf9Gk48aNaWQYnYuDMwdB04t89/1O/w1cDnyilFU='
user_id_public = 'Uce9447965d010544ea7f4e30d83e00d8' # from webhook
# send_line_message(channel_access_token_public, user_id_public)


def getUserInfo(channel_access_token, user_id):
    headers = {
        'Authorization': f'Bearer {channel_access_token}'
    }
    res = requests.get("https://api.line.me/v2/bot/profile/" + user_id, headers=headers)
    # print(res.json())
    print(res.json()["displayName"])
    print(res.json()["pictureUrl"])
    # download the image and print on a UI
    img = requests.get(res.json()["pictureUrl"])



def getQuota(channel_access_token):
    headers = {
        'Authorization': f'Bearer {channel_access_token}'
    }
    res = requests.get("https://api.line.me/v2/bot/message/quota", headers=headers)
    res1 = requests.get("https://api.line.me/v2/bot/message/quota/consumption", headers=headers)
    print(res.json()['value'], res1.json()['totalUsage'])


def getAccountName(channel_access_token):
    headers = {
        'Authorization': f'Bearer {channel_access_token}'
    }
    res = requests.get("https://api.line.me/v2/bot/info", headers=headers)
    # print(res.json())
    accountID = res.json()['userId']
    accountLINEID = res.json()['basicId']
    name = res.json()['displayName']
    print(accountID, accountLINEID, name)
    return accountID, accountLINEID, name


getAccountName(channel_access_token_public)
getQuota(channel_access_token_public)
getUserInfo(channel_access_token_public, user_id_public)
exit(0)
groupID = "C50cb787a3f61b19567b12659b459f4b3"
# def getGroupInfo(channel_access_token, group_id):
#     headers = {
#         'Authorization' : f'Bearer {channel_access_token}'
#     }
#     res = requests.get("https://api.line.me/v2/bot/group/" + group_id, headers=headers)
#
#     print(res.json())
# getGroupInfo(channel_access_token_public, groupID)
# exit(0)
# send_line_message(channel_access_token_public, groupID)



# id = "ee481c17c8ae36266612fe4d74bbd685"
# webhook_bearer = "22381d5762fbc834e57504cd2e541f821bd7a46ebd432d2d"
def webhook_access(debug=False):
    try:

        url = "https://webhook-test.com/api/webhooks/" + id
        headers = {
            'Authorization': 'Bearer 22381d5762fbc834e57504cd2e541f821bd7a46ebd432d2d'
        }

        response = requests.get(url, headers=headers)

        # Optionally, print the response content
        print(response.status_code)
        # print(response.text)

        if debug:
            print('line status code: ' + str(response.status_code))
        return response.json()
    except Exception as e:
        print(e)


import json


print(time.time(), "start fetching msg")
res = webhook_access()
print(time.time(), "msg received")
print("\n\n")
# print(res['payloads'])
for i in res['payloads']:
    payload = i['payload']
    events = json.loads(payload)['events'][0]

    print(events["timestamp"], events["type"], events["source"]["userId"])
    print()
