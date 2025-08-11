import cv2
import mediapipe as mp
import numpy as np
from gesture_rules import SINGLE_HAND_RULES, DOUBLE_HAND_RULES

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# --- Hàm đảo ngược bàn tay (vì camera trước lật hình) ---
def mirror_finger_data(fingers):
    return [fingers[0]] + fingers[1:][::-1]  # giữ nguyên ngón cái, đảo thứ tự 4 ngón còn lại

# --- Hàm xác định trạng thái ngón ---
def get_finger_states(hand_landmarks):
    # Các mốc tay trong Mediapipe: https://google.github.io/mediapipe/solutions/hands
    tips = [4, 8, 12, 16, 20]
    pips = [3, 6, 10, 14, 18]

    fingers = []
    # Ngón cái (so sánh x theo chiều ngang)
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[pips[0]].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Các ngón còn lại (so sánh y theo chiều dọc)
    for tip, pip in zip(tips[1:], pips[1:]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

# --- Hàm so khớp với tolerance ---
def match_pattern(detected, pattern, tolerance=0):
    diff = sum(1 for d, p in zip(detected, pattern) if d != p)
    return diff <= tolerance

# --- Hàm nhận diện ---
def detect_gesture(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5
    ) as hands:
        results = hands.process(image_rgb)

        if not results.multi_hand_landmarks:
            return "Không nhận diện được tay"

        hand_count = len(results.multi_hand_landmarks)

        if hand_count == 1:
            # --- Xử lý tay phải (ảnh mirror) ---
            fingers = get_finger_states(results.multi_hand_landmarks[0])
            fingers = mirror_finger_data(fingers)

            # Ưu tiên nhận dạng exact match cho ký hiệu đặc trưng
            for rule in SINGLE_HAND_RULES:
                if rule.get("strict", False) and match_pattern(fingers, rule["pattern"], tolerance=0):
                    return rule["label"]

            # Sau đó mới dùng tolerance cho ký hiệu dễ lệch
            for rule in SINGLE_HAND_RULES:
                if match_pattern(fingers, rule["pattern"], tolerance=1):
                    return rule["label"]

        elif hand_count == 2:
            # Xử lý hai tay
            fingers_list = []
            for hl in results.multi_hand_landmarks:
                fingers_list.append(mirror_finger_data(get_finger_states(hl)))

            for rule in DOUBLE_HAND_RULES:
                if all(match_pattern(f, p, tolerance=1) for f, p in zip(fingers_list, rule["patterns"])):
                    return rule["label"]

        return "Không rõ"
