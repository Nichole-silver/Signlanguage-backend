# services/image_api/app.py
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

image_bp = Blueprint("image", __name__)
CORS(image_bp)

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "SignLanguageDB"
COLLECTION_NAME = "lessons_full"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@image_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "db": DB_NAME, "collection": COLLECTION_NAME}), 200

@image_bp.route("/lessons", methods=["GET"])
def get_lessons():
    group = request.args.get("group")
    query = {"category": group} if group else {}
    lessons = list(collection.find(query, {"_id": 0}))
    print(f"📦 Truy vấn nhóm: {group or 'Tất cả'} — {len(lessons)} kết quả")
    return jsonify(lessons), 200

@image_bp.route("/lesson/<lesson_id>", methods=["GET"])
def get_lesson_detail(lesson_id):
    lesson = collection.find_one({"id": lesson_id}, {"_id": 0})
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    return jsonify(lesson), 200
