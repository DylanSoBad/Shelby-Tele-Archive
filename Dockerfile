# Sử dụng base image Python tinh gọn
FROM python:3.10-slim

# Cài đặt Node.js (chuẩn bị môi trường cho SDK của mảng Web3)
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file định nghĩa thư viện của cả Python & Node
COPY requirements.txt package.json ./

# Cài đặt thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt thư viện Node.js (chỉ lấy dependencies thật không lấy dev)
RUN npm install

# Copy phần còn lại của mã nguồn vào container
COPY . .

# Khởi chạy bot
CMD ["python", "main.py"]
