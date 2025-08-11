import cv2
import mediapipe as mp
import numpy as np
from gesture_rules import SINGLE_HAND_RULES, DOUBLE_HAND_RULES

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def get_finger_states(hand_landmarks):
    """
    Xác định trạng thái các ngón tay (0 = co, 1 = duỗi) cho tay phải của người dùng.
    Ảnh chụp từ camera trước KHÔNG bị mirror.
    """
    lm = hand_landmarks.landmark
    states = []

    # Thumb (ngón cái) - tay phải thật
    # Trong ảnh không mirror: thumb mở ra ngoài thì x > pip_x
    states.append(1 if lm[4].x > lm[3].x else 0)

    # Các ngón còn lại (trỏ, giữa, áp út, út)
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    for t, p in zip(tips, pips):
        states.append(1 if lm[t].y < lm[p].y else 0)

    return states


def match_pattern(actual, target, tolerance=0):
    """So khớp pattern với ngưỡng tolerance (sai tối đa tolerance ngón)"""
    if len(actual) != len(target):
        return False
    diff = sum(1 for a, b in zip(actual, target) if a != b)
    return diff <= tolerance


def detect_gesture(image, debug=False):
    """
    Nhận diện ký hiệu tay từ ảnh tĩnh.
    Trả về tên ký hiệu hoặc thông báo không rõ.
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w, _ = image.shape

    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5
    ) as hands:

        results = hands.process(image_rgb)
        if not results.multi_hand_landmarks:
            if debug:
                print("[detect_gesture] Không phát hiện tay")
            return "Không nhận diện được tay"

        num_hands = len(results.multi_hand_landmarks)
        if debug:
            print(f"[detect_gesture] Số tay phát hiện: {num_hands}")

        # Nếu chỉ có 1 tay → xử lý như tay phải
        if num_hands == 1:
            states = get_finger_states(results.multi_hand_landmarks[0])
            if debug:
                print("[detect_gesture] Pattern tay phải:", states)

            for rule in SINGLE_HAND_RULES:
                if match_pattern(states, rule["pattern"], tolerance=1):
                    if debug:
                        print("[detect_gesture] Khớp SINGLE:", rule["label"])
                    return rule["label"]

            if debug:
                print("[detect_gesture] Không khớp rule tay phải")
            return "Không rõ"

        # Nếu có 2 tay → dò trong DOUBLE_HAND_RULES
        elif num_hands == 2:
            patterns = []
            for lm in results.multi_hand_landmarks:
                patterns.append(get_finger_states(lm))
            if debug:
                print("[detect_gesture] Patterns 2 tay:", patterns)

            for rule in DOUBLE_HAND_RULES:
                if all(match_pattern(p, r, tolerance=1) for p, r in zip(patterns, rule["patterns"])):
                    if debug:
                        print("[detect_gesture] Khớp DOUBLE:", rule["label"])
                    return rule["label"]

            if debug:
                print("[detect_gesture] Không khớp rule 2 tay")
            return "Không rõ"
