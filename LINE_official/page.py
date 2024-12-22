import sys
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import official_LINE_lib, error_Handling

version = "2025.1.1.1234567"
folder = "img/"

isRenewing = False
isShuttingDown = False
I_renew = None

# Sample data array
F_userList, L_lineAccountInfo, lineAccount = None, None, None

def updateInfo():
    global isRenewing, F_userList, L_lineAccountInfo, lineAccount

    L_lineAccountInfo.config(
        text="\n" + "名稱: " + lineAccount.accountName + "\nID: " + lineAccount.accountLINEID + "\n訊息剩餘次數: " + lineAccount.accountQuota)
    lineAccount.loadJoinedUser_interval = 90000
    usrInfo = lineAccount.getResponse()

    for idx, user in enumerate(usrInfo):
        # photo = display_image_from_web(user[3])
        image_label = tk.Label(F_userList, image=user[3])  # Replace with Image when integrated
        image_label.image = user[3]  # Keep a reference to avoid garbage collection
        image_label.grid(row=idx, column=0, padx=0, pady=0)

        # Right column: Name
        name_label = tk.Label(F_userList, text=user[2], font=("Arial", 14))
        name_label.grid(row=idx, column=1, padx=20, pady=50)
    isRenewing = False

def updateLineAccount():  # Tokens and Urls
    global lineAccount
    try:
        error_Handling.error_info_Handling(100, "[INFO] Verifying LINE account")
        channel_access_token_public = 'ufRWLckiARfsXwB0JN2DjEcFVUtFzPpphhR6YhCAIYou9T8Y3mZ0qTOEQVCB/QPuLiS08ybRL2XEj20AW4dX2loBM3jZkNE4nWom+KyhDlSn3tQZD4afDPns0OmYHME3tNrWf9Gk48aNaWQYnYuDMwdB04t89/1O/w1cDnyilFU='
        webhook_id_ = "ee481c17c8ae36266612fe4d74bbd685"
        webhook_bearer_ = "22381d5762fbc834e57504cd2e541f821bd7a46ebd432d2d"

        lineAccount = official_LINE_lib.LineOfficialAccount(LINE_channel_access_token=channel_access_token_public,
                                                            webhook_id=webhook_id_,
                                                            webhook_bearer=webhook_bearer_, key="Luósī³")
        error_Handling.error_info_Handling(200, "[INFO] Verify LINE account succeed")
    except Exception as e:
        error_Handling.error_info_Handling(-1, "[ERROR] Failed to verify LINE account with error", e)

