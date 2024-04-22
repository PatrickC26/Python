
import os
import cv2
import PySimpleGUI as sg
import time
import numpy as np
from datetime import datetime as dt
import random


def get_time():
    e = dt.now()
    return e


name = ['jklkds']



# def get_name(no,number):
#     return "name"


def valid(person):
    global name
    #TODO
    get_num = ['class01','class02','class03','class04']
    for m in range(len(get_num)):
        now_num = get_num[m]
        last_two_digits = now_num[-2:]

    recognizer = cv2.face.LBPHFaceRecognizer_create() # 啟用訓練人臉模型方法
    recognizer.read('/Users/slothsmba/Documents/Codes/Python/pythonProject/CGU project/0testing/face_try.yml') # 讀取人臉模型檔
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # 載入人臉追蹤模型
    filename = "/Users/slothsmba/Documents/Codes/Python/pythonProject/CGU project/0testing/photo.jpg"
    img = cv2.imread(filename)
    #img = cv2.resize(img,(200,200)) # 縮小尺寸，加快辨識效率
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 色彩轉換成黑白
    faces = face_cascade.detectMultiScale(gray) # 追蹤人臉 ( 目的在於標記出外框 )
    while True:
        print(name)
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2) # 標記人臉外框
            idnum,confidence = recognizer.predict(gray[y:y+h,x:x+w]) # 取出 id 號碼以及信心指數 confidence
            print(idnum)
            print(confidence)
            text = name[int(idnum)]
            print(text)
        if text == person:  #輸入學號跟判斷人物相同
            print('succeed')
            sg.popup_ok("點名成功")
            text_last_two = text[-2:]
        elif text != person:  #不相同
            print('人物不符')
            print('判斷為')
            print(text)
            sg.popup_auto_close("身分不符")
        else:
            print('無資料，請先確認是否已登錄過')
            sg.popup_auto_close("無資料 \n 請先確認是否已登錄過")
        return

def student_table(name,subject):
    #TODO
    student_member = ["ABC","CDE","EFG"]

    rows = [[] for _ in range(len(student_member))]
    rows_complete = [[] for i in range(0)]
    m = 0

    for i in range(len(student_member)):
        now_student = student_member[i]
        print(now_student)
        now_last_two = now_student[-2:]
        print(name)
        print(subject)
        get_attend = 'yes'
        get_attend_time = "32:324:234"
        get_sleep = 'no'
        get_duration = 0
        get_sleep_times = 0
        if get_attend == 'yes':
            get_attend = '到'
        else:
            get_attend = '未到'
        if get_sleep == 'yes':
            get_sleep = '睡著'
        else:
            get_sleep = '良好'
            get_duration = 0
            get_sleep_times = 0
        rows[i].append(str(now_student))
        rows[i].append(str(get_attend))
        rows[i].append(str(get_attend_time))
        rows[i].append(str(get_sleep))
        rows[i].append(str(get_duration))
        rows[i].append(str(get_sleep_times))
        if get_sleep == '睡著':
            rows_complete.append([])
            rows_complete[m].append(str(now_student))
            rows_complete[m].append(str(get_attend))
            rows_complete[m].append(str(get_attend_time))
            rows_complete[m].append(str(get_sleep))
            rows_complete[m].append(str(get_duration))
            rows_complete[m].append(str(get_sleep_times))
            m += 1

    return [rows, rows_complete]

