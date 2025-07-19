# 🐳 Docker Setup - Air Traffic Control System

## 🚀 **Quick Start (Chỉ cần Docker Desktop)**

### **Bước 1: Cài đặt Docker Desktop**
1. Tải Docker Desktop từ: https://www.docker.com/products/docker-desktop/
2. Cài đặt và restart máy
3. Mở Docker Desktop và đợi nó khởi động

### **Bước 2: Clone và chạy project**
```bash
# Clone project
git clone https://github.com/tienquocbui/flight.git
cd flight

# Chạy development environment (KHÔNG cần cài Python/Node.js)
docker-compose -f docker-compose.dev.yml up --build
```

### **Bước 3: Truy cập ứng dụng**
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 🛠️ **Development Environment**

### **Chạy với tất cả tools đã cài sẵn:**
```bash
# Development environment với Python, Node.js, Git, vim, nano, htop
docker-compose -f docker-compose.dev.yml up dev

# Vào container để code
docker-compose -f docker-compose.dev.yml exec dev bash
```

### **Trong container, bạn có thể:**
```bash
# Chạy backend
python server.py

# Chạy frontend
cd frontend && npm start

# Chạy tests
python -m pytest

# Edit files với vim/nano
vim src/api.py
nano frontend/src/App.tsx

# Monitor system với htop
htop
```

## 🏭 **Production Environment**

### **Chạy production build:**
```bash
# Production backend + frontend
docker-compose up --build

# Hoặc chạy riêng
docker-compose up backend
docker-compose up frontend
```

## 🔧 **Troubleshooting**

### **Port Conflicts**
Nếu port 8000 hoặc 3000 bị chiếm:
```bash
# Thay đổi port trong docker-compose.dev.yml
ports:
  - "8001:8000"  # Dùng port 8001 trên host
```

### **Build Issues**
```bash
# Clean up và rebuild
docker-compose down
docker system prune -f
docker-compose -f docker-compose.dev.yml up --build --force-recreate
```

### **Volume Issues**
```bash
# Restart containers
docker-compose restart

# Rebuild specific service
docker-compose up --build dev
```

## 📋 **Available Commands**

### **Development Container:**
- `python server.py` - Start backend
- `cd frontend && npm start` - Start frontend  
- `python -m pytest` - Run tests
- `vim/nano` - Edit files
- `htop` - Monitor system
- `git` - Version control
- `curl` - Test APIs

### **Docker Commands:**
```bash
# View logs
docker-compose logs dev

# Execute commands
docker-compose exec dev python -c "print('Hello!')"

# Stop all
docker-compose down

# Remove all containers/images
docker system prune -a
```

## 🎯 **Benefits**

✅ **Không cần cài Python, Node.js, Git**  
✅ **Tất cả tools đã có sẵn trong container**  
✅ **Environment consistent trên mọi máy**  
✅ **Easy setup cho Windows/Linux/Mac**  
✅ **Isolated development environment**  
✅ **Easy cleanup và reset**

## 🔍 **Cấu trúc Docker**

### **Development Container:**
- **Image**: Python 3.9.7 + Node.js 18
- **Tools**: Git, vim, nano, htop, curl
- **Ports**: 8000, 3000, 22
- **Volumes**: Toàn bộ project directory

### **Production Backend:**
- **Image**: Python 3.9.7
- **Port**: 8000
- **Volumes**: `./src` và `./data`

### **Production Frontend:**
- **Image**: Node.js 18
- **Port**: 3000
- **Volumes**: `./frontend`

## 🎉 **Kết quả**

Sau khi chạy `docker-compose -f docker-compose.dev.yml up --build`:
- Development environment với tất cả tools
- Backend API tại http://localhost:8000
- Frontend tại http://localhost:3000
- API docs tại http://localhost:8000/docs
- Có thể test conflict detection và pathfinding 