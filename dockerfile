# 1. Base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements và cài dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy toàn bộ source code
COPY . .

# 5. Expose port (Render sẽ map cổng $PORT vào container)
EXPOSE 8000

# 6. Start command
# Lấy $PORT từ Render (nếu không có thì default là 8000)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
