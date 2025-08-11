# process_image.py
import cv2
import mediapipe as mp
import numpy as np
from gesture_rules import one_hand_rules, two_hand_rules
import operator

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Hàm so sánh điều kiện với toán tử
ops = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq
}

def detect_gesture_from_landmarks(landmarks, image_shape):
    """Xác định trạng thái các ngón tay từ landmarks"""
    fingers = []
    h, w = image_shape[:2]

    # Quy ước Mediapipe: Thumb(4), Index(8), Middle(12), Ring(16), Pinky(20)
    # Ngón cái
    fingers.append(1 if landmarks[4].x > landmarks[3].x else 0)
    # Các ngón còn lại
    tips = [8, 12, 16, 20]
    for tip in tips:
        fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)

    return fingers

def calc_thumb_index_dist(landmarks):
    """Tính khoảng cách giữa ngón cái và ngón trỏ"""
    p1 = np.array([landmarks[4].x, landmarks[4].y])
    p2 = np.array([landmarks[8].x, landmarks[8].y])
    return np.linalg.norm(p1 - p2)

def match_rule(fingers, extra_info, rules):
    """So khớp fingers và các điều kiện với rules"""
    for rule in rules:
        # Nếu là 1 tay
        if isinstance(rule["fingers"][0], int):
            if fingers == rule["fingers"]:
                matched = True
                for cond in rule["conditions"]:
                    if cond["type"] in extra_info:
                        if not ops[cond["op"]](extra_info[cond["type"]], cond["value"]):
                            matched = False
                            break
                if matched:
                    return rule["name"]

        # Nếu là 2 tay
        else:
            if fingers == rule["fingers"]:
                matched = True
                for cond in rule["conditions"]:
                    if cond["type"] in extra_info:
                        if not ops[cond["op"]](extra_info[cond["type"]], cond["value"]):
                            matched = False
                            break
                if matched:
                    return rule["name"]

    return "Không rõ"

def detect_gesture(image):
    """Nhận diện ký hiệu từ ảnh"""
    # Bỏ mirror để ảnh giống thực tế
    image = cv2.flip(image, 1)

    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.7
    ) as hands:
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_hand_landmarks:
            return "Không nhận diện được tay"

        hand_count = len(results.multi_hand_landmarks)

        if hand_count == 1:
            landmarks = results.multi_hand_landmarks[0].landmark
            fingers = detect_gesture_from_landmarks(landmarks, image.shape)
            extra_info = {
                "thumb_index_dist": calc_thumb_index_dist(landmarks)
            }
            return match_rule(fingers, extra_info, one_hand_rules)

        elif hand_count == 2:
            all_fingers = []
            for lm in results.multi_hand_landmarks:
                all_fingers.append(detect_gesture_from_landmarks(lm.landmark, image.shape))
            return match_rule(all_fingers, {}, two_hand_rules)

        return "Không rõ"
