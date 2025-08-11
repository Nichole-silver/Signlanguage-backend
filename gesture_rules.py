# gesture_rules.py
# Quy tắc nhận diện ký hiệu tay, chia thành 2 nhóm: 1 tay và 2 tay

# Quy tắc 1 tay (tay phải, ảnh không mirror)
# fingers: [ngón cái, ngón trỏ, ngón giữa, ngón áp út, ngón út] (1 = duỗi, 0 = gập)
one_hand_rules = [
    {"pattern": [0, 1, 1, 0, 0], "name": "V"},
    {"pattern": [0, 1, 0, 0, 0], "name": "L"},
    {"pattern": [0, 1, 1, 1, 0], "name": "W"},
    {"pattern": [0, 0, 0, 0, 0], "name": "Nắm tay"},
    {"pattern": [0, 1, 1, 1, 1], "name": "B"},
    {"pattern": [1, 1, 0, 0, 1], "name": "I Love You", "thumb_index_dist_max": 0.05}
]

# Quy tắc 2 tay (ít gặp, không dò tìm như 1 tay)
two_hand_rules = [
    {"pattern_left": [0, 1, 1, 0, 0], "pattern_right": [0, 1, 1, 0, 0], "name": "Double V"},
    {"pattern_left": [0, 0, 0, 0, 0], "pattern_right": [0, 0, 0, 0, 0], "name": "Double fist"}
]
