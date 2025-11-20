# services/translate_api/app.py
from flask import Blueprint, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from .process_image1 import detect_gesture  # thêm dấu . để import đúng trong package

translate_bp = Blueprint("translate", __name__)
CORS(translate_bp)

@translate_bp.route("/")
def home():
    return jsonify({"message": "Translate API đang chạy."})

@translate_bp.route("/detect_image", methods=["POST", "OPTIONS"])
def detect_image():
    print("📥 Nhận yêu cầu /detect_image")
    image = None

    if 'image' in request.files:
        file = request.files['image']
        in_memory_file = file.read()
        npimg = np.frombuffer(in_memory_file, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    elif request.is_json:
        data = request.get_json()
        if 'image' in data:
            base64_data = data['image']
            if ',' in base64_data:
                base64_data = base64_data.split(',', 1)[1]
            try:
                image_bytes = base64.b64decode(base64_data)
                npimg = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            except Exception as e:
                return jsonify({'error': f'Lỗi khi decode base64: {str(e)}'}), 400
        else:
            return jsonify({'error': 'Không có ảnh trong JSON'}), 400
    else:
        return jsonify({'error': 'Định dạng không hợp lệ'}), 400

    if image is None:
        return jsonify({'error': 'Không thể đọc ảnh'}), 400

    result = detect_gesture(image)
    return jsonify({'result': result})

