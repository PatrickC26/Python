import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
sw = 0
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            # print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        image_width = image.shape[1]
        image_height = image.shape[0]
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = face_mesh.process(image)
        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 取得左眼瞼座標
                L_EYE_UP_Y = face_landmarks.landmark[159].y
                L_EYE_BOTTOM_Y = face_landmarks.landmark[145].y
                L_EYE_VALUE = int((L_EYE_BOTTOM_Y - L_EYE_UP_Y) * image_height)
                L_EYE_LEFT_X = face_landmarks.landmark[137].x
                L_EYE_LEFT_Y = face_landmarks.landmark[137].y

                # 取得右眼瞼座標
                R_EYE_UP_Y = face_landmarks.landmark[386].y
                R_EYE_BOTTOM_Y = face_landmarks.landmark[374].y
                R_EYE_VALUE = int((R_EYE_BOTTOM_Y - R_EYE_UP_Y) * image_height)
                R_EYE_RIGHT_X = face_landmarks.landmark[359].x
                R_EYE_RIGHT_Y = face_landmarks.landmark[359].y

                if (L_EYE_VALUE > 11):
                    cv2.putText(image, 'OPEN', (int(image_width * L_EYE_LEFT_X), int(image_height * L_EYE_LEFT_Y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 6, cv2.LINE_AA)
                    cv2.putText(image, 'OPEN', (int(image_width * L_EYE_LEFT_X), int(image_height * L_EYE_LEFT_Y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                else:
                    cv2.putText(image, 'CLOSE', (int(image_width * L_EYE_LEFT_X), int(image_height * L_EYE_LEFT_Y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 6, cv2.LINE_AA)
                    cv2.putText(image, 'CLOSE', (int(image_width * L_EYE_LEFT_X), int(image_height * L_EYE_LEFT_Y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                if (R_EYE_VALUE > 11):
                    cv2.putText(image, 'OPEN', (int(image_width * R_EYE_RIGHT_X), int(image_height * R_EYE_RIGHT_Y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 6, cv2.LINE_AA)
                    cv2.putText(image, 'OPEN', (int(image_width * R_EYE_RIGHT_X), int(image_height * R_EYE_RIGHT_Y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                else:
                    cv2.putText(image, 'CLOSE', (int(image_width * R_EYE_RIGHT_X), int(image_height * R_EYE_RIGHT_Y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 6, cv2.LINE_AA)
                    cv2.putText(image, 'CLOSE', (int(image_width * R_EYE_RIGHT_X), int(image_height * R_EYE_RIGHT_Y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            # 畫出人臉網格mesh_map
            if (sw == 0):
                # jason-nano mediapipe
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    # connections=mp_face_mesh.FACE_CONNECTIONS,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec)
            # 本機mediapipe
            # 鍵盤偵測
        key = cv2.waitKey(5) & 0xFF
        if (key == 27) or (key == ord('q')):
            break
        elif (key == ord('s')):  # 按 s 鍵可拿掉 mesh_map
            sw = sw + 1
        if (sw == 2):
            sw = 0
        cv2.imshow('MediaPipe FaceMesh', image)
cap.release()