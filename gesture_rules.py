# gesture_rules.py
# Bộ quy tắc nhận dạng ký hiệu tay

# Ký hiệu 1 tay (mặc định tay phải)
# fingers = [thumb, index, middle, ring, pinky] (0: gập, 1: duỗi)
one_hand_gestures = [
    {
        "name": "A",
        "pattern": [0, 0, 0, 0, 0]
    },
    {
        "name": "B",
        "pattern": [0, 1, 1, 1, 1]
    },
    {
        "name": "L",
        "pattern": [1, 1, 0, 0, 0]
    },
    {
        "name": "V",
        "pattern": [0, 1, 1, 0, 0]
    },
    {
        "name": "W",
        "pattern": [0, 1, 1, 1, 0]
    },
    {
        "name": "Nắm tay",
        "pattern": [0, 0, 0, 0, 0]
    },
]

# Các ký hiệu 1 tay nhưng cần điều kiện phụ (góc hoặc khoảng cách)
special_one_hand_gestures = [
    {
        "name": "I Love You",
        "pattern": [1, 1, 0, 0, 1],
        "thumb_index_dist": 0.05  # khoảng cách nhỏ hơn giá trị này
    }
]

# Ký hiệu 2 tay
two_hand_gestures = [
    {
        "name": "Hai tay mở",
        "pattern": [
            [0, 1, 1, 1, 1],  # tay trái
            [0, 1, 1, 1, 1]   # tay phải
        ]
    }
]
