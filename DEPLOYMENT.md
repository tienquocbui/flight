# 🚀 Deployment Guide

## GitHub Actions Deployment

### ✅ **Đã sửa lỗi submodule**
- Xóa frontend khỏi submodule tracking
- Add frontend như regular files
- GitHub Actions sẽ không còn lỗi submodule

### ✅ **Đã sửa lỗi permissions**
- Thêm `permissions` section trong workflow
- `contents: write` - cho phép write vào repository
- `pages: write` - cho phép deploy lên GitHub Pages
- `id-token: write` - cho phép authentication

### 🔧 **Workflows đã tạo**

#### 1. **Test Workflow** (`.github/workflows/test.yml`)
- Test backend imports
- Test data loading
- Test frontend build
- Chạy trên mọi push và PR

#### 2. **Deploy Workflow** (`.github/workflows/deploy.yml`)
- Test + Deploy frontend lên GitHub Pages
- Chỉ chạy trên main branch
- Cần enable GitHub Pages trong repository settings

#### 3. **Simple Deploy Workflow** (`.github/workflows/deploy-simple.yml`)
- Chỉ deploy, không test
- Nhanh hơn cho production

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

#### **Nếu Actions fail với 403 error:**
1. Check repository settings → Actions → General
2. Ensure "Workflow permissions" is set to "Read and write permissions"
3. Or manually set permissions in workflow file

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
- ✅ **Permissions fix**: Applied
- ✅ **Workflows**: Created with proper permissions
- 🔄 **GitHub Pages**: Need to enable
- 🔄 **Frontend deployment**: Ready after enabling Pages

### 🎯 **Next Steps**

1. **Enable GitHub Pages** trong repository settings
2. **Check repository permissions** → Actions → General
3. **Push một commit** để trigger workflow
4. **Check Actions** để đảm bảo build thành công
5. **Access deployed site** tại https://tienquocbui.github.io/flight/

### 📝 **Repository Settings**

#### **Actions Permissions:**
- Go to Settings → Actions → General
- Workflow permissions: "Read and write permissions"
- Allow GitHub Actions to create and approve pull requests: ✅

#### **Pages Settings:**
- Go to Settings → Pages
- Source: "Deploy from a branch"
- Branch: "gh-pages"
- Folder: "/ (root)"

### 🎉 **Deployment sẽ hoạt động sau khi enable GitHub Pages!** 🚀 