import cv2
import mediapipe as mp
from gesture_rules import SINGLE_HAND_RULES, DOUBLE_HAND_RULES

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def get_finger_states(hand_landmarks):
    """Trả về mảng [ngón cái, trỏ, giữa, áp út, út], 1 = duỗi, 0 = gập"""
    finger_states = []

    # Ngón cái: so sánh x theo trục ngang
    finger_states.append(
        1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0
    )

    # Các ngón còn lại: so sánh y giữa khớp đầu và khớp giữa
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    for tip, pip in zip(finger_tips, finger_pips):
        finger_states.append(
            1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y else 0
        )

    return finger_states

def detect_gesture(fingers_list):
    """Xác định cử chỉ dựa vào số tay"""
    if len(fingers_list) == 1:
        pattern = fingers_list[0]
        for rule in SINGLE_HAND_RULES:
            if pattern == rule["pattern"]:
                return rule["label"]
        return "Không rõ"
    elif len(fingers_list) == 2:
        left_pattern, right_pattern = fingers_list
        for rule in DOUBLE_HAND_RULES:
            if (left_pattern == rule["left_pattern"] and
                right_pattern == rule["right_pattern"]):
                return rule["label"]
        return "Không rõ (2 tay)"
    else:
        return "Không phát hiện tay"

def process_image(image):
    """Xử lý ảnh và trả về kết quả nhận diện"""
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5
    ) as hands:

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.multi_hand_landmarks:
            return "Không phát hiện tay"

        fingers_list = [get_finger_states(hand_landmarks)
                        for hand_landmarks in results.multi_hand_landmarks]

        # Xác định kết quả
        result = detect_gesture(fingers_list)
        return result
