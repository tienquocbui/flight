# 🚀 Hướng dẫn chạy nhanh Air Traffic Control System

## ✅ Trạng thái hiện tại
- ✅ Backend FastAPI: **Đang chạy** tại http://localhost:8000
- ✅ Dữ liệu JSON: **Đã load** 24 waypoints và 13 flights
- ✅ Frontend React: **Đang khởi động** tại http://localhost:3000

## 🎯 Kiểm tra hệ thống

### 1. Backend API (http://localhost:8000)
```bash
# Kiểm tra API root
curl http://localhost:8000/

# Xem danh sách waypoints và routes
curl http://localhost:8000/airspace

# Xem danh sách flights
curl http://localhost:8000/flights

# Kiểm tra conflicts
curl http://localhost:8000/conflicts
```

### 2. Frontend Web (http://localhost:3000)
- Mở trình duyệt và truy cập: http://localhost:3000
- Giao diện sẽ hiển thị:
  - Danh sách waypoints (24 waypoints)
  - Danh sách routes
  - Danh sách flights (13 flights)
  - Form thêm flight mới
  - Danh sách conflicts (nếu có)

## 🔧 Tính năng chính

### ✅ Đã hoạt động:
1. **Load dữ liệu thực tế** từ JSON files
2. **Quản lý waypoints** với tọa độ thực
3. **Quản lý flights** với timeline
4. **Phát hiện xung đột** (4 loại: crossing, head-on, overtake, lateral)
5. **Đề xuất đường bay** với thuật toán A*
6. **Giao diện web** Material-UI

### 📊 Dữ liệu đã load:
- **24 waypoints** từ `data/airspace_data-2.json`
- **13 flights** từ `data/flight_plans-2.json`
- **Routes** được tính toán tự động

## 🚨 Nếu gặp lỗi

### Backend không chạy:
```bash
cd src
PYTHONPATH=. uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Frontend không chạy:
```bash
cd frontend
npm install
npm start
```

### Lỗi import Python:
```bash
export PYTHONPATH=src
```

## 🎮 Thử nghiệm

1. **Thêm flight mới**:
   - Vào form "Add Flight"
   - Nhập callsign, route, speed, flight level
   - Submit để thêm flight

2. **Xem conflicts**:
   - Refresh trang để xem conflicts mới
   - Click "Suggest Path" để tìm đường thay thế

3. **Kiểm tra API**:
   - Truy cập http://localhost:8000/docs để xem Swagger UI
   - Test các endpoint trực tiếp

## 📁 Cấu trúc dự án
```
a*/
├── src/                    # Backend Python
│   ├── api.py             # FastAPI server
│   ├── models/            # Data models
│   └── algorithms/        # Core algorithms
├── frontend/              # React frontend
├── data/                  # JSON data files
├── requirements.txt       # Python dependencies
└── README.md             # Hướng dẫn chi tiết
```

## 🎉 Hệ thống đã sẵn sàng!
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs 