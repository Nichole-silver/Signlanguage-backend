# process_image.py
import cv2
import numpy as np
import mediapipe as mp
from gesture_rules import GESTURE_RULES_ONE_HAND, GESTURE_RULES_TWO_HANDS

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def calculate_normalized_distance(hand_landmarks, id1, id2):
    """Tính khoảng cách chuẩn hóa giữa 2 điểm landmark"""
    p1 = np.array([hand_landmarks.landmark[id1].x, hand_landmarks.landmark[id1].y])
    p2 = np.array([hand_landmarks.landmark[id2].x, hand_landmarks.landmark[id2].y])
    dist = np.linalg.norm(p1 - p2)

    wrist = np.array([hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y])
    middle_tip = np.array([hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y])
    hand_length = np.linalg.norm(wrist - middle_tip)

    return dist / hand_length if hand_length > 0 else dist

def get_finger_state(hand_landmarks):
    """Xác định trạng thái các ngón tay: 1 = duỗi, 0 = gập"""
    fingers = []

    # Ngón cái
    fingers.append(1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)

    # Các ngón còn lại
    tips_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]

    for tip, pip in zip(tips_ids, pip_ids):
        fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y else 0)

    return fingers

def match_pattern(fingers, pattern, tolerance=0):
    """So khớp fingers với pattern, cho phép tolerance"""
    return all(abs(f - p) <= tolerance for f, p in zip(fingers, pattern))

def detect_gesture(image):
    """Phân tích ảnh và trả về tên ký hiệu"""
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
        results = hands.process(image_rgb)

        if not results.multi_hand_landmarks:
            return "Không nhận diện được tay"

        num_hands = len(results.multi_hand_landmarks)

        # === Một tay ===
        if num_hands == 1:
            hand_landmarks = results.multi_hand_landmarks[0]
            fingers = get_finger_state(hand_landmarks)

            for gesture in GESTURE_RULES_ONE_HAND:
                if match_pattern(fingers, gesture["pattern"], tolerance=0):
                    # Nếu gesture cần kiểm tra khoảng cách
                    if "thumb_index_dist" in gesture:
                        dist = calculate_normalized_distance(hand_landmarks, 4, 8)
                        if abs(dist - gesture["thumb_index_dist"]) <= 0.02:
                            return gesture["name"]
                    else:
                        return gesture["name"]

            return "Không rõ"

        # === Hai tay ===
        elif num_hands == 2:
            hands_fingers = [get_finger_state(hand) for hand in results.multi_hand_landmarks]

            for gesture in GESTURE_RULES_TWO_HANDS:
                pattern = gesture["pattern"]

                if (hands_fingers == pattern) or (hands_fingers[::-1] == pattern):
                    return gesture["name"]

            return "Không rõ"

        return "Không rõ"
