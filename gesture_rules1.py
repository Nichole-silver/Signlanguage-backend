# gesture_rules.py
# fingers = [thumb, index, middle, ring, pinky] (0: gập, 1: duỗi)
# angles = {1: thumb-index, 2: index-middle, 3: middle-ring, 4: ring-pinky}
# forwards = {"index_forward_angle": ..., ...}

one_hand_gestures = [
    {"name": "A", "pattern": [0, 0, 0, 0, 0]},
    {"name": "B", "pattern": [0, 1, 1, 1, 1]},
    {"name": "C", "pattern": [0, 1, 1, 1, 1], "angle_1": (40, 80)},  # thumb-index mở vừa
    {"name": "Tôi yêu bạn", "pattern": [1, 1, 0, 0, 1]},
]

special_one_hand_gestures = [
    {"name": "OK", "pattern": [0, 1, 1, 1, 1], "angle_1": (10, 30)},
    {"name": "Point", "pattern": [0, 1, 0, 0, 0], "index_forward_angle": (160, 200)},
]

two_hand_gestures = [
    {"name": "Hai tay mở", "pattern": [[0, 1, 1, 1, 1], [0, 1, 1, 1, 1]]},
]
