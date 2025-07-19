# 🐳 Docker Setup - Air Traffic Control System

## 🚀 **Chạy toàn bộ hệ thống với Docker**

### **Bước 1: Build và chạy**
```bash
# Build và chạy cả backend và frontend
docker-compose up --build

# Hoặc chạy ở background
docker-compose up -d --build
```

### **Bước 2: Truy cập ứng dụng**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### **Bước 3: Dừng hệ thống**
```bash
# Dừng và xóa containers
docker-compose down

# Dừng và xóa cả images
docker-compose down --rmi all
```

## 🔧 **Các lệnh hữu ích**

### **Xem logs**
```bash
# Xem logs của tất cả services
docker-compose logs

# Xem logs của backend
docker-compose logs backend

# Xem logs của frontend
docker-compose logs frontend

# Xem logs real-time
docker-compose logs -f
```

### **Restart services**
```bash
# Restart backend
docker-compose restart backend

# Restart frontend
docker-compose restart frontend

# Restart tất cả
docker-compose restart
```

### **Vào container để debug**
```bash
# Vào backend container
docker-compose exec backend bash

# Vào frontend container
docker-compose exec frontend sh
```

## 📁 **Cấu trúc Docker**

### **Backend Container:**
- **Image**: Python 3.9.7
- **Port**: 8000
- **Volumes**: `./src` và `./data`
- **Environment**: `PYTHONPATH=/app/src`

### **Frontend Container:**
- **Image**: Node.js 18
- **Port**: 3000
- **Volumes**: `./frontend`
- **Environment**: `REACT_APP_API_URL=http://localhost:8000`

## 🎯 **Tính năng**

✅ **Hot Reload**: Code changes sẽ tự động reload
✅ **Volume Mounting**: Code changes được sync real-time
✅ **Network Isolation**: Backend và frontend có thể giao tiếp
✅ **Environment Variables**: Cấu hình tự động
✅ **Easy Setup**: Chỉ cần 1 lệnh để chạy toàn bộ

## 🔍 **Troubleshooting**

### **Port đã được sử dụng**
```bash
# Kiểm tra ports đang sử dụng
lsof -i :3000
lsof -i :8000

# Kill process nếu cần
kill -9 <PID>
```

### **Build errors**
```bash
# Clean build
docker-compose down --rmi all
docker-compose up --build
```

### **Permission issues**
```bash
# Fix permissions
sudo chown -R $USER:$USER .
```

## 🎉 **Kết quả**

Sau khi chạy `docker-compose up --build`:
- Backend sẽ chạy tại http://localhost:8000
- Frontend sẽ chạy tại http://localhost:3000
- API docs có sẵn tại http://localhost:8000/docs
- Có thể test conflict detection và pathfinding 