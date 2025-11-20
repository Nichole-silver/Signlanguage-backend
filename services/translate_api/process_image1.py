# process_image.py (Nâng cấp)
import cv2
import mediapipe as mp
import numpy as np
from .gesture_rules import one_hand_gestures, special_one_hand_gestures, two_hand_gestures

mp_hands = mp.solutions.hands


def finger_distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def compute_score(states, gesture):
    base_pattern = gesture["pattern"]
    fd = finger_distance(states, base_pattern)
    score = 1 - fd / 5  # tolerance normalizer

    # bonus từ điều kiện phụ
    if "avg_finger_angle" in gesture:
        score += 0.15

    if "thumb_index_dist" in gesture:
        score += 0.20

    if "thumb_position" in gesture:
        score += 0.20

    if "thumb_between" in gesture:
        score += 0.20

    if "thumb_hidden_under" in gesture:
        score += 0.20

    return max(0, min(1, score))


def calculate_angle_between_fingers(hand_landmarks, tip1, mcp1, tip2, mcp2):
    v1 = np.array([
        hand_landmarks.landmark[tip1].x - hand_landmarks.landmark[mcp1].x,
        hand_landmarks.landmark[tip1].y - hand_landmarks.landmark[mcp1].y
    ])
    v2 = np.array([
        hand_landmarks.landmark[tip2].x - hand_landmarks.landmark[mcp2].x,
        hand_landmarks.landmark[tip2].y - hand_landmarks.landmark[mcp2].y
    ])
    cosang = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0)))


def calculate_forward_angle(hand_landmarks, tip_id, mcp_id):
    v = np.array([
        hand_landmarks.landmark[tip_id].x - hand_landmarks.landmark[mcp_id].x,
        hand_landmarks.landmark[tip_id].y - hand_landmarks.landmark[mcp_id].y
    ])
    angle = np.degrees(np.arctan2(v[1], v[0]))
    if angle < 0:
        angle += 360
    return angle


def get_finstatus(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    mcps = [2, 5, 9, 13, 17]

    states = []
    thumb_extended = hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[mcps[0]].x
    states.append(int(thumb_extended))

    for tip, mcp in zip(tips[1:], mcps[1:]):
        extended = hand_landmarks.landmark[tip].y < hand_landmarks.landmark[mcp].y
        states.append(int(extended))

    angles = {i + 1: calculate_angle_between_fingers(hand_landmarks, tips[i], mcps[i],
                                                     tips[i + 1], mcps[i + 1]) for i in range(4)}

    forwards = {name: calculate_forward_angle(hand_landmarks, tips[idx], mcps[idx])
                for idx, name in enumerate(
            ["thumb_forward_angle", "index_forward_angle", "middle_forward_angle",
             "ring_forward_angle", "pinky_forward_angle"])}

    return {"states": states, "angles": angles, "forwards": forwards}


def detect_gesture(image):
    image = cv2.flip(image, 1)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(static_image_mode=True, max_num_hands=2,
                        min_detection_confidence=0.7) as hands:

        results = hands.process(img_rgb)
        if not results.multi_hand_landmarks:
            return {"result": "Không nhận diện được tay", "top": []}

        num_hands = len(results.multi_hand_landmarks)

        # ===== ONE HAND =====
        if num_hands == 1:
            status = get_finstatus(results.multi_hand_landmarks[0])
            states = status["states"]

            scores = []

            for gesture in special_one_hand_gestures + one_hand_gestures:
                sc = compute_score(states, gesture)
                scores.append((gesture["name"], sc))

            scores.sort(key=lambda x: x[1], reverse=True)
            top3 = scores[:3]

            if top3[0][1] < 0.40:
                return {"result": "Không rõ", "top": top3}

            return {"result": top3[0][0], "top": top3}

        # ===== TWO HANDS =====
        elif num_hands == 2:
            hands_states = [get_finstatus(h)["states"] for h in results.multi_hand_landmarks]

            matched = []
            for g in two_hand_gestures:
                dist_left = finger_distance(hands_states[0], g["pattern"][0])
                dist_right = finger_distance(hands_states[1], g["pattern"][1])

                sc = 1 - (dist_left + dist_right) / 10
                matched.append((g["name"], sc))

            matched.sort(key=lambda x: x[1], reverse=True)

            if matched[0][1] < 0.40:
                return {"result": "Không rõ", "top": matched[:3]}

            return {"result": matched[0][0], "top": matched[:3]}

        return {"result": "Không rõ", "top": []}
