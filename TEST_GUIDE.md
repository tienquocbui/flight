# 🧪 Hướng dẫn Test Air Traffic Control System

## ✅ Trạng thái hệ thống
- **Backend**: ✅ Đang chạy tại http://localhost:8000
- **Frontend**: ✅ Đang chạy tại http://localhost:3000
- **Test Data**: ✅ Đã load với 26 conflicts

## 🎯 Các trường hợp test xung đột

### 1. **Crossing Conflicts (Xung đột giao nhau)**
- **TEST001** (FL330) và **TEST002** (FL340) giao nhau tại waypoint B
- **TEST002** (FL340) và **TEST003** (FL350) giao nhau tại waypoint B
- **TEST003** (FL350) và **TEST004** (FL360) giao nhau tại waypoints A, B
- **TEST004** (FL360) và **TEST005** (FL370) giao nhau tại waypoints A, B
- **TEST005** (FL370) và **TEST006** (FL380) giao nhau tại waypoints A, B, C

### 2. **Head-on Conflicts (Xung đột đối đầu)**
- **TEST003** (FL350) và **TEST004** (FL360) bay ngược chiều trên route A→B vs B→A

### 3. **Overtake Conflicts (Xung đột vượt)**
- **TEST005** (FL370, chậm) và **TEST006** (FL380, nhanh) cùng route A→B→C

### 4. **Lateral Conflicts (Xung đột bên)**
- Nhiều cặp flights ở gần nhau cùng thời điểm với mực bay gần nhau

## 🚀 Cách test

### **Bước 1: Truy cập Frontend**
```
http://localhost:3000
```

### **Bước 2: Xem Dashboard**
- Kiểm tra stats: 6 waypoints, 8 flights, 26 conflicts
- Xem breakdown theo loại conflict

### **Bước 3: Test Load Test Data**
1. Click nút **"Load Test Data"**
2. Xem conflicts xuất hiện trong panel bên phải
3. Kiểm tra các loại conflict khác nhau

### **Bước 4: Test Suggest Path**
1. Chọn một conflict bất kỳ
2. Click **"Suggest Path"**
3. Xem dialog hiển thị đường bay thay thế

### **Bước 5: Test Add Flight**
1. Điền form "Add Flight":
   - Callsign: TEST999
   - Route: A,B,C
   - Speed: 450
   - Flight Level: 350
   - Entry Time: 2025-01-19T08:30:00
2. Click **"Add Flight"**
3. Xem flight mới xuất hiện và conflicts mới (nếu có)

### **Bước 6: Test API trực tiếp**

#### Kiểm tra stats:
```bash
curl http://localhost:8000/stats
```

#### Load test data:
```bash
curl -X POST http://localhost:8000/load_test_data
```

#### Xem conflicts:
```bash
curl http://localhost:8000/conflicts
```

#### Thêm flight mới:
```bash
curl -X POST http://localhost:8000/flights \
  -H "Content-Type: application/json" \
  -d '{
    "callsign": "TEST999",
    "route": ["A", "B", "C"],
    "speed": 450,
    "flight_level": 350,
    "entry_time": "2025-01-19T08:30:00"
  }'
```

## 🎨 Tính năng UI mới

### **Dashboard Stats**
- Cards hiển thị số liệu thống kê
- Màu sắc thay đổi theo trạng thái (xanh = an toàn, đỏ = có conflict)

### **Improved Flight Display**
- Icons cho từng loại thông tin
- Chips hiển thị FL và Speed
- Layout đẹp hơn với borders và spacing

### **Enhanced Conflict Display**
- Icons emoji cho từng loại conflict
- Color-coded chips (đỏ = nguy hiểm, vàng = cảnh báo, xanh = thông tin)
- Thông tin chi tiết hơn

### **Better Forms**
- Form fields nhỏ gọn hơn
- Validation tốt hơn
- Loading states

### **Action Buttons**
- Refresh Data: Cập nhật dữ liệu
- Load Test Data: Load dữ liệu test với conflicts

## 🔍 Kiểm tra chi tiết

### **Crossing Conflict Test**
- Xem conflict TEST001 vs TEST002 tại waypoint B
- Kiểm tra thời gian overlap và flight level difference

### **Head-on Conflict Test**
- Xem conflict TEST003 vs TEST004 trên route A↔B
- Kiểm tra hướng bay ngược chiều

### **Overtake Conflict Test**
- Xem conflict TEST005 vs TEST006 cùng route A→B→C
- Kiểm tra tốc độ khác nhau (400 vs 500 KTS)

### **Lateral Conflict Test**
- Xem các conflicts lateral với thời gian gần nhau
- Kiểm tra khoảng cách thời gian < 5 phút

## 🎯 Kết quả mong đợi

### **Sau khi load test data:**
- 6 waypoints (A, B, C, D, E, F)
- 8 flights (TEST001-TEST008)
- 26 conflicts tổng cộng
- Breakdown: crossing, head-on, overtake, lateral

### **Sau khi thêm flight mới:**
- Conflicts có thể tăng lên
- Flight mới xuất hiện trong danh sách
- Timeline được tính toán tự động

## 🚨 Troubleshooting

### **Nếu frontend không load:**
```bash
cd frontend
npm start
```

### **Nếu backend không chạy:**
```bash
cd src
PYTHONPATH=. uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### **Nếu không có conflicts:**
1. Click "Load Test Data"
2. Refresh page
3. Kiểm tra console errors

## 🎉 Hệ thống sẵn sàng test!
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs 