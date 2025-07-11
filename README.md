# Django 部落格範例專案

一個功能完整的 Django 部落格應用程式，展示 Django 框架的核心功能和最佳實踐。

## 📋 專案簡介

這是一個使用 Django 4.2+ 建立的部落格範例專案，包含完整的部落格功能：

- ✅ 文章發布與管理
- ✅ 分類與標籤系統
- ✅ 評論功能
- ✅ 搜尋功能
- ✅ 分頁系統
- ✅ 響應式設計
- ✅ Django Admin 整合
- ✅ 使用者認證

## 🚀 功能特色

### 核心功能
- **文章管理**: 支援 Markdown 格式，包含標題、內容、摘要、特色圖片
- **分類系統**: 階層式分類管理
- **標籤功能**: 靈活的標籤系統，支援多標籤
- **評論系統**: 使用者可對文章發表評論，支援評論管理
- **搜尋功能**: 全文搜尋文章標題和內容
- **分頁系統**: 優化載入效能，支援自定義每頁顯示數量

### 使用者體驗
- **響應式設計**: 支援桌面、平板、手機等各種裝置
- **現代化 UI**: 使用 Bootstrap 5 和 Font Awesome 圖示
- **SEO 友善**: 優化的 URL 結構和 meta 標籤
- **社群分享**: 支援 Facebook、Twitter 分享功能

### 管理功能
- **Django Admin**: 完整的後台管理介面
- **權限控制**: 基於 Django 的使用者權限系統
- **批次操作**: 支援批次核准/拒絕評論
- **資料統計**: 文章、評論數量統計

## 🛠️ 技術架構

### 後端技術
- **Django 4.2+**: Web 框架
- **Python 3.8+**: 程式語言
- **SQLite**: 資料庫（可輕鬆切換至 PostgreSQL/MySQL）
- **Pillow**: 圖片處理
- **WhiteNoise**: 靜態檔案服務

### 前端技術
- **Bootstrap 5**: CSS 框架
- **Font Awesome 6**: 圖示庫
- **JavaScript**: 互動功能
- **響應式設計**: 支援各種螢幕尺寸

### 開發工具
- **Git**: 版本控制
- **虛擬環境**: 依賴隔離
- **Django Debug Toolbar**: 開發除錯
- **單元測試**: 程式碼品質保證

## 📦 環境建置

### 系統需求
- Python 3.8 或更高版本
- pip (Python 套件管理器)
- Git

### 安裝步驟

1. **複製專案**
```bash
git clone https://github.com/jackycj0830/Django_Sample.git
cd Django_Sample
```

2. **建立虛擬環境**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **安裝依賴套件**
```bash
pip install -r requirements.txt
```

4. **資料庫遷移**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **建立超級使用者**
```bash
python manage.py createsuperuser
```

6. **收集靜態檔案**
```bash
python manage.py collectstatic
```

7. **啟動開發伺服器**
```bash
python manage.py runserver
```

8. **瀏覽網站**
   - 前台: http://127.0.0.1:8000/
   - 後台: http://127.0.0.1:8000/admin/

## 🎯 使用指南

### 基本使用

1. **訪問網站**: 開啟瀏覽器，前往 `http://127.0.0.1:8000/`
2. **瀏覽文章**: 在首頁瀏覽最新文章
3. **搜尋文章**: 使用右側搜尋框搜尋感興趣的內容
4. **分類瀏覽**: 點擊分類連結瀏覽特定分類的文章
5. **標籤篩選**: 點擊標籤快速找到相關文章

### 管理後台使用

1. **登入後台**: 前往 `http://127.0.0.1:8000/admin/`
2. **文章管理**:
   - 新增文章: 點擊「文章」→「新增」
   - 編輯文章: 在文章列表中點擊要編輯的文章
   - 設定分類: 在「分類」區塊管理文章分類
   - 管理標籤: 在「標籤」區塊新增或編輯標籤

3. **評論管理**:
   - 查看評論: 在「評論」區塊查看所有評論
   - 核准評論: 選擇評論後使用批次操作
   - 刪除垃圾評論: 選擇不當評論並刪除

### 發布文章流程

