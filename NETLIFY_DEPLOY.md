# 🌐 Deploy Frontend lên Netlify

## Bước 1: Tạo Netlify Account
1. Vào https://netlify.com/
2. Sign up với GitHub account
3. Connect repository

## Bước 2: Deploy Frontend
1. **New site from Git**
2. **Connect to Git provider**: GitHub
3. **Repository**: `tienquocbui/flight`
4. **Base directory**: `frontend`
5. **Build command**: `npm run build`
6. **Publish directory**: `build`
7. **Branch**: `main`

## Bước 3: Environment Variables
Thêm trong Netlify dashboard:
```
REACT_APP_API_URL=https://your-render-backend-url.onrender.com
```

## Bước 4: Build Settings
- **Node version**: 18 (hoặc 16)
- **NPM version**: 9 (hoặc 8)

## Bước 5: Custom Domain (Optional)
- Có thể setup custom domain
- Netlify cung cấp subdomain miễn phí

## Bước 6: Update API URL
Sau khi có backend URL, update environment variable:
1. Site settings → Environment variables
2. Add: `REACT_APP_API_URL`
3. Value: Backend URL từ Render

## Lưu ý Netlify:
- Free tier rất tốt cho frontend
- Auto-deploy khi push code
- CDN global
- SSL tự động

## 🔧 Troubleshooting:
- **Build errors**: Check Node.js version
- **API connection**: Verify environment variables
- **CORS issues**: Check backend CORS settings 