# process_image.py
import cv2
import mediapipe as mp
import numpy as np
from gesture_rules import one_hand_gestures, special_one_hand_gestures, two_hand_gestures

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def fingers_up(hand_landmarks):
    """
    Xác định trạng thái các ngón: 1 = duỗi, 0 = gập
    Ảnh đã được flip để khớp với góc nhìn thực tế
    """
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Ngón cái
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 ngón còn lại
    for id in range(1, 5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def calculate_thumb_index_distance(hand_landmarks):
    """Tính khoảng cách giữa ngón cái và ngón trỏ"""
    thumb_tip = np.array([hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y])
    index_tip = np.array([hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y])
    return np.linalg.norm(thumb_tip - index_tip)

def detect_gesture(image):
    """
    Nhận diện ký hiệu tay từ ảnh
    """
    image = cv2.flip(image, 1)  # lật ảnh để giống thực tế
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.7
    ) as hands:

        results = hands.process(img_rgb)

        if not results.multi_hand_landmarks:
            return "Không nhận diện được tay"

        num_hands = len(results.multi_hand_landmarks)

        if num_hands == 1:
            # ---- XỬ LÝ 1 TAY ----
            hand_landmarks = results.multi_hand_landmarks[0]
            fingers = fingers_up(hand_landmarks)

            # 1. Kiểm tra special gestures
            for gesture in special_one_hand_gestures:
                if fingers == gesture["pattern"]:
                    dist = calculate_thumb_index_distance(hand_landmarks)
                    if dist < gesture["thumb_index_dist"]:
                        return gesture["name"]

            # 2. Kiểm tra gesture thường
            for gesture in one_hand_gestures:
                if fingers == gesture["pattern"]:
                    return gesture["name"]

            return "Không rõ"

        elif num_hands == 2:
            # ---- XỬ LÝ 2 TAY ----
            hands_fingers = []
            for hand_landmarks in results.multi_hand_landmarks:
                hands_fingers.append(fingers_up(hand_landmarks))

            # Duyệt các pattern 2 tay
            for gesture in two_hand_gestures:
                if hands_fingers == gesture["pattern"]:
                    return gesture["name"]

            return "Không rõ"

        return "Không rõ"
