
# process_image.py
import cv2
import mediapipe as mp
import numpy as np
from services.translate_api.gesture_rules import (
    one_hand_gestures, special_one_hand_gestures, two_hand_gestures
)


mp_hands = mp.solutions.hands

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
    states.append(1 if thumb_extended else 0)
    for tip, mcp in zip(tips[1:], mcps[1:]):
        extended = hand_landmarks.landmark[tip].y < hand_landmarks.landmark[mcp].y
        states.append(1 if extended else 0)
    angles = {}
    for i in range(4):
        angles[i+1] = calculate_angle_between_fingers(hand_landmarks, tips[i], mcps[i], tips[i+1], mcps[i+1])
    forwards = {
        "thumb_forward_angle": calculate_forward_angle(hand_landmarks, tips[0], mcps[0]),
        "index_forward_angle": calculate_forward_angle(hand_landmarks, tips[1], mcps[1]),
        "middle_forward_angle": calculate_forward_angle(hand_landmarks, tips[2], mcps[2]),
        "ring_forward_angle": calculate_forward_angle(hand_landmarks, tips[3], mcps[3]),
        "pinky_forward_angle": calculate_forward_angle(hand_landmarks, tips[4], mcps[4]),
    }
    return {"states": states, "angles": angles, "forwards": forwards}

def detect_gesture(image):
    image = cv2.flip(image, 1)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.7) as hands:
        results = hands.process(img_rgb)
        if not results.multi_hand_landmarks:
            return "Không nhận diện được tay"
        num_hands = len(results.multi_hand_landmarks)

        if num_hands == 1:
            status = get_finstatus(results.multi_hand_landmarks[0])
            states = status["states"]
            angles = status["angles"]
            forwards = status["forwards"]

            for gesture in special_one_hand_gestures:
                if states == gesture["pattern"]:
                    ok = True
                    for key, val in gesture.items():
                        if key.startswith("angle_"):
                            idx = int(key.split("_")[1])
                            if not (val[0] <= angles[idx] <= val[1]):
                                ok = False
                        elif key.endswith("_forward_angle"):
                            if not (val[0] <= forwards[key] <= val[1]):
                                ok = False
                    if ok:
                        return gesture["name"]

            for gesture in one_hand_gestures:
                if states == gesture["pattern"]:
                    ok = True
                    for key, val in gesture.items():
                        if key.startswith("angle_"):
                            idx = int(key.split("_")[1])
                            if not (val[0] <= angles[idx] <= val[1]):
                                ok = False
                        elif key.endswith("_forward_angle"):
                            if not (val[0] <= forwards[key] <= val[1]):
                                ok = False
                    if ok:
                        return gesture["name"]

            return "Không rõ"

        elif num_hands == 2:
            hands_states = []
            for hand_landmarks in results.multi_hand_landmarks:
                hands_states.append(get_finstatus(hand_landmarks)["states"])
            for gesture in two_hand_gestures:
                if hands_states == gesture["pattern"]:
                    return gesture["name"]
            return "Không rõ"

        return "Không rõ"

# process_image.py
import cv2
import mediapipe as mp
import numpy as np
from gesture_rules import one_hand_gestures, special_one_hand_gestures, two_hand_gestures

mp_hands = mp.solutions.hands

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
    states.append(1 if thumb_extended else 0)
    for tip, mcp in zip(tips[1:], mcps[1:]):
        extended = hand_landmarks.landmark[tip].y < hand_landmarks.landmark[mcp].y
        states.append(1 if extended else 0)
    angles = {}
    for i in range(4):
        angles[i+1] = calculate_angle_between_fingers(hand_landmarks, tips[i], mcps[i], tips[i+1], mcps[i+1])
    forwards = {
        "thumb_forward_angle": calculate_forward_angle(hand_landmarks, tips[0], mcps[0]),
        "index_forward_angle": calculate_forward_angle(hand_landmarks, tips[1], mcps[1]),
        "middle_forward_angle": calculate_forward_angle(hand_landmarks, tips[2], mcps[2]),
        "ring_forward_angle": calculate_forward_angle(hand_landmarks, tips[3], mcps[3]),
        "pinky_forward_angle": calculate_forward_angle(hand_landmarks, tips[4], mcps[4]),
    }
    return {"states": states, "angles": angles, "forwards": forwards}

def detect_gesture(image):
    image = cv2.flip(image, 1)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.7) as hands:
        results = hands.process(img_rgb)
        if not results.multi_hand_landmarks:
            return "Không nhận diện được tay"
        num_hands = len(results.multi_hand_landmarks)

        if num_hands == 1:
            status = get_finstatus(results.multi_hand_landmarks[0])
            states = status["states"]
            angles = status["angles"]
            forwards = status["forwards"]

            for gesture in special_one_hand_gestures:
                if states == gesture["pattern"]:
                    ok = True
                    for key, val in gesture.items():
                        if key.startswith("angle_"):
                            idx = int(key.split("_")[1])
                            if not (val[0] <= angles[idx] <= val[1]):
                                ok = False
                        elif key.endswith("_forward_angle"):
                            if not (val[0] <= forwards[key] <= val[1]):
                                ok = False
                    if ok:
                        return gesture["name"]

            for gesture in one_hand_gestures:
                if states == gesture["pattern"]:
                    ok = True
                    for key, val in gesture.items():
                        if key.startswith("angle_"):
                            idx = int(key.split("_")[1])
                            if not (val[0] <= angles[idx] <= val[1]):
                                ok = False
                        elif key.endswith("_forward_angle"):
                            if not (val[0] <= forwards[key] <= val[1]):
                                ok = False
                    if ok:
                        return gesture["name"]

            return "Không rõ"

        elif num_hands == 2:
            hands_states = []
            for hand_landmarks in results.multi_hand_landmarks:
                hands_states.append(get_finstatus(hand_landmarks)["states"])
            for gesture in two_hand_gestures:
                if hands_states == gesture["pattern"]:
                    return gesture["name"]
            return "Không rõ"

        return "Không rõ"

