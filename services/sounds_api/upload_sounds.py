import os
import base64
from pymongo import MongoClient

BASE_SOUND_DIR = r"C:\Users\Precision\SignLanguage-website\Signlanguage-frontend\sounds"

client = MongoClient("mongodb://localhost:27017/")
db = client["SignLanguageDB"]
collection = db["sounds"]

# Xóa dữ liệu cũ
collection.delete_many({})

count = 0
for filename in os.listdir(BASE_SOUND_DIR):
    if filename.endswith(".mp3"):
        filepath = os.path.join(BASE_SOUND_DIR, filename)
        with open(filepath, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        
        document = {
            "filename": filename,
            "data": encoded
        }
        collection.insert_one(document)
        print(f"✅ Upload: {filename}")
        count += 1

print(f"🎉 Hoàn tất upload {count} file âm thanh!")
