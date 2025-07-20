# 🧪 Test Cases Guide - Air Traffic Control System

## 🚀 **Cách sử dụng Test Cases**

### **Bước 1: Xem danh sách test cases**
```bash
python add_test_flights.py list
```

### **Bước 2: Thêm test case cụ thể**
```bash
# Thêm test case crossing conflict
python add_test_flights.py CROSSING_CONFLICT_1

# Thêm test case head-on conflict
python add_test_flights.py HEAD_ON_CONFLICT_1

# Thêm test case overtake conflict
python add_test_flights.py OVERTAKE_CONFLICT_1
```

### **Bước 3: Thêm tất cả test cases**
```bash
python add_test_flights.py all
```

### **Bước 4: Restart backend để load flights mới**
```bash
docker-compose restart backend
```

### **Bước 5: Test trên frontend**
Mở browser: http://localhost:3003

## 📋 **Danh sách Test Cases**

### **1. CROSSING_CONFLICT_1**
- **Mô tả**: Hai máy bay cắt nhau tại VVPK cùng thời gian
- **Flights**: TEST001, TEST002
- **Xung đột**: CROSSING
- **Vị trí**: VVPK
- **Thời gian**: 02:05

### **2. HEAD_ON_CONFLICT_1**
- **Mô tả**: Hai máy bay bay ngược chiều trên cùng route
- **Flights**: TEST003, TEST004
- **Xung đột**: HEAD_ON
- **Vị trí**: VVPK
- **Thời gian**: 03:05

### **3. OVERTAKE_CONFLICT_1**
- **Mô tả**: Máy bay nhanh vượt máy bay chậm trên cùng route
- **Flights**: TEST005, TEST006
- **Xung đột**: OVERTAKE
- **Vị trí**: VVPK
- **Thời gian**: 04:10

### **4. LATERAL_CONFLICT_1**
- **Mô tả**: Hai máy bay bay song song gần nhau
- **Flights**: TEST007, TEST008
- **Xung đột**: LATERAL
- **Vị trí**: VVPK
- **Thời gian**: 05:05

### **5. MULTIPLE_CONFLICTS_1**
- **Mô tả**: Nhiều loại xung đột cùng lúc
- **Flights**: TEST009, TEST010, TEST011
- **Xung đột**: CROSSING, HEAD_ON
- **Vị trí**: VVPK
- **Thời gian**: 06:05

### **6. VERTICAL_SEPARATION_1**
- **Mô tả**: Hai máy bay cùng route nhưng khác flight level
- **Flights**: TEST012, TEST013
- **Xung đột**: Không có (FL310 vs FL330)
- **Ghi chú**: Không có xung đột vì khác flight level

### **7. TIME_SEPARATION_1**
- **Mô tả**: Hai máy bay cùng route nhưng khác thời gian
- **Flights**: TEST014, TEST015
- **Xung đột**: Không có (02:00 vs 02:30)
- **Ghi chú**: Không có xung đột vì khác thời gian

### **8. COMPLEX_ROUTE_CONFLICT_1**
- **Mô tả**: Xung đột trên route phức tạp
- **Flights**: TEST016, TEST017
- **Xung đột**: CROSSING
- **Vị trí**: MUMGA
- **Thời gian**: 09:10

## 🎯 **Cách Test trên Frontend**

### **1. Xem danh sách flights**
- Vào tab "Flights"
- Tìm các flights có tên TEST001-TEST017
- Kiểm tra route và thời gian

### **2. Kiểm tra conflicts**
- Vào tab "Conflicts"
- Xem danh sách conflicts được phát hiện
- So sánh với expected conflicts

### **3. Test conflict detection**
- Thêm/sửa flights để tạo conflicts mới
- Kiểm tra xem hệ thống có phát hiện đúng không

### **4. Test pathfinding**
- Vào tab "Pathfinding"
- Chọn flight có conflict
- Xem suggested path để tránh conflict

## 🔧 **Troubleshooting**

### **Lỗi: File không tìm thấy**
```bash
# Kiểm tra vị trí hiện tại
pwd
ls -la

# Đảm bảo đang ở thư mục gốc của project
cd /path/to/flight/project
```

### **Lỗi: Backend không load flights mới**
```bash
# Restart backend
docker-compose restart backend

# Kiểm tra logs
docker-compose logs backend
```

### **Lỗi: Frontend không hiển thị**
```bash
# Restart frontend
docker-compose restart frontend

# Kiểm tra logs
docker-compose logs frontend
```

## 📊 **Expected Results**

### **Với CROSSING_CONFLICT_1:**
- 2 flights: TEST001, TEST002
- 1 conflict: CROSSING tại VVPK
- Thời gian: 02:05

### **Với HEAD_ON_CONFLICT_1:**
- 2 flights: TEST003, TEST004
- 1 conflict: HEAD_ON tại VVPK
- Thời gian: 03:05

### **Với MULTIPLE_CONFLICTS_1:**
- 3 flights: TEST009, TEST010, TEST011
- 2+ conflicts: CROSSING, HEAD_ON tại VVPK
- Thời gian: 06:05

## 🎉 **Tips**

1. **Test từng case một** để dễ debug
2. **Kiểm tra logs** nếu có lỗi
3. **So sánh expected vs actual** conflicts
4. **Test pathfinding** cho các conflicts phức tạp
5. **Thêm flights mới** để test edge cases

## 🚀 **Quick Test Commands**

```bash
# Thêm test case đơn giản
python add_test_flights.py CROSSING_CONFLICT_1
docker-compose restart backend

# Thêm tất cả test cases
python add_test_flights.py all
docker-compose restart backend

# Xem danh sách test cases
python add_test_flights.py list
```

**Chúc bạn test thành công!** 🎯 