1. 登入管理後台
2. 點擊「文章」→「新增文章」
3. 填寫文章資訊：
   - 標題: 文章標題
   - 網址別名: 用於 URL 的別名（會自動生成）
   - 內容: 文章正文
   - 摘要: 文章摘要（選填）
   - 分類: 選擇文章分類
   - 標籤: 選擇或新增標籤
   - 特色圖片: 上傳文章封面圖片（選填）
   - 狀態: 選擇「已發布」或「草稿」
4. 點擊「儲存」發布文章

## 🧪 測試

### 執行測試
```bash
# 執行所有測試
python manage.py test

# 執行特定應用程式的測試
python manage.py test blog

# 執行特定測試類別
python manage.py test blog.tests.BlogModelTests

# 顯示詳細測試資訊
python manage.py test --verbosity=2
```

### 測試覆蓋率
```bash
# 安裝 coverage
pip install coverage

# 執行測試並收集覆蓋率資料
coverage run --source='.' manage.py test

# 生成覆蓋率報告
coverage report

# 生成 HTML 覆蓋率報告
coverage html
```

## 📁 專案結構

```
Django_Sample/
├── django_sample/          # 主專案設定
│   ├── __init__.py
│   ├── settings.py         # Django 設定檔
│   ├── urls.py            # 主 URL 配置
│   ├── wsgi.py            # WSGI 配置
│   └── asgi.py            # ASGI 配置
├── blog/                   # 部落格應用程式
│   ├── __init__.py
│   ├── admin.py           # 管理後台配置
│   ├── apps.py            # 應用程式配置
│   ├── models.py          # 資料模型
│   ├── views.py           # 視圖函數
│   ├── urls.py            # URL 配置
│   ├── forms.py           # 表單定義
│   ├── tests.py           # 測試程式碼
│   └── templatetags/      # 自定義模板標籤
│       ├── __init__.py
│       └── blog_extras.py
├── templates/              # HTML 模板
│   ├── base.html          # 基礎模板
│   └── blog/              # 部落格模板
│       ├── post_list.html
│       ├── post_detail.html
│       ├── category_detail.html
│       ├── tag_detail.html
│       ├── about.html
│       └── sidebar.html
├── static/                 # 靜態檔案
│   └── css/
│       └── style.css      # 自定義樣式
├── media/                  # 媒體檔案（上傳的圖片等）
├── manage.py              # Django 管理腳本
├── requirements.txt       # Python 依賴套件
├── .gitignore            # Git 忽略檔案
└── README.md             # 專案說明文件
```

## 🔧 開發指南

### 新增應用程式

1. **建立新的 Django 應用程式**
```bash
python manage.py startapp app_name
```

2. **在 `settings.py` 中註冊應用程式**
```python
INSTALLED_APPS = [
    # ... 其他應用程式
    'app_name',
]
```

3. **建立模型、視圖、URL 配置**

### 資料庫操作

```bash
# 建立遷移檔案
python manage.py makemigrations

# 查看遷移 SQL
python manage.py sqlmigrate blog 0001

# 執行遷移
python manage.py migrate

# 重置資料庫（小心使用）
python manage.py flush
```

### 管理命令

```bash
# 建立超級使用者
python manage.py createsuperuser

# 收集靜態檔案
python manage.py collectstatic

# 清除快取
python manage.py clear_cache

# 檢查專案問題
python manage.py check
```

## 🎨 客製化指南

### 修改樣式

1. **編輯 CSS 檔案**: `static/css/style.css`
2. **使用 Bootstrap 變數**: 可以覆寫 Bootstrap 的預設變數
3. **新增自定義 JavaScript**: 在 `static/js/` 目錄下新增 JS 檔案

### 新增功能

1. **擴展模型**: 在 `blog/models.py` 中新增欄位或模型
2. **建立視圖**: 在 `blog/views.py` 中新增視圖函數
3. **設計模板**: 在 `templates/blog/` 中新增 HTML 模板
4. **配置 URL**: 在 `blog/urls.py` 中新增 URL 路由

### 整合第三方套件

1. **安裝套件**: `pip install package_name`
2. **更新 requirements.txt**: `pip freeze > requirements.txt`
3. **在 settings.py 中配置**: 新增必要的設定
4. **在應用程式中使用**: 匯入並使用套件功能

## 🚀 部署指南

### 準備部署

1. **設定環境變數**
```python
# settings.py
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
```

2. **建立 .env 檔案**
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

