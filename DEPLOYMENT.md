# 🚀 Deployment Guide

## GitHub Actions Deployment

### ✅ **Đã sửa lỗi submodule**
- Xóa frontend khỏi submodule tracking
- Add frontend như regular files
- GitHub Actions sẽ không còn lỗi submodule

### 🔧 **Workflows đã tạo**

#### 1. **Test Workflow** (`.github/workflows/test.yml`)
- Test backend imports
- Test data loading
- Test frontend build
- Chạy trên mọi push và PR

#### 2. **Deploy Workflow** (`.github/workflows/deploy.yml`)
- Deploy frontend lên GitHub Pages
- Chỉ chạy trên main branch
- Cần enable GitHub Pages trong repository settings

### 📋 **Cách enable GitHub Pages**

1. **Vào repository settings:**
   - Go to https://github.com/tienquocbui/flight/settings

2. **Enable GitHub Pages:**
   - Scroll down to "Pages" section
   - Source: "Deploy from a branch"
   - Branch: "gh-pages" (sẽ được tạo tự động)
   - Folder: "/ (root)"

3. **Check Actions:**
   - Go to https://github.com/tienquocbui/flight/actions
   - Workflows sẽ chạy tự động

### 🌐 **Deployment URLs**

- **GitHub Pages**: https://tienquocbui.github.io/flight/
- **Repository**: https://github.com/tienquocbui/flight
- **Actions**: https://github.com/tienquocbui/flight/actions

### 🔍 **Troubleshooting**

#### **Nếu Actions fail:**
1. Check Actions tab trong GitHub
2. Xem log lỗi cụ thể
3. Fix lỗi và push lại

#### **Nếu frontend không load:**
1. Check GitHub Pages settings
2. Verify gh-pages branch được tạo
3. Check build output trong Actions

#### **Nếu backend không chạy:**
- Backend cần được deploy riêng (Heroku, Railway, etc.)
- Frontend sẽ cần update API URL

### 📊 **Current Status**

- ✅ **Repository**: https://github.com/tienquocbui/flight
- ✅ **Submodule fix**: Applied
- ✅ **Workflows**: Created
- 🔄 **GitHub Pages**: Need to enable
- 🔄 **Frontend deployment**: Pending

### 🎯 **Next Steps**

1. **Enable GitHub Pages** trong repository settings
2. **Push một commit** để trigger workflow
3. **Check Actions** để đảm bảo build thành công
4. **Access deployed site** tại https://tienquocbui.github.io/flight/

### 📝 **Notes**

- **Frontend only**: GitHub Pages chỉ deploy frontend
- **Backend needed**: Cần deploy backend riêng cho full functionality
- **API calls**: Frontend sẽ gọi localhost:8000 (cần update cho production)
- **CORS**: Backend cần allow GitHub Pages domain

**Deployment sẽ hoạt động sau khi enable GitHub Pages!** 🚀 