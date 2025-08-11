# =========================
# Quy tắc nhận diện cho 1 tay
# =========================
SINGLE_HAND_RULES = [
    {"pattern": [0, 1, 1, 0, 0], "label": "V"},  # Ngón trỏ + giữa
    {"pattern": [0, 1, 0, 0, 0], "label": "L"},  # Ngón trỏ
    {"pattern": [0, 1, 1, 1, 0], "label": "W"},  # Trỏ + giữa + áp út
    {"pattern": [1, 1, 0, 0, 0], "label": "Y"},  # Cái + trỏ
    {"pattern": [0, 1, 1, 1, 1], "label": "B"},  # 4 ngón duỗi
    {"pattern": [0, 0, 0, 0, 0], "label": "Nắm tay"},  # Tất cả gập
    {"pattern": [1, 1, 1, 1, 1], "label": "Số 5"}  # Tất cả duỗi
]

# =========================
# Quy tắc nhận diện cho 2 tay
# =========================
DOUBLE_HAND_RULES = [
    {
        "left_pattern": [0, 1, 0, 0, 0],   # Tay trái L
        "right_pattern": [0, 1, 0, 0, 0],  # Tay phải L
        "label": "Bạn bè"  # Hai ngón trỏ móc vào nhau
    },
    {
        "left_pattern": [0, 1, 1, 0, 0],   # Tay trái V
        "right_pattern": [0, 1, 1, 0, 0],  # Tay phải V
        "label": "Gia đình"
    },
    {
        "left_pattern": [0, 0, 0, 0, 0],   # Nắm tay
        "right_pattern": [0, 0, 0, 0, 0],
        "label": "Chúc mừng"
    }
]
