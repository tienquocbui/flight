# Air Traffic Control Simulation System

Hệ thống mô phỏng kiểm soát không lưu với khả năng phát hiện xung đột và đề xuất đường bay thay thế.

## Tính năng chính

- **Quản lý không gian bay**: Load dữ liệu waypoints và routes từ JSON
- **Quản lý chuyến bay**: Thêm, xem danh sách chuyến bay với timeline
- **Phát hiện xung đột**: Tự động phát hiện 4 loại xung đột:
  - Xung đột chéo đường (Crossing)
  - Xung đột đối đầu (Head-on)
  - Xung đột vượt (Overtake)
  - Xung đột bên (Lateral)
- **Đề xuất đường bay**: Sử dụng thuật toán A* để tìm đường bay thay thế an toàn
- **Giao diện web**: React + Material-UI với API FastAPI

## Cấu trúc dự án

```
a*/
├── src/                    # Backend Python
│   ├── models/            # Data models
│   │   ├── waypoint.py    # Waypoint class
│   │   ├── flight.py      # Flight class
│   │   └── airspace.py    # Airspace graph
│   ├── algorithms/        # Core algorithms
│   │   ├── conflict_detection.py  # Conflict detection
│   │   └── pathfinding.py         # A* pathfinding
│   └── api.py             # FastAPI backend
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.tsx        # Main React component
│   │   └── api.ts         # API client
│   └── package.json
├── data/                  # JSON data files
│   ├── airspace_data-2.json    # Waypoints and routes
│   └── flight_plans-2.json     # Flight plans
├── requirements.txt       # Python dependencies
├── run_backend.sh         # Backend startup script
├── run_frontend.sh        # Frontend startup script
└── README.md
```

## Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.8+
- Node.js 16+
- npm hoặc yarn

### Bước 1: Cài đặt dependencies

```bash
# Cài đặt Python dependencies
pip install -r requirements.txt

# Cài đặt Node.js dependencies
cd frontend
npm install
cd ..
```

### Bước 2: Chạy Backend

```bash
# Cách 1: Sử dụng script
./run_backend.sh

# Cách 2: Chạy thủ công
export PYTHONPATH=src
cd src
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Backend sẽ chạy tại: http://localhost:8000

### Bước 3: Chạy Frontend

```bash
# Cách 1: Sử dụng script
./run_frontend.sh

# Cách 2: Chạy thủ công
cd frontend
npm start
```

Frontend sẽ chạy tại: http://localhost:3000

## API Endpoints

### GET /airspace
Lấy thông tin không gian bay (waypoints và routes)

### GET /flights
Lấy danh sách tất cả chuyến bay

### POST /flights
Thêm chuyến bay mới
```json
{
  "callsign": "VJC123",
  "route": ["A", "B", "C"],
  "speed": 450,
  "flight_level": 330,
  "entry_time": "2025-01-19T08:00:00"
}
```

### GET /conflicts
Phát hiện và trả về tất cả xung đột

### POST /suggest_path
Đề xuất đường bay thay thế
```json
{
  "callsign": "VJC123",
  "start": "A",
  "goal": "C"
}
```

## Dữ liệu mẫu

Hệ thống đã được load sẵn với:
- **23 waypoints** từ file `data/airspace_data-2.json`
- **13 chuyến bay** từ file `data/flight_plans-2.json`

Dữ liệu bao gồm:
- Các waypoint thực tế trong khu vực FIR Việt Nam
- Các chuyến bay với thông tin chi tiết: callsign, route, speed, flight level, entry time

## Tính năng nâng cao

### Phát hiện xung đột
- **Crossing**: Xung đột khi 2 chuyến bay cắt nhau tại cùng waypoint
- **Head-on**: Xung đột đối đầu trên cùng route
- **Overtake**: Xung đột vượt trên cùng route
- **Lateral**: Xung đột bên khi 2 chuyến bay ở gần nhau

### Thuật toán A*
- Tìm đường bay thay thế tối ưu
- Tránh xung đột với các chuyến bay khác
- Tuân thủ ràng buộc không gian bay

## Troubleshooting

### Lỗi import Python
```bash
# Đảm bảo PYTHONPATH được set đúng
export PYTHONPATH=src
```

### Lỗi CORS
Backend đã được cấu hình CORS để cho phép frontend kết nối.

### Lỗi port đã được sử dụng
```bash
# Thay đổi port backend
uvicorn api:app --reload --port 8001

# Thay đổi port frontend
PORT=3001 npm start
```

## Đóng góp

Để thêm tính năng mới hoặc sửa lỗi:
1. Fork repository
2. Tạo branch mới
3. Commit changes
4. Tạo Pull Request

## License

MIT License