3. **設定資料庫**
```python
# 生產環境使用 PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

### Heroku 部署

1. **安裝 Heroku CLI**
2. **建立 Procfile**
```
web: gunicorn django_sample.wsgi
```

3. **安裝 gunicorn**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

4. **部署到 Heroku**
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Docker 部署

1. **建立 Dockerfile**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "django_sample.wsgi:application", "--bind", "0.0.0.0:8000"]
```

2. **建立 docker-compose.yml**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=1
```

## 🤝 貢獻指南

我們歡迎任何形式的貢獻！請遵循以下步驟：

### 貢獻流程

1. **Fork 專案**: 點擊 GitHub 上的 Fork 按鈕
2. **建立分支**: `git checkout -b feature/your-feature-name`
3. **提交變更**: `git commit -am 'Add some feature'`
4. **推送分支**: `git push origin feature/your-feature-name`
5. **建立 Pull Request**: 在 GitHub 上建立 PR

### 程式碼規範

- 遵循 PEP 8 Python 程式碼風格
- 為新功能撰寫測試
- 更新相關文件
- 確保所有測試通過

### 報告問題

如果您發現 bug 或有功能建議，請：

1. 檢查是否已有相似的 issue
2. 建立新的 issue，詳細描述問題
3. 提供重現步驟和環境資訊

## 🔍 疑難排解

### 常見問題

**Q: 啟動伺服器時出現 "No module named 'django'" 錯誤**
A: 請確認已啟用虛擬環境並安裝了 Django：
```bash
source venv/bin/activate  # Linux/macOS
pip install django
```

**Q: 資料庫遷移失敗**
A: 嘗試重置遷移：
```bash
python manage.py migrate --fake-initial
```

**Q: 靜態檔案無法載入**
A: 確認已收集靜態檔案：
```bash
python manage.py collectstatic
```

**Q: 圖片上傳失敗**
A: 檢查 media 目錄權限和 settings.py 中的 MEDIA_ROOT 設定

### 除錯技巧

1. **啟用 DEBUG 模式**: 在 settings.py 中設定 `DEBUG = True`
2. **查看日誌**: 檢查 Django 的錯誤日誌
3. **使用 Django shell**: `python manage.py shell` 進行互動式除錯
4. **安裝 Django Debug Toolbar**: 用於詳細的除錯資訊

### 效能優化

1. **資料庫查詢優化**: 使用 `select_related()` 和 `prefetch_related()`
2. **快取設定**: 配置 Redis 或 Memcached
3. **靜態檔案壓縮**: 使用 WhiteNoise 或 CDN
4. **圖片優化**: 壓縮圖片大小

## 📚 學習資源

### Django 官方文件
- [Django 官方文件](https://docs.djangoproject.com/)
- [Django 教學](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
- [Django 最佳實踐](https://docs.djangoproject.com/en/4.2/misc/design-philosophies/)

### 推薦書籍
- "Django for Beginners" by William S. Vincent
- "Two Scoops of Django" by Daniel Roy Greenfeld
- "Django for Professionals" by William S. Vincent

### 線上課程
- [Django 官方教學](https://www.djangoproject.com/start/)
- [MDN Django 教學](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)

## 📄 授權條款

本專案採用 MIT 授權條款。詳細內容請參閱 [LICENSE](LICENSE) 檔案。

## 👥 作者與貢獻者

- **主要開發者**: [jackycj0830](https://github.com/jackycj0830)
- **貢獻者**: 歡迎查看 [Contributors](https://github.com/jackycj0830/Django_Sample/contributors) 頁面

## 📞 聯絡資訊

- **GitHub**: [Django_Sample](https://github.com/jackycj0830/Django_Sample)
- **Email**: 34931815+jackycj0830@users.noreply.github.com
- **Issues**: [回報問題](https://github.com/jackycj0830/Django_Sample/issues)

## 🙏 致謝

感謝以下開源專案和社群：

- [Django](https://www.djangoproject.com/) - 優秀的 Python Web 框架
- [Bootstrap](https://getbootstrap.com/) - 響應式 CSS 框架
- [Font Awesome](https://fontawesome.com/) - 圖示庫
- Django 社群的所有貢獻者

---

⭐ 如果這個專案對您有幫助，請給我們一個 Star！

📝 最後更新：2024年7月