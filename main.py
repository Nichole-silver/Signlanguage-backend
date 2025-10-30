# main.py
from flask import Flask, jsonify
from flask_cors import CORS

# Import các blueprint từ API con
from services.image_api.app import image_bp
from services.translate_api.app import translate_bp
from services.sounds_api.app import sound_bp  # thêm dòng này

app = Flask(__name__)
CORS(app)

# Đăng ký API con
app.register_blueprint(image_bp, url_prefix="/api/image")
app.register_blueprint(translate_bp, url_prefix="/api/translate")
app.register_blueprint(sound_bp, url_prefix="/api/sound")  # thêm dòng này

@app.route("/")
def home():
    return jsonify({
        "message": "SignLanguage Backend đang hoạt động.",
        "services": {
            "image_api": "/api/image",
            "translate_api": "/api/translate",
            "sound_api": "/api/sound"
        }
    })

if __name__ == "__main__":
    print("🚀 Server đang chạy tại http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
