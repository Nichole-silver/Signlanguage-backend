# process_image.py
import cv2
import mediapipe as mp
import numpy as np
import math
from gesture_rules import SINGLE_HAND_RULES, DOUBLE_HAND_RULES

mp_hands = mp.solutions.hands

def _calc_dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def get_finger_states(hand_landmarks):
    """
    Trả về mảng 5 phần tử: [thumb, index, middle, ring, pinky] (1=duỗi, 0=gập)
    Dùng rules đơn giản: thumb so sánh tip.x vs ip.x, others compare tip.y vs pip.y.
    """
    lm = hand_landmarks.landmark
    states = []
    try:
        # Thumb: so sánh tip (4) với ip (3)
        states.append(1 if lm[4].x < lm[3].x else 0)
    except Exception:
        states.append(0)

    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    for t, p in zip(tips, pips):
        try:
            states.append(1 if lm[t].y < lm[p].y else 0)
        except Exception:
            states.append(0)
    return states

def detect_gesture(image, debug=False):
    """
    Input:
      - image: numpy.ndarray BGR (cv2.imread or image from Flask)
      - debug: nếu True sẽ print log chi tiết
    Output: label string (ví dụ "V", "Không phát hiện tay", "Không rõ", ...)
    """
    if image is None:
        if debug: print("[detect_gesture] image is None")
        return "Không phát hiện tay"

    if not isinstance(image, np.ndarray):
        if debug: print("[detect_gesture] image is not numpy array:", type(image))
        return "Không phát hiện tay"

    if image.size == 0:
        if debug: print("[detect_gesture] image empty")
        return "Không phát hiện tay"

    if debug:
        print("[detect_gesture] image.shape:", getattr(image, "shape", None), "dtype:", image.dtype, "min/max:", np.min(image), np.max(image))

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Tweak params: giảm min_detection_confidence nếu môi trường khó
    with mp_hands.Hands(static_image_mode=True,
                        max_num_hands=2,
                        model_complexity=1,
                        min_detection_confidence=0.35) as hands:
        result = hands.process(img_rgb)

        if debug:
            print("[detect_gesture] Mediapipe result:", result)
            # result.multi_hand_landmarks thường là None hoặc list
            print("[detect_gesture] multi_hand_landmarks:", bool(result.multi_hand_landmarks))
            print("[detect_gesture] multi_handedness:", bool(result.multi_handedness))

        if not result.multi_hand_landmarks:
            if debug: print("[detect_gesture] No hand landmarks detected")
            return "Không phát hiện tay"

        # number of detected hands
        n_hands = len(result.multi_hand_landmarks)
        if debug: print(f"[detect_gesture] Detected hands: {n_hands}")

        # Build pairs (handedness label + landmarks)
        labeled = []
        if result.multi_handedness and len(result.multi_handedness) == len(result.multi_hand_landmarks):
            for ch, lm in zip(result.multi_handedness, result.multi_hand_landmarks):
                label = ch.classification[0].label  # 'Left' or 'Right'
                score = ch.classification[0].score
                labeled.append((label, lm, score))
            if debug: print("[detect_gesture] Handedness labels:", [(l,s) for l,_,s in labeled])
            # sort left then right to have consistent order
            labeled.sort(key=lambda x: 0 if x[0] == "Left" else 1)
            fingers_list = []
            for lbl, lm, sc in labeled:
                st = get_finger_states(lm)
                fingers_list.append((lbl, st))
                if debug: print(f"[detect_gesture] {lbl} finger states:", st)
            # keep only states (left then right)
            patterns = [p for _, p in fingers_list]
        else:
            # if no handedness info, fallback to order returned
            patterns = []
            for lm in result.multi_hand_landmarks:
                st = get_finger_states(lm)
                patterns.append(st)
                if debug: print("[detect_gesture] finger states:", st)

        # SINGLE hand
        if len(patterns) == 1:
            pattern = patterns[0]
            if debug: print("[detect_gesture] single-hand pattern:", pattern)
            for rule in SINGLE_HAND_RULES:
                if pattern == rule["pattern"]:
                    if debug: print("[detect_gesture] matched SINGLE rule:", rule)
                    return rule["label"]
            if debug: print("[detect_gesture] no single-hand match")
            return "Không rõ"

        # DOUBLE hands
        elif len(patterns) == 2:
            left_pattern, right_pattern = patterns[0], patterns[1]
            if debug: print("[detect_gesture] two-hand patterns:", left_pattern, right_pattern)
            for rule in DOUBLE_HAND_RULES:
                if left_pattern == rule["left_pattern"] and right_pattern == rule["right_pattern"]:
                    if debug: print("[detect_gesture] matched DOUBLE rule:", rule)
                    return rule["label"]
            if debug: print("[detect_gesture] no double-hand match")
            return "Không rõ (2 tay)"

        else:
            if debug: print("[detect_gesture] unexpected hand count:", len(patterns))
            return "Không rõ"
