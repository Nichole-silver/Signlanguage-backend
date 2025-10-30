# --- 1. Chọn phiên bản Python mong muốn ---
FROM python:3.10-slim

# --- 2. Đặt thư mục làm việc ---
WORKDIR /app

# --- 3. Copy toàn bộ mã nguồn vào container ---
COPY . /app

# --- 4. Cài đặt dependencies ---
RUN pip install --no-cache-dir -r requirements.txt

# --- 5. Render yêu cầu app lắng nghe biến môi trường PORT ---
EXPOSE 10000

# --- 6. Chạy ứng dụng Flask ---
# Flask sẽ tự đọc biến môi trường PORT mà Render cung cấp
CMD ["sh", "-c", "python main.py --port=$PORT"]
