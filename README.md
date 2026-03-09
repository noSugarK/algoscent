# Algoscent 部署文档

## 目录

- [项目概述](#项目概述)
- [环境要求](#环境要求)
- [本地开发环境部署](#本地开发环境部署)
- [Docker 部署](#docker-部署)
- [生产环境配置](#生产环境配置)
- [常见问题](#常见问题)

---

## 项目概述

Algoscent 是一个香水测评系统，包含以下组件：

- **后端**: Django 5.2 + Django REST Framework + MySQL
- **前端**: Vue 3 + Vite + Element Plus
- **密码传输加密**: 使用 RSA 非对称加密保护密码传输

---

## 环境要求

### 本地开发环境

| 组件 | 版本要求 |
|------|----------|
| Python | 3.12+ |
| Node.js | 20.19.0+ 或 22.12.0+ |
| MySQL | 8.0+ |
| npm | 随 Node.js 安装 |

### Docker 部署环境

| 组件 | 版本要求 |
|------|----------|
| Docker | 20.10+ |
| Docker Compose | 2.0+ |

---

## 本地开发环境部署

### 1. 数据库准备

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE algoscent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出 MySQL
exit;
```

### 2. 后端部署

#### 2.1 创建 Python 虚拟环境

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

#### 2.2 安装依赖

```bash
# 升级 pip
python -m pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 如果使用清华镜像源加速
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

#### 2.3 配置数据库连接

编辑 `backend/backend/settings.py` 文件，修改数据库配置：

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'NAME': 'algoscent',           # 数据库名称
        'USER': 'root',                # 数据库用户名
        'PASSWORD': '123456',          # 数据库密码
        'HOST': 'localhost',           # 数据库服务器地址
        'PORT': '3306',                # 数据库端口
    }
}
```

#### 2.4 执行数据库迁移

```bash
# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate
```

#### 2.5 生成 RSA 密钥对

```bash
python manage.py generate_keys
```

#### 2.6 创建超级管理员

```bash
python manage.py create_superuser
```

#### 2.7 导入初始数据

```bash
# 导入问题数据
python manage.py import_questions

# 导入香调类别
python manage.py import_fragrance_categories
```

#### 2.8 启动后端服务

```bash
# 开发模式启动
python manage.py runserver 0.0.0.0:8000

# 或使用 daphne (支持 WebSocket)
daphne -b 0.0.0.0 -p 8000 backend.asgi:application
```

后端服务将在 `http://localhost:8000` 启动。

### 3. 前端部署

#### 3.1 安装依赖

```bash
# 进入前端目录
cd web

# 安装依赖
npm install

# 如果遇到网络问题，可使用国内镜像
npm install --registry=https://registry.npmmirror.com
```

#### 3.2 配置 API 代理

前端已配置开发代理，`/api` 请求会自动代理到 `http://localhost:8000`。

如需修改，编辑 `web/vite.config.js`：

```javascript
server: {
    port: 5173,
    proxy: {
        '/api': {
            target: 'http://localhost:8000',
            changeOrigin: true,
            rewrite: (path) => path.replace(/^\/api/, '')
        }
    }
}
```

#### 3.3 启动前端服务

```bash
# 开发模式启动
npm run dev
```

前端服务将在 `http://localhost:5173` 启动。

### 4. 访问应用

- 前端地址: http://localhost:5173
- 后端 API: http://localhost:8000
- Django Admin: http://localhost:8000/admin

---

## Docker 部署

### 1. 环境准备

确保已安装 Docker 和 Docker Compose：

```bash
# 检查 Docker 版本
docker --version

# 检查 Docker Compose 版本
docker compose version
```

### 2. 配置数据库连接

编辑 `docker-compose.yml` 文件中的数据库配置：

```yaml
services:
  django:
    environment:
      - DATABASE_HOST=your_db_host      # 数据库地址
      - DATABASE_PORT=3306
      - DATABASE_NAME=algoscent
      - DATABASE_USER=root
      - DATABASE_PASSWORD=your_password
```

### 3. 修改后端配置

编辑 `backend/backend/settings.py`，确保数据库配置与 Docker Compose 一致：

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'NAME': 'algoscent',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',    # Docker 内部使用环境变量覆盖
        'PORT': '3306',
    }
}
```

### 4. 构建并启动容器

```bash
# 在项目根目录执行

# 构建镜像
docker compose build

# 启动服务（后台运行）
docker compose up -d

# 查看容器状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 5. 初始化数据库

如果数据库是新建的，需要手动执行迁移：

```bash
# 进入 Django 容器
docker exec -it django bash

# 执行迁移
python manage.py migrate

# 生成密钥
python manage.py generate_keys

# 创建超级管理员
python manage.py create_superuser

# 导入数据
python manage.py import_questions
python manage.py import_fragrance_categories

# 退出容器
exit
```

### 6. 访问应用

- 前端地址: http://localhost:5173
- 后端 API: http://localhost:8000

### 7. Docker 常用命令

```bash
# 停止服务
docker compose down

# 重启服务
docker compose restart

# 重新构建并启动
docker compose up -d --build

# 查看特定服务日志
docker compose logs -f django
docker compose logs -f web

# 进入容器
docker exec -it django bash
docker exec -it web sh
```

---

## 生产环境配置

### 1. 安全配置

#### 1.1 修改 Django 密钥

编辑 `backend/backend/settings.py`：

```python
# 生成新的密钥
SECRET_KEY = 'your-new-secret-key-here'

# 关闭调试模式
DEBUG = False

# 配置允许的主机
ALLOWED_HOSTS = ['your-domain.com', 'your-ip-address']
```

#### 1.2 配置 CORS

```python
CORS_ALLOWED_ORIGINS = [
    "https://your-domain.com",
]
```

### 2. 数据库优化

#### 2.1 创建独立数据库用户

```sql
-- 登录 MySQL
mysql -u root -p

-- 创建用户
CREATE USER 'algoscent'@'%' IDENTIFIED BY 'your_strong_password';

-- 授权
GRANT ALL PRIVILEGES ON algoscent.* TO 'algoscent'@'%';

-- 刷新权限
FLUSH PRIVILEGES;
```

### 3. 静态文件配置

```python
# settings.py 添加
STATIC_ROOT = '/var/www/static/'
```

```bash
# 收集静态文件
python manage.py collectstatic
```

### 4. 前端生产构建

```bash
# 进入前端目录
cd web

# 构建生产版本
npm run build

# 构建产物在 dist 目录
```

### 5. Nginx 配置（生产环境）

创建 `/etc/nginx/conf.d/algoscent.conf`：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 100M;
    
    # 前端静态文件
    location / {
        root /var/www/algoscent/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # API 代理
    location /api/ {
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        proxy_connect_timeout 600s;
        proxy_read_timeout 600s;
        proxy_send_timeout 600s;
        
        rewrite ^/api/(.*)$ /$1 break;
        proxy_pass http://127.0.0.1:8000/;
    }
}
```

### 6. 邮件服务配置

编辑 `backend/backend/settings.py`：

```python
# QQ 邮箱配置
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your-email@qq.com'
EMAIL_HOST_PASSWORD = 'your-authorization-code'  # QQ邮箱授权码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

---

## 常见问题

### 1. 数据库连接失败

**问题**: `Can't connect to MySQL server`

**解决方案**:
- 检查 MySQL 服务是否启动
- 确认数据库配置正确
- 检查防火墙是否开放 3306 端口

```bash
# 检查 MySQL 状态
# Linux
sudo systemctl status mysql

# Windows
net start MySQL80
```

### 2. 前端跨域问题

**问题**: API 请求出现 CORS 错误

**解决方案**:
- 确保后端安装了 `django-cors-headers`
- 检查 `settings.py` 中的 `CORS_ALLOWED_ORIGINS` 配置

### 3. RSA 密钥问题

**问题**: 登录时提示密钥错误

**解决方案**:
```bash
# 重新生成密钥
python manage.py generate_keys
```

### 4. Docker 容器无法启动

**问题**: 容器启动失败或立即退出

**解决方案**:
```bash
# 查看详细日志
docker compose logs django

# 检查端口占用
netstat -tlnp | grep 8000
netstat -tlnp | grep 5173
```

### 5. 依赖安装失败

**问题**: `mysqlclient` 安装失败

**解决方案**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# CentOS/RHEL
sudo yum install python3-devel mysql-devel

# macOS
brew install mysql-client
```

### 6. 前端构建内存不足

**问题**: `JavaScript heap out of memory`

**解决方案**:
```bash
# 增加 Node.js 内存限制
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

---

## 密码传输加密

系统使用 RSA 非对称加密保护用户密码传输安全。

### 生成密钥对

```bash
python backend/apps/account/management/commands/generate_keys.py
```

或使用 Django 命令：

```bash
python manage.py generate_keys
```

### 定时更换密钥

建议设置定时任务定期更换密钥对：

```bash
# Linux crontab 示例（每周更换）
0 0 * * 0 cd /path/to/algoscent && python manage.py generate_keys
```

---

## 技术支持

如有问题，请查看项目日志或联系开发团队。