def student_performance(name,subject):
    toprow = ['學號', '簽到', '簽到時間', '上課狀態', '睡覺時長', '睡著次數']
    tab = student_table(name, subject)
    all = tab[0]
    sleep = tab[1]
    table_1 = sg.Table(values=all, headings=toprow, size=(800, 500), auto_size_columns=True,
                       display_row_numbers=False,
                       justification='center', key='-TABLE_1-', enable_events=True, expand_x=True, expand_y=False,
                       enable_click_events=True, background_color='lightblue', alternating_row_color='lightyellow')
    layout_1 = [[table_1]]
    table_2 = sg.Table(values=sleep, headings=toprow, size=(800, 500), auto_size_columns=True,
                       display_row_numbers=False,
                       justification='center', key='-TABLE_1-', enable_events=True, expand_x=True, expand_y=False,
                       enable_click_events=True, background_color='lightblue', alternating_row_color='lightyellow')
    layout_2 = [[table_2]]
    layout = [[sg.TabGroup([[sg.Tab('總攬', layout_1), sg.Tab('睡著', layout_2)]],
                               expand_x=True, expand_y=False)]]
    window_for_student_performance = sg.Window('學生上課狀態', layout, size=(700,300))

    while True:
        event, values = window_for_student_performance.read()
        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break
    window_for_student_performance.close()

def teacher_window(name):
    teacher_subject = ['class01','class02','class03','class04']

    layout = [[sg.Text('選擇課程 : '), sg.Combo(teacher_subject, size=(15, 1), key='-TEACHER_COMBO-')],
              [sg.Button('查看上課資料', key='-TEACHER_COMBO_CONFIRM-')],
              [sg.Text('\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')],
              [sg.Button('產生登錄碼 : ', key='-RANDOM-', visible=False),sg.Text('',key='-RANDOM_TEXT-', visible=False)]]
    window_for_teacher = sg.Window('教職員介面', layout, size=(300,300))
    while True:
        event, values = window_for_teacher.read()
        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break
        elif event == '-TEACHER_COMBO_CONFIRM-':
            subject = window_for_teacher['-TEACHER_COMBO-'].get()
            window_for_teacher['-RANDOM-'].Update(visible=True)
            window_for_teacher['-RANDOM_TEXT-'].Update(visible=True)
            student_performance(name,subject)

        elif event == '-RANDOM-':
            random_number = random.randint(100, 999)


    window_for_teacher.close()


def combo_subject(userName):
    if len(userName)==0:
        return ''
    else:
        return ['class01','class02','class03','class04']


def initial():
    global number, current_subject
    sg.theme('LightGrey1')
    text = '(輸入格式 : BXXXXXXX)'

    layout = [[sg.Text('-------------------------------------------------------歡迎使用線上人臉辨識自動點名系統-----------------------------------------------------------')],
              [sg.Text('我是學生')],
              [sg.Text('請輸入學號'), sg.Input('', key='-INPUT-')],
              [sg.Text(text, key='-TEXT-')],
              [sg.Button('確認', key='-CONFIRM-')],
              [sg.Text('選擇課程 : ',key='-SUBJECT_TEXT-',visible=False),sg.Combo(combo_subject(''), size=(15, 1), key='-COMBO-',visible=False)],
              [sg.Button('進行點名', key='-START-',visible=False)],
              [sg.Button('離開系統', key='-EXIT-')],
              [sg.Text('\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')],
              [sg.Button('學生首次登錄', key='-NEW-')],
              [sg.Text('\n*******************************************************************************************************************************************\n')],
              [sg.Text('我是教職員 : ')],
              [sg.Text('名稱 : '), sg.Input('',key='-TEACHER_NAME-')],
              [sg.Text('密碼 : '), sg.Input('',key='-TEACHER_PASSWORD-')],
              [sg.Text('',key='-TEACHER_TEXT-')],
              [sg.Button('確認', key='-TEACHER_GO-')]
              ]
    window_for_initial = sg.Window('開始點名', layout, size=(700,700))

    while True:
        event, values = window_for_initial.read()
        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break

        elif event == '-CONFIRM-':
            number = window_for_initial['-INPUT-'].get()
            last_two = number[-2:]
            if len(number) ==0:
                window_for_initial['-TEXT-'].Update(text + '\n請先輸入學號')
            else:
                print(number)
                window_for_initial['-SUBJECT_TEXT-'].Update(visible=True)
                window_for_initial['-COMBO-'].Update(visible=True)
                window_for_initial['-START-'].Update(visible=True)
                window_for_initial['-COMBO-'].Update(values=combo_subject(str(last_two)))

        elif event == '-START-':
            current_subject = window_for_initial['-COMBO-'].get()
            work1(last_two, number)
        elif event == '-NEW-':
            new_window()
        elif event == '-TEACHER_GO-':
            teacher_name = window_for_initial['-TEACHER_NAME-'].get()
            teacher_password = window_for_initial['-TEACHER_PASSWORD-'].get()
            ref = 'deep/' + teacher_name + '/code'
            password = "1234"
            if len(teacher_name) == 0 or len(teacher_password) == 0:
                window_for_initial['-TEACHER_TEXT-'].Update('資料未填寫完畢，請重新檢查')
            else:
                if teacher_password == password:
                    print('teacher login ')
                    teacher_window(teacher_name)
                else:
                    window_for_initial['-TEACHER_TEXT-'].Update('密碼錯誤')

    window_for_initial.close()

