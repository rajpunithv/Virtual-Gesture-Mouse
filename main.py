import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)

# Cursor smoothing
prev_x, prev_y = 0, 0
smooth_factor = 7

# Debounce timers
last_click_time = 0
last_scroll_time = 0
click_delay = 0.4
scroll_delay = 0.3

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    action = "None"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark

            index_up = lm[8].y < lm[6].y
            middle_up = lm[12].y < lm[10].y
            ring_up = lm[16].y < lm[14].y
            pinky_up = lm[20].y < lm[18].y
            thumb_up = lm[4].x < lm[3].x

            thumb = (int(lm[4].x * w), int(lm[4].y * h))
            index = (int(lm[8].x * w), int(lm[8].y * h))
            middle = (int(lm[12].x * w), int(lm[12].y * h))

            def dist(a, b):
                return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5

            if index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
                screen_x = np.interp(index[0], [0, w], [0, screen_w])
                screen_y = np.interp(index[1], [0, h], [0, screen_h])
                curr_x = prev_x + (screen_x - prev_x) / smooth_factor
                curr_y = prev_y + (screen_y - prev_y) / smooth_factor
                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y
                action = "Pointer Move"

            elif dist(index, thumb) < 40 and not middle_up:
                if time.time() - last_click_time > click_delay:
                    pyautogui.click()
                    last_click_time = time.time()
                action = "Left Click"

            elif dist(index, thumb) < 40 and dist(middle, thumb) < 40:
                if time.time() - last_click_time > click_delay:
                    pyautogui.rightClick()
                    last_click_time = time.time()
                action = "Right Click"

            elif index_up and middle_up and ring_up and pinky_up and not thumb_up:
                if time.time() - last_scroll_time > scroll_delay:
                    pyautogui.scroll(100)
                    last_scroll_time = time.time()
                action = "Scroll Up"
            elif not index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
                if time.time() - last_scroll_time > scroll_delay:
                    pyautogui.scroll(-100)
                    last_scroll_time = time.time()
                action = "Scroll Down"

    cv2.putText(frame, f"Action: {action}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
