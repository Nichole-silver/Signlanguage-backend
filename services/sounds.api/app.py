from flask import Blueprint, jsonify, send_file, Response, request
from flask_cors import CORS
from pymongo import MongoClient
import base64
import io

sound_bp = Blueprint("sound", __name__)
CORS(sound_bp)

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "SignLanguageDB"
COLLECTION_NAME = "sounds"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@sound_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "db": DB_NAME, "collection": COLLECTION_NAME}), 200

@sound_bp.route("/sound/<filename>", methods=["GET"])
def get_sound(filename):
    doc = collection.find_one({"filename": filename})
    if not doc:
        return jsonify({"error": "File not found"}), 404
    
    audio_data = base64.b64decode(doc["data"])
    return Response(audio_data, mimetype="audio/mpeg")
