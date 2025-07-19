# 🛩️ Air Traffic Control System

Hệ thống mô phỏng và quản lý không lưu với phát hiện xung đột và đề xuất đường bay thay thế.

## ✨ Tính năng chính

### 🎯 **Phát hiện xung đột thông minh**
- **Crossing Conflicts**: Xung đột giao nhau tại waypoints
- **Head-on Conflicts**: Xung đột đối đầu trên cùng route
- **Overtake Conflicts**: Xung đột vượt trên cùng route
- **Lateral Conflicts**: Xung đột bên với khoảng cách gần

### 🗺️ **Đề xuất đường bay thay thế**
- Thuật toán A* cải tiến với tránh xung đột
- Tính toán góc rẽ và ràng buộc hàng không
- Đa chiến lược tìm đường (conflict-free, minimal conflict)
- Thông tin chi tiết: khoảng cách, số waypoints

### 📊 **Real Database Integration**
- **29 waypoints** thực tế của Việt Nam
- **13 flight plans** với dữ liệu thực
- **48 routes** kết nối các waypoints
- Phát hiện **7 conflicts** từ dữ liệu thực

### 🎨 **UI/UX hiện đại**
- Dashboard với thống kê real-time
- Material-UI với icons và colors
- Responsive design
- Loading states và error handling

## 🚀 Cài đặt và chạy

### **Backend (FastAPI)**
```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy backend
cd src
PYTHONPATH=. uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend (React)**
```bash
# Cài đặt dependencies
cd frontend
npm install

# Chạy frontend
npm start
```

### **Scripts tự động**
```bash
# Chạy backend
./run_backend.sh

# Chạy frontend  
./run_frontend.sh
```

## 📁 Cấu trúc project

```
├── src/                    # Backend Python
│   ├── api.py             # FastAPI server
│   ├── models/            # Data models
│   │   ├── airspace.py    # Airspace management
│   │   ├── flight.py      # Flight objects
│   │   └── waypoint.py    # Waypoint objects
│   └── algorithms/        # Core algorithms
│       ├── conflict_detection.py  # Conflict detection
│       └── pathfinding.py         # A* pathfinding
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.tsx        # Main component
│   │   └── api.ts         # API client
│   └── package.json
├── data/                  # Real database
│   ├── airspace_data.json # 29 waypoints + 48 routes
│   └── flight_plans.json  # 13 flight plans
└── docs/                  # Documentation
```

## 🔧 API Endpoints

### **Core APIs**
- `GET /airspace` - Lấy thông tin airspace
- `GET /flights` - Lấy danh sách flights
- `GET /conflicts` - Phát hiện xung đột
- `POST /flights` - Thêm flight mới

### **Advanced APIs**
- `POST /suggest_path` - Đề xuất đường bay thay thế
- `GET /stats` - Thống kê hệ thống
- `POST /load_test_data` - Load dữ liệu test

### **Example: Suggest Path**
```bash
curl -X POST http://localhost:8000/suggest_path \
  -H "Content-Type: application/json" \
  -d '{
    "callsign": "VJC172",
    "start": "SADAS", 
    "goal": "MEVON"
  }'
```

**Response:**
```json
{
  "new_path": ["SADAS", "MUMGA", "BANSU", "VVPK", "MEVON"],
  "total_distance_nm": 121.06,
  "waypoints_count": 5,
  "original_start": "SADAS",
  "original_goal": "MEVON"
}
```

## 🧪 Test Cases

### **Real Database Conflicts**
- **VJC172 vs BAV254**: Lateral conflicts tại VVPK, MEVON
- **Multiple flights**: 7 conflicts tổng cộng
- **Flight levels**: FL390, FL400 với separation < 1000ft

### **Path Finding Tests**
- **SADAS → MEVON**: Alternative route qua MUMGA, BANSU, VVPK
- **Conflict avoidance**: Tự động tránh segments có conflicts
- **Turn angle constraints**: Giới hạn góc rẽ < 90°

## 🎯 Kết quả hiện tại

### **Real Database Stats**
- ✅ **29 waypoints** loaded successfully
- ✅ **13 flights** with real flight plans
- ✅ **48 routes** connecting waypoints
- ✅ **7 conflicts** detected automatically
- ✅ **Enhanced A*** pathfinding working

### **System Performance**
- ⚡ **Fast conflict detection**: < 100ms
- 🗺️ **Smart pathfinding**: Multiple strategies
- 📊 **Real-time stats**: Live dashboard
- 🎨 **Modern UI**: Material-UI components

## 🔍 Technical Details

### **Conflict Detection Algorithm**
```python
# Enhanced thresholds for real data
FLIGHT_LEVEL_SEPARATION = 2000  # ft (increased from 1000)
TIME_WINDOW = 15  # minutes (increased from 10)
LATERAL_TIME_WINDOW = 5  # minutes (increased from 1)
```

### **A* Pathfinding Features**
- **Conflict avoidance**: Skip unsafe route segments
- **Turn angle constraints**: Maximum 90° turns
- **Multiple strategies**: Conflict-free → Minimal conflict
- **Distance calculation**: Haversine formula for accuracy

### **Real Data Integration**
- **Waypoints**: 29 real Vietnamese waypoints
- **Routes**: 48 actual airway connections
- **Flights**: 13 real flight plans with actual routes
- **Timing**: Real entry times and speed data

## 🚨 Troubleshooting

### **Backend Issues**
```bash
# Check if backend is running
curl http://localhost:8000/stats

# Restart backend
pkill -f uvicorn
cd src && PYTHONPATH=. uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend Issues**
```bash
# Reinstall dependencies
cd frontend && rm -rf node_modules && npm install

# Check for port conflicts
lsof -ti:3000 | xargs kill -9
```

### **Data Loading Issues**
```bash
# Test data loading
cd src && PYTHONPATH=. python debug_load.py
```

## 📈 Roadmap

### **Phase 1** ✅ (Completed)
- [x] Real database integration
- [x] Enhanced conflict detection
- [x] Improved A* pathfinding
- [x] Modern UI/UX
- [x] API documentation

### **Phase 2** 🚧 (In Progress)
- [ ] Real-time flight tracking
- [ ] 3D visualization
- [ ] Weather integration
- [ ] Advanced conflict resolution

### **Phase 3** 📋 (Planned)
- [ ] Machine learning predictions
- [ ] Multi-airspace support
- [ ] Mobile app
- [ ] Performance optimization

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 **Hệ thống sẵn sàng sử dụng!**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **GitHub**: https://github.com/tienquocbui/flight

**Truy cập ngay để test hệ thống với dữ liệu thực!** 🚀
