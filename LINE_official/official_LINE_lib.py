import requests
import json
import time
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
import error_Handling


class LineOfficialAccount:
    def __init__(self, LINE_channel_access_token, webhook_id, webhook_bearer, key=None):
        self.accountQuota = "N/A"
        self.__accountUID, self.accountLINEID, self.accountName = "N/A", "N/A", "N/A"
        self.loadJoinedUser_interval = 600

        self.webhook_id = webhook_id
        self.webhook_bearer = webhook_bearer
        self.channel_access_token = LINE_channel_access_token

        self.__getAccountInfo()
        self.__getAccountQuota()

        self.accountUID = self.__accountUID if key == "Luósī³" else "N/A"
        a = tk.Tk()
        a.withdraw()

    def __load_img_from_web(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)  # Convert bytes to a file-like object
                image = Image.open(image_data).resize((50, 50))  # Resize the image
                error_Handling.error_info_Handling(response.status_code, "[Info] user image fetch successfully!")
                return ImageTk.PhotoImage(image)
            else:
                return error_Handling.error_info_Handling(response.status_code,
                                                          f"[ERROR] Failed to fetch user image from {url}")
        except Exception as e:
            return error_Handling.error_info_Handling(-1, f"[ERROR] Failed to fetch user image with error from {url}",
                                                      e)

    def send_line_message(self, user_id, msg):
        try:
            # Message payload
            message_data = {
                "to": user_id,
                "messages": [
                    {
                        "type": "text",
                        "text": msg
                    }
                ]
            }
            # Request headers
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.channel_access_token}'
            }

            # Send POST request to LINE API
            response = requests.post(
                'https://api.line.me/v2/bot/message/push',
                headers=headers,
                json=message_data
            )

            # Check the response status
            if response.status_code == 200:
                return error_Handling.error_info_Handling(response.status_code, "[Info] Message sent successfully!")
            else:
                return error_Handling.error_info_Handling(response.status_code,
                                                          "[ERROR] Failed to send message" + response.text)
        except Exception as e:
            return error_Handling.error_info_Handling(-1, "[ERROR] Failed to send message with error", e)

    def __getUserInfo(self, user_id):
        try:
            headers = {
                'Authorization': f'Bearer {self.channel_access_token}'
            }
            res = requests.get("https://api.line.me/v2/bot/profile/" + user_id, headers=headers)

            if res.status_code == 200:
                user_name = res.json()["displayName"]
                user_img_url = res.json()["pictureUrl"]
                error_Handling.error_info_Handling(res.status_code,
                                                   "[Info] Received User: " + user_name + ", img_url:" + user_img_url[:20])
                return user_name, user_img_url
            else:
                error_Handling.error_info_Handling(res.status_code, "[ERROR] Failed to get user info: " + res.text)
                return None, None
        except Exception as e:
            error_Handling.error_info_Handling(-1, "[ERROR] Failed to get user name with error", e)
            return None, None

    def __getAccountQuota(self):
        try:
            headers = {
                'Authorization': f'Bearer {self.channel_access_token}'
            }
            totalQuota_res = requests.get("https://api.line.me/v2/bot/message/quota", headers=headers)
            usedQuota_res = requests.get("https://api.line.me/v2/bot/message/quota/consumption", headers=headers)

            if totalQuota_res.status_code != 200:
                error_Handling.error_info_Handling(totalQuota_res.status_code,
                                                   "[ERROR] Failed to get totalQuota: " + totalQuota_res.text)
            elif usedQuota_res.status_code != 200:
                error_Handling.error_info_Handling(usedQuota_res.status_code,
                                                   "[ERROR] Failed to get usedQuota: " + usedQuota_res.text)
            else:
                self.accountQuota = str(totalQuota_res.json()['value'] - usedQuota_res.json()['totalUsage']) + \
                                    "/" + str(totalQuota_res.json()['value'])
                error_Handling.error_info_Handling(200, "[Info] Received accountQuota: " + self.accountQuota)
        except Exception as e:
            error_Handling.error_info_Handling(-1, "[ERROR] Failed to get accountQuota with error", e)

    def __getAccountInfo(self):
        try:
            headers = {
                'Authorization': f'Bearer {self.channel_access_token}'
            }
            res = requests.get("https://api.line.me/v2/bot/info", headers=headers)
            accountUID = res.json()['userId']
            accountLINEID = res.json()['basicId']
            accountName = res.json()['displayName']

            if res.status_code != 200:
                error_Handling.error_info_Handling(res.status_code, "[ERROR] Failed to get account info: " + res.text)
            else:
                self.__accountUID, self.accountLINEID, self.accountName = accountUID, accountLINEID, accountName
                error_Handling.error_info_Handling(200, f"[Info] Received account info: LINE_ID: {self.accountLINEID}, Name: {self.accountName}")
        except Exception as e:
            error_Handling.error_info_Handling(-1, "[ERROR] Failed to get account info with error", e)

    def getResponse(self):
        try:
            url = "https://webhook-test.com/api/webhooks/" + self.webhook_id
            headers = {
                'Authorization': 'Bearer ' + self.webhook_bearer
            }
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                return error_Handling.error_info_Handling(response.status_code,
                                                          "[ERROR] Failed to get webhook response: " + response.text)

            nowTimeStamp = time.time()
            output = []
            for info in response.json()['payloads']:
                payload = info['payload']
                events = json.loads(payload)['events'][0]
                # payload = info['payload'].json()
                destination = json.loads(payload)['destination']

                # events = payload['events'][0]
                timeStamp, event_type = events["timestamp"], events["type"]
                timeStamp /= 1000

                if event_type != "follow":
                    continue
                elif destination != self.__accountUID:
                    continue
                elif (nowTimeStamp - timeStamp) > self.loadJoinedUser_interval:
                    continue

                userID = events["source"]["userId"]
                name, img_url = self.__getUserInfo(userID)
                output.append([timeStamp, userID, name, self.__load_img_from_web(img_url)])

            error_Handling.error_info_Handling(response.status_code, "[Info] Webhook response received successfully!")
            return output
        except Exception as e:
            error_Handling.error_info_Handling(-1, "[ERROR] Failed to get webhook response with error", e)


