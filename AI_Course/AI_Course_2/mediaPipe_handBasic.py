# 導入必要的庫
import cv2
import mediapipe as mp
# 導入 MediaPipe 工具包中的繪圖函數和手部檢測模型
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# 打開攝像頭
cap = cv2.VideoCapture(0)
# 創建 Hand 模型對象,並設置檢測和跟踪的置信度閾值
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
  # 循環讀取攝像頭數據並處理
  while cap.isOpened():
    success, image = cap.read() # 讀取㇐幀圖像
    if not success:
      # print(“Ignoring empty camera frame.”) # 如果圖像為空則跳過”“
      continue
    # 如果讀取的是視頻,使用 'break' 跳出循環
    # 對圖像進行水平翻轉和顏色空間轉換(BGR to RGB)
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # 優化性能,將圖像設置為不可寫入
    image.flags.writeable = False
    # 處理圖像,獲取檢測結果
    results = hands.process(image)
    # 將圖像設置為可寫入
    image.flags.writeable = True
    # 將 RGB 圖像轉換為 BGR 圖像
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # 如果檢測到多個手部,則在圖像上繪製每個手部的關鍵點和連接線
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        # 顯示帶有手部關鍵點的圖像
        cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27: # 按下 'ESC' 鍵退出循環
      cap.release() # 釋放攝像頭並關閉窗口
      break

