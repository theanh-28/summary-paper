# Sử dụng Node.js bản nhẹ nhất
FROM node:20-alpine

# Set thư mục làm việc trong container
WORKDIR /app

# Copy file cấu hình package vào trước để cài đặt (tận dụng cache của Docker)
COPY package*.json ./

# Cài đặt thư viện
RUN npm install

# Copy toàn bộ code frontend vào container
COPY . .

# Mở cổng 5173 cho Vite
EXPOSE 5173

# Chạy server ở chế độ dev và expose ra ngoài mạng của Docker (--host)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
