#!/bin/bash
# python3 manage.py makemigrations
python manage.py migrate
# python3 manage.py init
# 生成密钥
python manage.py generate_keys
# 自动创建超级管理员
python manage.py create_superuser
# 导入问题
python manage.py import_questions
# 导入香调类别
python manage.py import_fragrance_categories
daphne -b 0.0.0.0 -p 8000 --proxy-headers backend.asgi:application
