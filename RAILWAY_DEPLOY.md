# 🚂 Deploy Backend lên Railway

## Bước 1: Tạo Railway Account
1. Vào https://railway.app/
2. Sign up với GitHub account
3. Connect repository

## Bước 2: Deploy Backend
1. **New Project** → **Deploy from GitHub repo**
2. Chọn repository: `tienquocbui/flight`
3. **Root Directory**: `src`
4. **Build Command**: `pip install -r ../requirements.txt`
5. **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

## Bước 3: Environment Variables
Thêm trong Railway dashboard:
```
PYTHONPATH=/app
```

## Bước 4: Get Backend URL
- Railway sẽ cung cấp URL như: `https://flight-backend-production.up.railway.app`
- Copy URL này để update frontend

## Bước 5: Update Frontend API URL
Cập nhật `frontend/src/api.ts`:
```typescript
const API_BASE = "https://your-railway-url.railway.app";
```

## Bước 6: Deploy Frontend
Push code mới lên GitHub để trigger deployment. 