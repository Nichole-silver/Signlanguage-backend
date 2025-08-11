# gesture_rules.py
# Danh sách các gesture mẫu cho 1 tay và 2 tay
# fingers pattern: [thumb, index, middle, ring, pinky] (1 = duỗi, 0 = gập)
# distance: khoảng cách chuẩn hóa (nếu cần)
# angle: góc giữa các ngón (nếu cần)

# Các gesture 1 tay
GESTURE_RULES_ONE_HAND = [
    {"name": "B", "pattern": [0, 1, 1, 1, 1]},
    {"name": "L", "pattern": [0, 1, 0, 0, 0]},
    {"name": "V", "pattern": [0, 1, 1, 0, 0]},
    {"name": "Nắm tay", "pattern": [0, 0, 0, 0, 0]},
    {"name": "I Love You", "pattern": [1, 1, 0, 0, 1], "thumb_index_dist": 0.05},
]

# Các gesture 2 tay
GESTURE_RULES_TWO_HANDS = [
    {
        "name": "Hai tay mở",
        "pattern": [[0, 1, 1, 1, 1], [0, 1, 1, 1, 1]]
    },
    {
        "name": "Hai nắm tay",
        "pattern": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    }
]
