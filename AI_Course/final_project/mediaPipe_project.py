import time

import cv2
import mediapipe as mp
import numpy as np
import functions


def detection(question_needed: int):
    # Constants
    SQUARE_SIZE = 200
    LABELS = [str(i) for i in range(1, 10)]
    WINDOW_NAME = 'Hand Gesture Recognition'

    # Initialize Mediapipe
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # Initialize OpenCV
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Initialize the square positions
    squares = []
    for i in range(3):
        for j in range(3):
            x = i * SQUARE_SIZE + 150
            y = j * SQUARE_SIZE + 50
            squares.append((x, y, SQUARE_SIZE, SQUARE_SIZE))

    # Initialize the square colors
    square_colors = [(255, 255, 255)] * 9  # Set square color to white

    # Initialize flags
    grabbed = False
    isGrabbedCounted = False
    grabbed_index = -1
    grabbed_index_pre = -1
    grabbed_timer = 0
    grabbed_time = -1

    # random number
    random_number_index = np.random.randint(0, 8)
    square_colors[random_number_index] = (255, 0, 255)  # Set square color to purple
    random_number_time = time.time()

    # question status
    total_question = 0
    correct_question = 0

    result = ""
    result_time = []

    # Main loop
    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while True:
            # Read frame from webcam
            ret, frame = cap.read()
            if not ret:
                continue

            # Flip the frame horizontally for a mirrored view
            frame = cv2.flip(frame, 1)

            # Convert the BGR frame to RGB and process it with Mediapipe
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            # Reset the square colors
            square_colors = [(255, 255, 255)] * 9  # Set square color to white
            square_colors[random_number_index] = (255, 0, 255)  # Set square color to purple

            # Detect hand landmarks and update the square colors
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for i, (x, y, w, h) in enumerate(squares):
                        # Check if hand is inside the square
                        fingers = functions.finger_distance(hand_landmarks, 0.1)

                        if x < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1] < x + w and \
                                y < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0] < y + h:
                            square_colors[i] = (255, 0, 0)  # Set square color to blue

                            # Check if the hand is grabbing the square

                            if (not grabbed) & (fingers == [0, 0, 0, 0, 0]) & (
                                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * frame.shape[1] <
                                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1]):
                                grabbed = True
                                grabbed_index = i
                                grabbed_timer = 10
                                grabbed_time = time.time() - random_number_time

            # Update the grabbed square color if it's being grabbed
            if grabbed:
                grabbed_timer -= 1

                if random_number_index == grabbed_index:
                    square_colors[grabbed_index] = (0, 255, 0)  # Set square color to Green
                    if not isGrabbedCounted:
                        if total_question != 0:
                            correct_question += 1
                            result += "Correct\tGrabbed: " + str(grabbed_index + 1) + \
                                      ",\ttarget is: " + str(random_number_index + 1) + \
                                      ",\tTime: " + str(round(grabbed_time, 2)) + "\n"
                            print("Touch Target : " + str(grabbed_index + 1))
                            result_time.append(grabbed_time)

                elif random_number_index != grabbed_index:
                    square_colors[grabbed_index] = (0, 0, 255)  # Set square color to red
                    if not isGrabbedCounted:
                        result += "Wrong\tGrabbed: " + str(grabbed_index + 1) + \
                                  ",\ttarget is: " + str(random_number_index + 1) + \
                                  ",\tTime: " + str(round(grabbed_time, 2)) + "\n"
                        print("Touch No Target : " + str(grabbed_index + 1) +
                              "   target is: " + str(random_number_index + 1))

                isGrabbedCounted = True

                if grabbed_timer == 0:
                    grabbed = False
                    isGrabbedCounted = False
                    grabbed_index = -1
                    random_number_index = np.random.randint(0, 8)
                    square_colors[random_number_index] = (255, 0, 255)  # Set square color to purple
                    random_number_time = time.time()
                    total_question += 1

            # Draw squares on the frame
            for i, (x, y, w, h) in enumerate(squares):
                # cv2.rectangle(frame, (x, y), (x + w, y + h), square_colors[i], -1)

                alpha = 0.7
                overlay = frame.copy()
                cv2.rectangle(overlay, (x, y), (x + w, y + h), square_colors[i], -1)
                frame = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)

                label_size, _ = cv2.getTextSize(LABELS[i], cv2.FONT_HERSHEY_SIMPLEX, 2, 3)
                cv2.putText(frame, LABELS[i], (x + w // 2 - label_size[0] // 2, y + h // 2 + label_size[1] // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

            if grabbed:
                cv2.putText(frame, "time: " + str("{:.2f}".format(grabbed_time)), (3 * SQUARE_SIZE + 200, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
            else:
                cv2.putText(frame, "time: " + str("{:.2f}".format(time.time() - random_number_time)),
                            (3 * SQUARE_SIZE + 200, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

            if total_question == 0:
                cv2.putText(frame, "Testing", (3 * SQUARE_SIZE + 200, 230), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255),
                            5)
            else:
                cv2.putText(frame, "accuracy: " + str(correct_question) + '/' + str(total_question),
                            (3 * SQUARE_SIZE + 200, 230), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

            cv2.putText(frame, "total: " + str(question_needed), (3 * SQUARE_SIZE + 200, 330), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 0, 0), 3)

            if (question_needed + 1) == total_question:
                break

            # Display the frame
            cv2.imshow(WINDOW_NAME, frame)

            # Check for key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the video capture and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    print(result_time)

    return "Accuracy of the Detection: " + str(
        "{:.2f}".format(correct_question * 100 / question_needed)) + " % ( " + str(correct_question) + "/" + str(
        question_needed) + " ) " + "\n" \
                                   "Average Time of the Detection: " + str(
        "{:.2f}".format(np.average(result_time))) + "\n" + \
           "\n\nIndividual Data are as follow: \n" + \
           result + \
           "\n--------------------------------------------------------\n\n"


if __name__ == '__main__':
    detection(3)
