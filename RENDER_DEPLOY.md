# 🎨 Deploy Backend lên Render

## Bước 1: Tạo Render Account
1. Vào https://render.com/
2. Sign up với GitHub account
3. Connect repository

## Bước 2: Deploy Backend
1. **New** → **Web Service**
2. **Connect repository**: `tienquocbui/flight`
3. **Name**: `flight-backend`
4. **Root Directory**: `src`
5. **Runtime**: `Python 3`
6. **Build Command**: `pip install --no-cache-dir -r ../requirements.txt`
7. **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

## Bước 3: Environment Variables
Thêm trong Render dashboard:
```
PYTHONPATH=/opt/render/project/src
PIP_NO_CACHE_DIR=1
```

## Bước 4: Get Backend URL
- Render sẽ cung cấp URL như: `https://flight-backend-xxxx.onrender.com`
- Copy URL này để update frontend

## Bước 5: Update Frontend API URL
Cập nhật `frontend/src/api.ts`:
```typescript
const API_BASE = "https://your-render-url.onrender.com";
```

## Bước 6: Deploy Frontend
Push code mới lên GitHub để trigger deployment

## Lưu ý Render:
- Free tier có thể sleep sau 15 phút không hoạt động
- Lần đầu access có thể mất 30-60 giây để wake up
- Có thể upgrade lên paid plan để tránh sleep

## 🔧 Troubleshooting:
- **Rust build error**: Đã fix bằng cách dùng pydantic v1 và --no-cache-dir
- **Build timeout**: Có thể tăng build timeout trong Render settings
- **Memory issues**: Có thể upgrade lên paid plan để có nhiều RAM hơn 