def new_window():
    global current_teacher
    new_num =''
    login_ans = '123'
    layout = [[sg.Text('輸入學號  ex:BXXXXXXX'), sg.Input('',key='-NEW_NUM-')],
              [sg.Button('確認', key='-NEW_CONFIRM-')],
              [sg.Text('選擇課程 : ',visible=False,key='-SUBJECT_TEXT-'), sg.Combo('', size=(15, 1),visible=False, key='-COMBO_NEW-')],
              [sg.Text('輸入登錄碼',visible=False, key='-LOGIN_TEXT-'),sg.Input('',key='-LOGIN-', visible=False)],
              [sg.Text('',key='-NEW_TEXT-')],
              [sg.Button('開始拍攝',key='-NEW_SHOOT-',visible=True)]
               ]
    window_for_new = sg.Window('首次登錄', layout,size=(300,300))
    while True:
        event, values = window_for_new.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-NEW_CONFIRM-':
            new_num = window_for_new['-NEW_NUM-'].get()

            last_two = new_num[-2:]
            if len(new_num) == 0:
                window_for_new['-NEW_TEXT-'].Update('請輸入學號')
            else:
                window_for_new['-SUBJECT_TEXT-'].Update(visible=True)
                window_for_new['-COMBO_NEW-'].Update(visible=True)
                window_for_new['-LOGIN_TEXT-'].Update(visible=True)
                window_for_new['-LOGIN-'].Update(visible=True)
                window_for_new['-NEW_SHOOT-'].Update(visible=True)
                window_for_new['-COMBO_NEW-'].Update(values=combo_subject(str(last_two)))
        elif event == '-NEW_SHOOT-':
            subject = window_for_new['-COMBO_NEW-'].get()
            new_num = window_for_new['-NEW_NUM-'].get()
            last_two_digits = new_num[-2:]
            print(last_two_digits)

            current_teacher = "Teacher"
            login_ans = "1234"
            print(str(login_ans))

            window_for_new.close()
            shooting(new_num)


    window_for_new.close()

def shooting(num):
    # 创建保存照片的文件夹
    output_folder = "/Users/slothsmba/Documents/Codes/Python/pythonProject/CGU project/0testing/" + num
    os.makedirs(output_folder, exist_ok=True)

    # 打开相机
    cap = cv2.VideoCapture(0)

    # 检查相机是否成功打开
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # 定义计时器
    timer = None

    # 定义计数器
    counter = 0

    # 定义窗口布局
    layout = [
        [sg.Text('請轉動頭部')],
        [sg.Image(filename='', key='image')],
        [sg.Text('10', key='timer_text', font='Helvetica 20')],
    ]

    # 创建窗口
    window = sg.Window('Camera', layout)
    timer = time.time()
    while True:
        event, values = window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            break
        if timer is None and counter < 100:
            timer = time.time()
        ret, frame = cap.read()
        if ret:
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(data=imgbytes)

        elapsed_time = time.time() - timer

        if elapsed_time >= 0.1 and counter < 100:
            if not 'numpy.ndarray' in str(frame.__class__):
                continue


            filename = "/Users/slothsmba/Documents/Codes/Python/pythonProject/CGU project/0testing/"+num+"/" + str(counter) + '.jpg'
            cv2.imwrite(filename, frame)
            counter += 1
            counter_countdowm =  10 - counter//10
            window['timer_text'].update(str(counter_countdowm))
            timer = time.time()

        if counter >= 100:
            sg.popup_ok('拍攝完畢')
            break

    cap.release()
    cv2.destroyAllWindows()
    window.close()
    train(num)

