SINGLE_HAND_RULES = [
    {"label": "B", "pattern": [0, 1, 1, 1, 1], "strict": True},       # 4 ngón duỗi, ngón cái gập
    {"label": "L", "pattern": [0, 1, 0, 0, 0], "strict": True},       # L
    {"label": "V", "pattern": [0, 1, 1, 0, 0]},                       # V
    {"label": "Nắm tay", "pattern": [0, 0, 0, 0, 0], "strict": True}, # Fist
]

DOUBLE_HAND_RULES = [
    {"label": "Hai tay mở", "patterns": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]}
]
