import math
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands


def finger_distance(hand_landmarks, thersshold):
    INDEX_FINGER_TIP_X_value = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
    INDEX_FINGER_TIP_Y_value = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    # print(INDEX_FINGER_TIP_X_value,INDEX_FINGER_TIP_Y_value)

    INDEX_FINGER_MCP_X_value = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
    INDEX_FINGER_MCP_Y_value = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
    # print(INDEX_FINGER_MCP_X_value,INDEX_FINGER_MCP_Y_value)

    p1 = np.array([INDEX_FINGER_TIP_X_value, INDEX_FINGER_TIP_Y_value])
    p2 = np.array([INDEX_FINGER_MCP_X_value, INDEX_FINGER_MCP_Y_value])
    p3 = p2 - p1
    distance_INDEX = math.hypot(p3[0], p3[1])
    # print(distance_text)

    MIDDLE_FINGER_TIP_X_value = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
    MIDDLE_FINGER_TIP_Y_value = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    # print(INDEX_FINGER_TIP_X_value,INDEX_FINGER_TIP_Y_value)

    MIDDLE_FINGER_MCP_X_value = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
    MIDDLE_FINGER_MCP_Y_value = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
    # print(INDEX_FINGER_MCP_X_value,INDEX_FINGER_MCP_Y_value)

    p4 = np.array([MIDDLE_FINGER_TIP_X_value, MIDDLE_FINGER_TIP_Y_value])
    p5 = np.array([MIDDLE_FINGER_MCP_X_value, MIDDLE_FINGER_MCP_Y_value])
    p6 = p5 - p4
    distance_MIDDLE = math.hypot(p6[0], p6[1])

    RING_FINGER_TIP_X_value = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
    RING_FINGER_TIP_Y_value = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
    # print(INDEX_FINGER_TIP_X_value,INDEX_FINGER_TIP_Y_value)

    RING_FINGER_MCP_X_value = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x
    RING_FINGER_MCP_Y_value = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y
    # print(INDEX_FINGER_MCP_X_value,INDEX_FINGER_MCP_Y_value)

    p7 = np.array([RING_FINGER_TIP_X_value, RING_FINGER_TIP_Y_value])
    p8 = np.array([RING_FINGER_MCP_X_value, RING_FINGER_MCP_Y_value])
    p9 = p8 - p7
    distance_RING = math.hypot(p9[0], p9[1])

    PINKY_TIP_X_value = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
    PINKY_TIP_Y_value = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
    # print(INDEX_FINGER_TIP_X_value,INDEX_FINGER_TIP_Y_value)

    PINKY_MCP_X_value = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x
    PINKY_MCP_Y_value = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y
    # print(INDEX_FINGER_MCP_X_value,INDEX_FINGER_MCP_Y_value)

    p10 = np.array([PINKY_TIP_X_value, PINKY_TIP_Y_value])
    p11 = np.array([PINKY_MCP_X_value, PINKY_MCP_Y_value])
    p12 = p11 - p10
    distance_PINKY = math.hypot(p12[0], p12[1])

    THUMB_TIP_X_value = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
    THUMB_TIP_Y_value = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
    # print(INDEX_FINGER_TIP_X_value,INDEX_FINGER_TIP_Y_value)

    THUMB_MCP_X_value = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x
    THUMB_MCP_Y_value = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y
    # print(INDEX_FINGER_MCP_X_value,INDEX_FINGER_MCP_Y_value)

    p13 = np.array([THUMB_TIP_X_value, THUMB_TIP_Y_value])
    p14 = np.array([THUMB_MCP_X_value, THUMB_MCP_Y_value])
    p15 = p14 - p13
    distance_THUMB = math.hypot(p15[0], p15[1])

    thumb_up = (distance_THUMB > thersshold)
    index_up = (distance_INDEX > thersshold)
    middle_up = (distance_MIDDLE > thersshold)
    ring_up = (distance_RING > thersshold)
    pinky_up = (distance_PINKY > thersshold)

    return [thumb_up, index_up, middle_up, ring_up, pinky_up]
