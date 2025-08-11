# gesture_rules.py

# Quy tắc nhận diện 1 tay (tay phải)
SINGLE_HAND_RULES = [
    {"label": "B", "pattern": [0, 1, 1, 1, 1]},       # Ngón cái co, 4 ngón còn lại duỗi
    {"label": "L", "pattern": [0, 1, 0, 0, 0]},       # Ngón trỏ duỗi
    {"label": "V", "pattern": [0, 1, 1, 0, 0]},       # Trỏ + giữa duỗi
    {"label": "Y", "pattern": [1, 1, 0, 0, 1]},       # Ngón cái + trỏ + út duỗi
    {"label": "Nắm tay", "pattern": [0, 0, 0, 0, 0]}  # Tất cả co
]

# Quy tắc nhận diện 2 tay (ít dùng hơn, không ưu tiên tìm kiếm)
DOUBLE_HAND_RULES = [
    {
        "label": "Song V",
        "patterns": [
            [0, 1, 1, 0, 0],  # Tay phải: V
            [0, 1, 1, 0, 0]   # Tay trái: V
        ]
    },
    {
        "label": "Song B",
        "patterns": [
            [0, 1, 1, 1, 1],  # Tay phải: B
            [0, 1, 1, 1, 1]   # Tay trái: B
        ]
    }
]