if __name__ == "__main__":
    # find it in the LINE Developers Console/messaging API/bottom of the page
    channel_access_token_public = 'ufRWLckiARfsXwB0JN2DjEcFVUtFzPpphhR6YhCAIYou9T8Y3mZ0qTOEQVCB/QPuLiS08ybRL2XEj20AW4dX2loBM3jZkNE4nWom+KyhDlSn3tQZD4afDPns0OmYHME3tNrWf9Gk48aNaWQYnYuDMwdB04t89/1O/w1cDnyilFU='
    user_id_public = 'Uce9447965d010544ea7_f4e30d83e00d8'  # from webhook
    groupID = "C50cb787a3f61b19567b12659b459f4b3"  # from webhook

    webhook_id_ = "ee481c17c8ae36266612fe4d74bbd685"
    webhook_bearer_ = "22381d5762fbc834e57504cd2e541f821bd7a46ebd432d2d"

    account = LineOfficialAccount(LINE_channel_access_token=channel_access_token_public, webhook_id=webhook_id_,
                                  webhook_bearer=webhook_bearer_, key="Luósī³")

    # print(account.accountName)
    # print(account.accountLINEID)
    # print(account.accountUID)
    # print(account.accountQuota)
    # print(account.loadJoinedUser_interval)
    account.loadJoinedUser_interval = 9000
    # print(account.loadJoinedUser_interval)

    # account.send_line_message(user_id=user_id_public, msg="Hello, this is a test message.")
    # print(account.getUserInfo(user_id=user_id_public))

    print(account.getResponse())
