# gesture_rules.py
# Bộ quy tắc nhận dạng ký hiệu tay nâng cấp

one_hand_gestures = [
    {"name": "A", "pattern": [0,0,0,0,0], "thumb_index_dist": (">", 0.06)},
    {"name": "B", "pattern": [0,1,1,1,1]},
    {"name": "C", "pattern": [0,1,1,1,1], "thumb_index_angle": (40,80)},
    {"name": "D", "pattern": [0,1,0,0,0]},
    {"name": "E", "pattern": [0,0,0,0,0], "avg_finger_angle": ("<", 25)},
    {"name": "F", "pattern": [0,1,1,1,1]},
    {"name": "G", "pattern": [1,1,0,0,0]},
    {"name": "H", "pattern": [1,1,1,0,0]},
    {"name": "I", "pattern": [0,0,0,0,1]},
    {"name": "L", "pattern": [1,1,0,0,0]},
    {"name": "M", "pattern": [0,0,0,0,0], "thumb_hidden_under": 3},
    {"name": "N", "pattern": [0,0,0,0,0], "thumb_hidden_under": 2},
    {"name": "O", "pattern": [0,1,1,1,1]},
    {"name": "P", "pattern": [0,1,1,0,0]},
    {"name": "Q", "pattern": [1,1,0,0,0]},
    {"name": "R", "pattern": [0,1,1,0,0]},
    {"name": "S", "pattern": [0,0,0,0,0], "thumb_position": "over"},
    {"name": "T", "pattern": [0,0,0,0,0], "thumb_between": True},
    {"name": "U", "pattern": [0,1,1,0,0]},
    {"name": "V", "pattern": [0,1,1,0,0]},
    {"name": "W", "pattern": [0,1,1,1,0]},
    {"name": "X", "pattern": [0,1,0,0,0]},
    {"name": "Y", "pattern": [1,0,0,0,1]},
    {"name": "Z", "pattern": [0,1,0,0,0]},
    {"name": "Nắm tay", "pattern": [0,0,0,0,0]},

    {"name": "Tôi", "pattern": [0,1,0,0,0]},
    {"name": "Bạn", "pattern": [0,1,0,0,0]},
    {"name": "Vui", "pattern": [0,1,1,1,1]},
    {"name": "Buồn", "pattern": [0,0,0,0,0]},
]

special_one_hand_gestures = [
    {
        "name": "I Love You",
        "pattern": [1,1,0,0,1],
        "thumb_index_dist": ("<", 0.05)
    },
    {
        "name": "OK",
        "pattern": [0,1,1,1,1],
        "thumb_index_dist": ("<", 0.03)
    },
    {
        "name": "Point",
        "pattern": [0,1,0,0,0],
        "index_forward_angle": (160,200)
    }
]

two_hand_gestures = [
    {
        "name": "Hai tay mở",
        "pattern": [
            [0,1,1,1,1],
            [0,1,1,1,1]
        ]
    },
    {
        "name": "Hai tay chữ L",
        "pattern": [
            [1,1,0,0,0],
            [1,1,0,0,0]
        ]
    }
]
