#!/bin/bash

# Django 部落格專案部署腳本
# 使用方法: ./deploy.sh [環境]
# 環境選項: development, production

set -e  # 遇到錯誤時停止執行

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函數定義
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 檢查參數
ENVIRONMENT=${1:-development}

if [[ "$ENVIRONMENT" != "development" && "$ENVIRONMENT" != "production" ]]; then
    print_error "無效的環境參數。請使用 'development' 或 'production'"
    exit 1
fi

print_info "開始部署 Django 部落格專案 (環境: $ENVIRONMENT)"

# 檢查 Python 版本
print_info "檢查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_success "Python 版本檢查通過: $python_version"
else
    print_error "需要 Python $required_version 或更高版本，目前版本: $python_version"
    exit 1
fi

# 檢查虛擬環境
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "未偵測到虛擬環境，建議使用虛擬環境"
    read -p "是否要建立並啟用虛擬環境? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "建立虛擬環境..."
        python3 -m venv venv
        print_info "啟用虛擬環境..."
        source venv/bin/activate
        print_success "虛擬環境已啟用"
    fi
else
    print_success "虛擬環境已啟用: $VIRTUAL_ENV"
fi

# 安裝依賴套件
print_info "安裝 Python 依賴套件..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "依賴套件安裝完成"

# 環境變數檢查
if [[ "$ENVIRONMENT" == "production" ]]; then
    if [[ ! -f ".env" ]]; then
        print_warning "生產環境需要 .env 檔案"
        print_info "建立範例 .env 檔案..."
        cat > .env << EOF
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=sqlite:///db.sqlite3
EOF
        print_warning "請編輯 .env 檔案並設定正確的值"
    fi
fi

# 資料庫遷移
print_info "執行資料庫遷移..."
python manage.py makemigrations
python manage.py migrate
print_success "資料庫遷移完成"

# 收集靜態檔案
if [[ "$ENVIRONMENT" == "production" ]]; then
    print_info "收集靜態檔案..."
    python manage.py collectstatic --noinput
    print_success "靜態檔案收集完成"
fi

# 建立超級使用者 (僅開發環境)
if [[ "$ENVIRONMENT" == "development" ]]; then
    print_info "檢查是否需要建立超級使用者..."
    if ! python manage.py shell -c "from django.contrib.auth.models import User; exit(0 if User.objects.filter(is_superuser=True).exists() else 1)" 2>/dev/null; then
        print_info "建立超級使用者..."
        echo "請輸入超級使用者資訊:"
        python manage.py createsuperuser
        print_success "超級使用者建立完成"
    else
        print_info "超級使用者已存在，跳過建立"
    fi
fi

# 建立範例資料 (僅開發環境)
if [[ "$ENVIRONMENT" == "development" ]]; then
    read -p "是否要建立範例資料? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "建立範例資料..."
        python manage.py create_sample_data --posts 15 --comments 30
        print_success "範例資料建立完成"
    fi
fi

# 執行測試
print_info "執行測試..."
python manage.py test --verbosity=1
if [[ $? -eq 0 ]]; then
    print_success "所有測試通過"
else
    print_warning "部分測試失敗，請檢查程式碼"
fi

# 檢查專案問題
print_info "檢查專案設定..."
python manage.py check
if [[ $? -eq 0 ]]; then
    print_success "專案檢查通過"
else
    print_error "專案檢查發現問題，請修正後再部署"
    exit 1
fi

# 啟動開發伺服器 (僅開發環境)
if [[ "$ENVIRONMENT" == "development" ]]; then
    print_success "部署完成！"
    echo
    print_info "可用的管理命令:"
    echo "  python manage.py runserver          # 啟動開發伺服器"
    echo "  python manage.py createsuperuser    # 建立超級使用者"
    echo "  python manage.py create_sample_data  # 建立範例資料"
    echo "  python manage.py test               # 執行測試"
    echo "  python manage.py shell              # 進入 Django shell"
    echo
    print_info "網站連結:"
    echo "  前台: http://127.0.0.1:8000/"
    echo "  後台: http://127.0.0.1:8000/admin/"
    echo "  API:  http://127.0.0.1:8000/api-docs/"
    echo
    
    read -p "是否要啟動開發伺服器? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "啟動開發伺服器..."
        python manage.py runserver
    fi
else
    print_success "生產環境部署完成！"
    print_info "請使用適當的 WSGI 伺服器 (如 Gunicorn) 來運行應用程式"
    print_info "範例: gunicorn django_sample.wsgi:application --bind 0.0.0.0:8000"
fi
