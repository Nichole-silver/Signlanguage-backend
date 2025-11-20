# gesture_rules.py
# Bộ quy tắc nhận dạng ký hiệu tay

# === Ký hiệu 1 tay (mặc định tay phải) ===
# fingers = [thumb, index, middle, ring, pinky] (0: gập, 1: duỗi)
one_hand_gestures = [
    {"name": "A", "pattern": [0, 0, 0, 0, 0]},
    {"name": "B", "pattern": [0, 1, 1, 1, 1]},
    {"name": "C", "pattern": [0, 1, 1, 1, 1], "thumb_index_angle": (40, 80)},  # cong như chữ C
    {"name": "D", "pattern": [0, 1, 0, 0, 0]},
    {"name": "E", "pattern": [0, 0, 0, 0, 0]},  # tương tự A nhưng bàn tay khum
    {"name": "F", "pattern": [0, 1, 1, 1, 1]},  # ngón cái chạm ngón trỏ (OK)
    {"name": "G", "pattern": [1, 1, 0, 0, 0]},
    {"name": "H", "pattern": [1, 1, 1, 0, 0]},
    {"name": "I", "pattern": [0, 0, 0, 0, 1]},
    {"name": "L", "pattern": [1, 1, 0, 0, 0]},
    {"name": "M", "pattern": [0, 0, 0, 0, 0]},  # ngón cái giấu dưới 3 ngón
    {"name": "N", "pattern": [0, 0, 0, 0, 0]},  # ngón cái giấu dưới 2 ngón
    {"name": "O", "pattern": [0, 1, 1, 1, 1]},  # tạo hình tròn
    {"name": "P", "pattern": [0, 1, 1, 0, 0]},
    {"name": "Q", "pattern": [1, 1, 0, 0, 0]},  # giống G nhưng hướng xuống
    {"name": "R", "pattern": [0, 1, 1, 0, 0]},  # trỏ và giữa bắt chéo
    {"name": "S", "pattern": [0, 0, 0, 0, 0]},  # nắm tay
    {"name": "T", "pattern": [0, 0, 0, 0, 0]},  # ngón cái kẹp giữa trỏ và giữa
    {"name": "U", "pattern": [0, 1, 1, 0, 0]},
    {"name": "V", "pattern": [0, 1, 1, 0, 0]},
    {"name": "W", "pattern": [0, 1, 1, 1, 0]},
    {"name": "X", "pattern": [0, 1, 0, 0, 0]},  # trỏ cong
    {"name": "Y", "pattern": [1, 0, 0, 0, 1]},
    {"name": "Z", "pattern": [0, 1, 0, 0, 0]},  # vẽ chữ Z
    {"name": "Nắm tay", "pattern": [0, 0, 0, 0, 0]},
    # Biểu cảm / từ thông dụng
    {"name": "Tôi", "pattern": [0, 1, 0, 0, 0]},
    {"name": "Bạn", "pattern": [0, 1, 0, 0, 0]},
    {"name": "Vui", "pattern": [0, 1, 1, 1, 1]},
    {"name": "Buồn", "pattern": [0, 0, 0, 0, 0]},
]

# === Các ký hiệu 1 tay nhưng cần điều kiện phụ ===
special_one_hand_gestures = [
    {
        "name": "I Love You",
        "pattern": [1, 1, 0, 0, 1],
        "thumb_index_dist": ("<", 0.05)
    },
    {
        "name": "OK",
        "pattern": [0, 1, 1, 1, 1],
        "thumb_index_dist": ("<", 0.03)
    },
    {
        "name": "Point",
        "pattern": [0, 1, 0, 0, 0],
        "index_forward_angle": (160, 200)
    }
]

# === Ký hiệu 2 tay ===
two_hand_gestures = [
    {
        "name": "Hai tay mở",
        "pattern": [
            [0, 1, 1, 1, 1],  # tay trái
            [0, 1, 1, 1, 1]   # tay phải
        ]
    },
    {
        "name": "Hai tay chữ L",
        "pattern": [
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0]
        ]
    }
]

