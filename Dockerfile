# 使用官方 Python 3.9 映像作為基礎
FROM python:3.9-slim

# 設定環境變數
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        libjpeg-dev \
        libpng-dev \
        libwebp-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libopenjp2-7-dev \
        libtiff5-dev \
        tk-dev \
        tcl-dev \
        libharfbuzz-dev \
        libfribidi-dev \
        libxcb1-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 複製專案檔案
COPY . .

# 建立媒體和靜態檔案目錄
RUN mkdir -p /app/media /app/staticfiles

# 收集靜態檔案
RUN python manage.py collectstatic --noinput

# 建立非 root 使用者
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 健康檢查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000', timeout=10)"

# 啟動命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "django_sample.wsgi:application"]