Root_mainPage = tk.Tk()
def init_main_page():
    global F_userList, L_lineAccountInfo, B_renew, isRenewing, I_renew, Root_mainPage
    # Initialize main application window
    Root_mainPage.title("LINE 官方帳號使用者讀取")
    Root_mainPage.geometry("600x400")

    # ------ bottom frame ------
    bottom_frame = tk.Frame(Root_mainPage)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

    L_copyRight = tk.Label(bottom_frame, text="© 2025.1.1.1234567", font=("Arial", 10))
    L_copyRight.pack(side=tk.LEFT, padx=5, pady=0)

    L_version = tk.Label(bottom_frame, text="v" + version, font=("Arial", 10))
    L_version.pack(side=tk.RIGHT, padx=5, pady=0)
    # ======= bottom frame =======

    # ------- top Frame -------
    # Top Frame for Label and Buttons
    top_frame = tk.Frame(Root_mainPage)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    # Left Label
    L_lineAccountInfo = tk.Label(top_frame, text="\n" + "名稱:" + "\nID:" + "\n訊息剩餘次數", font=("Arial", 14),
                                 justify="left")
    L_lineAccountInfo.pack(side=tk.LEFT, padx=10)

    # Buttons Frame
    F_top = tk.Frame(top_frame)
    F_top.pack(side=tk.RIGHT)

    # Renew Button
    def btnCmd_refresh():
        global isRenewing
        isRenewing = True
        
    I_renew = Image.open(folder + "renew.png").resize((50, 50))
    P_renew = ImageTk.PhotoImage(I_renew)
    B_renew = tk.Button(F_top, text="renew", command=btnCmd_refresh, image=P_renew)
    B_renew.image = P_renew  # Keep a reference to avoid garbage collection
    B_renew.pack(side=tk.LEFT, padx=5)

    # Settings Button
    def btnCmd_open_settings():
        global isRenewing, Root_settingsPage
        error_Handling.error_info_Handling(200, "[INFO] Settings button clicked")
        # updateLineAccount()
        Root_settingsPage.deiconify()
        
    P_setting = ImageTk.PhotoImage(Image.open(folder + "setting.png").resize((50, 50)))
    B_setting = tk.Button(F_top, text="setting", command=btnCmd_open_settings, image=P_setting)
    B_setting.image = P_setting  # Keep a reference to avoid garbage collection
    B_setting.pack(side=tk.LEFT, padx=5)
    # ======= top Frame =======

    # ------- middle Frame -------
    # Middle Frame for Scrollable Panel
    middle_frame = tk.Frame(Root_mainPage)
    middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=2)

    # Canvas and Scrollbar for scrolling
    C_forScrollBar = tk.Canvas(middle_frame)
    scrollbar = ttk.Scrollbar(middle_frame, orient=tk.VERTICAL, command=C_forScrollBar.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    C_forScrollBar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollable Frame
    F_userList = ttk.Frame(C_forScrollBar)
    F_userList.bind(
        "<Configure>", lambda e: C_forScrollBar.configure(scrollregion=C_forScrollBar.bbox("all"))
    )
    C_forScrollBar.create_window((0, 0), window=F_userList, anchor="nw")
    C_forScrollBar.configure(yscrollcommand=scrollbar.set)
    # ======= middle Frame =======

    def funcShutDown():
        global isShuttingDown
        isShuttingDown = True
        error_Handling.error_info_Handling(0, "[INFO] Shutting down")
        Root_mainPage.destroy()
        sys.exit(0)

    Root_mainPage.protocol("WM_DELETE_WINDOW", funcShutDown)

    error_Handling.error_info_Handling(200, "[INFO] page init DONE")

Root_settingsPage = tk.Toplevel(Root_mainPage)
def init_settings_page():
    global Root_settingsPage, Root_mainPage
    error_Handling.error_info_Handling(200, "[INFO] hosting settings page")
    Root_settingsPage = tk.Toplevel(Root_mainPage)
    Root_settingsPage.title("LINE 官方帳號使用者讀取 - 設定")
    Root_settingsPage.geometry("600x400")

    # ------ top frame ------
    top_frame = tk.Frame(Root_settingsPage)
    top_frame.pack(side=tk.TOP, fill=tk.Y, expand=True, padx=10, pady=2)

    image_label = tk.Label(top_frame, text="設定", font=("Arial", 20))
    image_label.grid(row=0, column=0, padx=0, pady=0)
    # ======= top frame =======


    # ------ middle frame ------
    middle_frame = tk.Frame(Root_settingsPage)
    middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=2)


    L_channel_access = tk.Label(middle_frame, text="Channel access token", font=("Arial", 14))
    L_channel_access.grid(row=0, column=0, padx=0, pady=0)
    T_channel_access = tk.Entry(middle_frame, font=("Arial", 14))
    T_channel_access.grid(row=0, column=1, padx=0, pady=10)

    L_webhook_id = tk.Label(middle_frame, text="webhook ID", font=("Arial", 14))
    L_webhook_id.grid(row=1, column=0, padx=0, pady=0)
    T_webhook_id = tk.Entry(middle_frame, font=("Arial", 14))
    T_webhook_id.grid(row=1, column=1, padx=0, pady=10)

    L_webhook_bearer = tk.Label(middle_frame, text="webhook bearer", font=("Arial", 14))
    L_webhook_bearer.grid(row=2, column=0, padx=0, pady=0)
    T_webhook_bearer = tk.Entry(middle_frame, font=("Arial", 14))
    T_webhook_bearer.grid(row=2, column=1, padx=0, pady=10)
    # ======= middle frame =======



    # ------ bottom frame ------
    bottom_frame = tk.Frame(Root_settingsPage)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.Y, expand=True, padx=10, pady=2)

    def btnCmd_save_settings():
        error_Handling.error_info_Handling(200, "[INFO] settings saved")
        Root_settingsPage.withdraw()
        updateLineAccount()

    B_confirm = tk.Button(bottom_frame, text="確認", command=btnCmd_save_settings)
    B_confirm.pack(side=tk.RIGHT, padx=5)

    # ======= bottom frame =======

    Root_settingsPage.withdraw()

    Root_settingsPage.protocol("WM_DELETE_WINDOW", Root_settingsPage.withdraw)


    # Root_settingsPage. TODO make page uneditable
    error_Handling.error_info_Handling(200, "[INFO] settings page init DONE")

def process_loading_animation():
    global isRenewing, B_renew, I_renew, isShuttingDown
    rotateAngle = 0

    while I_renew is None:
        error_Handling.error_info_Handling(404, "[ERROR] Failed loading animation: Image not found")
        time.sleep(1)

    error_Handling.error_info_Handling(200, "[INFO] hosting loading animation")

    while 1:
        if isShuttingDown:
            error_Handling.error_info_Handling(0, "[INFO] Shutting down loading animation")
            break
        try:
            if isRenewing:
                rotateAngle -= 10
                photo = ImageTk.PhotoImage(I_renew.rotate(rotateAngle))
                B_renew.config(image=photo)  # Keep a reference to avoid garbage collection
            else:
                if rotateAngle != 0:
                    rotateAngle = 0
                    photo = ImageTk.PhotoImage(I_renew)
                    B_renew.config(image=photo)
            time.sleep(0.15)
        except Exception as e:
            if isShuttingDown:
                error_Handling.error_info_Handling(0, "[INFO] Shutting down loading animation")
                break
            error_Handling.error_info_Handling(-1, "[ERROR] loading animation failed with error", e)
            time.sleep(.5)
            pass

def process_updateInfo():
    global isRenewing, isShuttingDown
    error_Handling.error_info_Handling(200, "[INFO] hosting updateInfo")
    while 1:
        try:
            if isShuttingDown:
                error_Handling.error_info_Handling(0, "[INFO] Shutting down process updater")
                break
            if isRenewing:
                updateInfo()
            time.sleep(.2)
        except Exception as e:
            error_Handling.error_info_Handling(-1, "[ERROR] updateInfo failed with error", e)
            time.sleep(1)


init_main_page()
init_settings_page()
if __name__ == '__main__':
    start_process_reloading = threading.Thread(target=process_loading_animation)
    start_process_updateInfo = threading.Thread(target=process_updateInfo)
    a = threading.Thread(target=Root_mainPage.mainloop)

    # start_process_root = threading.Thread(target=Root_mainPage.mainloop)

    start_process_reloading.start()
    start_process_updateInfo.start()
    # a.start()
    Root_mainPage.mainloop()