#!/bin/bash
# python3 manage.py makemigrations
python manage.py migrate
# python3 manage.py init
# 生成密钥
python generate_keys.py
# 自动创建超级管理员
python create_superuser.py
daphne -b 0.0.0.0 -p 8000 --proxy-headers backend.asgi:application
