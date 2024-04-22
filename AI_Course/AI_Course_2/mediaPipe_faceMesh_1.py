import cv2
import mediapipe as mp

# 載入繪圖工具
mp_drawing = mp.solutions.drawing_utils
# 載入臉部關鍵點檢測模型
mp_face_mesh = mp.solutions.face_mesh

# 使用攝影機作為影像輸入
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

# 初始化臉部關鍵點檢測模型
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    # 讀取攝影機影像
    success, image = cap.read()

    if not success:
      print("Ignoring empty camera frame.")
      # 如果使用的是影片，使用break而非continue
      continue

    # 將圖像水平翻轉，以便在後續顯示時顯示自拍畫面，並將BGR格式的圖像轉換為RGB格式
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # 為了提高性能，可以將圖像標記為不可寫，以便通過引用傳遞
    image.flags.writeable = False
    # 進行臉部關鍵點檢測
    results = face_mesh.process(image)

    # 在圖像上繪製臉部關鍵點標記
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec)
    cv2.imshow('MediaPipe FaceMesh', image)
    # 如果按下ESC鍵，則跳出迴圈，關閉視窗
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()