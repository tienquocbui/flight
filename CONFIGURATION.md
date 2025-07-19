# ⚙️ Configuration Guide

## 🔧 **Frontend Configuration**

### **Local Development:**
```bash
# Frontend sẽ tự động sử dụng localhost:8000
cd frontend
npm start
```

### **Production Deployment:**
1. **Tạo file `.env` trong thư mục `frontend/`:**
```bash
REACT_APP_API_URL=https://flight-mupy.onrender.com
```

2. **Hoặc set environment variable trong GitHub:**
   - Go to repository settings → Secrets and variables → Actions
   - Add repository variable: `REACT_APP_API_URL`
   - Value: `https://flight-mupy.onrender.com`

## 🎨 **Backend Configuration**

### **Render Deployment:**
1. **Environment Variables:**
```
PYTHONPATH=/opt/render/project/src
```

2. **Build Command:**
```bash
pip install -r requirements.txt
```

3. **Start Command:**
```bash
cd src && uvicorn api:app --host 0.0.0.0 --port $PORT
```

## 🌐 **URLs Configuration**

### **Development:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### **Production:**
- Frontend: https://tienquocbui.github.io/flight/
- Backend: https://your-render-backend-url.onrender.com

## 🔄 **Deployment Steps**

### **1. Deploy Backend (Render):**
1. Vào https://render.com/
2. Connect GitHub repository
3. Deploy với cấu hình trên
4. Copy backend URL

### **2. Update Frontend API URL:**
1. Tạo file `frontend/.env` với backend URL
2. Push code lên GitHub
3. GitHub Actions sẽ deploy frontend

### **3. Enable GitHub Pages:**
1. Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: "gh-pages"
4. Save

## ✅ **Test Deployment**

### **Backend Test:**
```bash
curl https://your-render-backend-url.onrender.com/stats
```

### **Frontend Test:**
- Truy cập https://tienquocbui.github.io/flight/
- Kiểm tra console để đảm bảo API calls thành công

## 🚨 **Troubleshooting**

### **CORS Issues:**
- Backend đã có CORS middleware
- Nếu vẫn lỗi, check Render environment variables

### **API Connection Issues:**
- Check backend URL trong frontend
- Verify Render deployment status
- Check browser console for errors 