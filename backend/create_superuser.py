import os
import django
from django.contrib.auth import get_user_model

# 初始化Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

User = get_user_model()

# 超级管理员默认信息（可根据需要修改）
SUPERUSER_USERNAME = "admin"
SUPERUSER_EMAIL = "admin@example.com"
SUPERUSER_PASSWORD = "admin"  # 生产环境建议修改为更安全的密码

def create_superuser():
    if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
        User.objects.create_superuser(
            username=SUPERUSER_USERNAME,
            email=SUPERUSER_EMAIL,
            password=SUPERUSER_PASSWORD,
            full_name="超级管理员"  # 对应USER模型的full_name字段
        )
        print(f"✅ 超级管理员 {SUPERUSER_USERNAME} 创建成功")
    else:
        print(f"ℹ️ 超级管理员 {SUPERUSER_USERNAME} 已存在")

if __name__ == "__main__":
    create_superuser()
