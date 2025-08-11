# gesture_rules.py
# Chứa các quy tắc nhận diện ký hiệu tay

# Quy tắc cho một tay (mặc định là tay phải, ảnh đã un-mirror)
one_hand_rules = [
    {
        "name": "B",
        "fingers": [0, 1, 1, 1, 1],
        "conditions": []
    },
    {
        "name": "L",
        "fingers": [1, 1, 0, 0, 0],
        "conditions": []
    },
    {
        "name": "I Love You",
        "fingers": [1, 1, 0, 0, 1],
        "conditions": [
            {"type": "thumb_index_dist", "op": "<", "value": 0.05}
        ]
    },
    {
        "name": "Fist",
        "fingers": [0, 0, 0, 0, 0],
        "conditions": []
    }
]

# Quy tắc cho hai tay
two_hand_rules = [
    {
        "name": "Double L",
        "fingers": [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0]],
        "conditions": []
    },
    {
        "name": "Two Hands Up",
        "fingers": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
        "conditions": []
    }
]
