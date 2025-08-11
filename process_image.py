# process_image.py
import cv2
import mediapipe as mp
import numpy as np
from gesture_rules import one_hand_rules, two_hand_rules

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def fingers_up(hand_landmarks):
    """
    Xác định trạng thái 5 ngón tay: 1 = duỗi, 0 = gập
    Dành cho tay phải, ảnh đã được flip để không bị mirror
    """
    finger_states = []
    tips_ids = [4, 8, 12, 16, 20]
    pip_ids = [2, 6, 10, 14, 18]

    # Ngón cái (xét trục X)
    if hand_landmarks.landmark[tips_ids[0]].x > hand_landmarks.landmark[pip_ids[0]].x:
        finger_states.append(1)
    else:
        finger_states.append(0)

    # 4 ngón còn lại (xét trục Y)
    for tip, pip in zip(tips_ids[1:], pip_ids[1:]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            finger_states.append(1)
        else:
            finger_states.append(0)

    return finger_states


def detect_gesture(image):
    """
    Phân tích ảnh, trả về tên ký hiệu
    """
    # Flip ảnh để giống góc nhìn thực tế (người đối diện)
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(static_image_mode=True,
                        max_num_hands=2,
                        min_detection_confidence=0.5) as hands:

        results = hands.process(image_rgb)

        if not results.multi_hand_landmarks:
            return "Không nhận diện được tay"

        num_hands = len(results.multi_hand_landmarks)

        # ===== 1 tay =====
        if num_hands == 1:
            hand_landmarks = results.multi_hand_landmarks[0]
            fingers = fingers_up(hand_landmarks)

            # Dò nhanh trong rule 1 tay
            for rule in one_hand_rules:
                if fingers == rule["pattern"]:
                    # Kiểm tra điều kiện phụ nếu có
                    if "thumb_index_dist_max" in rule:
                        thumb_tip = hand_landmarks.landmark[4]
                        index_tip = hand_landmarks.landmark[8]
                        dist = np.sqrt((thumb_tip.x - index_tip.x) ** 2 +
                                       (thumb_tip.y - index_tip.y) ** 2)
                        if dist > rule["thumb_index_dist_max"]:
                            continue
                    return rule["name"]

            return "Không rõ"

        # ===== 2 tay =====
        elif num_hands == 2:
            hands_fingers = []
            for hand_landmarks in results.multi_hand_landmarks:
                hands_fingers.append(fingers_up(hand_landmarks))

            left_fingers, right_fingers = hands_fingers

            for rule in two_hand_rules:
                if left_fingers == rule["pattern_left"] and right_fingers == rule["pattern_right"]:
                    return rule["name"]

            return "Không rõ"

        return "Không rõ"
