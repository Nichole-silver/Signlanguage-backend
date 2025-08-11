# gesture_rules.py
# Mảng quy tắc rút gọn: SINGLE_HAND_RULES và DOUBLE_HAND_RULES
# Dễ mở rộng: mỗi rule là dict với key pattern(s) và label.

SINGLE_HAND_RULES = [
    {"pattern": [0, 1, 1, 0, 0], "label": "V"},
    {"pattern": [0, 1, 0, 0, 0], "label": "L"},
    {"pattern": [0, 1, 1, 1, 0], "label": "W"},
    {"pattern": [1, 1, 0, 0, 0], "label": "Y"},
    {"pattern": [0, 1, 1, 1, 1], "label": "B"},
    {"pattern": [0, 0, 0, 0, 0], "label": "Nắm tay"},
    {"pattern": [1, 1, 1, 1, 1], "label": "Số 5"}
]

DOUBLE_HAND_RULES = [
    {
        "left_pattern": [0, 1, 0, 0, 0],
        "right_pattern": [0, 1, 0, 0, 0],
        "label": "Bạn bè"
    },
    {
        "left_pattern": [0, 1, 1, 0, 0],
        "right_pattern": [0, 1, 1, 0, 0],
        "label": "Gia đình"
    }
]