def train(num):
    #TODO
    global name

    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # 載入人臉追蹤模型
    recog = cv2.face.LBPHFaceRecognizer_create()  # 啟用訓練人臉模型方法
    faces = []  # 儲存人臉位置大小的串列
    ids = []  # 記錄該人臉 id 的串列

    now_num = len(name)
    print(now_num)

    for i in range(1,100):
        filename = "/Users/slothsmba/Documents/Codes/Python/pythonProject/CGU project/0testing/"+num+"/"+str(i)+".jpg"
        img = cv2.imread(filename) # 依序開啟每一張蔡英文的照片
        if 'NoneType' in str(img.__class__):
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 色彩轉換成黑白
        img_np = np.array(gray,'uint8') # 轉換成指定編碼的 numpy 陣列
        face=detector.detectMultiScale(gray) # 擷取人臉區域
        for (x,y,w,h) in face:
            faces.append(img_np[y:y+h,x:x+w]) # 記錄人臉的位置和大小內像素的數值
            ids.append(now_num) # 記錄人臉對應的 id，只能是整數，都是 1 表示的 id 為 1

    print('training...') # 提示開始訓練
    recog.train(faces, np.array(ids, dtype=np.int32))
    recog.save('/Users/slothsmba/Documents/Codes/Python/pythonProject/CGU project/0testing/face_try.yml') # 訓練完成儲存為 face.yml
    name.append(num)
    print(name)


z=0

def work1(last_two,number):
    global z
    cap = cv2.VideoCapture(0)

    # 檢查攝像頭是否成功開啟
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # 讀取一張圖像以獲取攝像頭的尺寸
    ret, frame = cap.read()
    image_height, image_width, _ = frame.shape

    # 定義視窗佈局
    layout = [
        [sg.Image(filename='', key='image')],
        [sg.Button('Take Picture', key='-SHOOT-', size=(20, 2), font='Helvetica 14')],
        [sg.Button('確認照片', key='-CONFIRM-', size=(10, 2), font='Helvetica 14',visible=False)],
        [sg.Button('Exit', size=(10, 2), font='Helvetica 14')]
    ]

    window = sg.Window('Camera', layout)

    while True:
        event, values = window.read(timeout=20)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == '-SHOOT-':
            ret, frame = cap.read()
            filename = "/Users/slothsmba/Documents/Codes/Python/pythonProject/CGU project/0testing/photo.jpg"
            cv2.imwrite(filename, frame)
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(imgbytes)
            time.sleep(1)
            # show_picture(imgbytes)
            window['image'].Update(imgbytes)
            z = 1

        if z==0:
            ret, frame = cap.read()
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(data=imgbytes)

        elif z==1:
            print('z')
            print(z)
            window['image'].update(data=imgbytes)
            window['-SHOOT-'].update('CONFIRM')
            window['-CONFIRM-'].update(visible=True)
            window['-SHOOT-'].update(visible=False)

            if event == '-CONFIRM-':
                print('good')
                valid(number)
                break
            elif event == '-RETURN-':
                z=0
                window.close()
                work1()

    cap.release()
    cv2.destroyAllWindows()
    window.close()


if __name__ == '__main__':
    print("initializing")
    initial()
