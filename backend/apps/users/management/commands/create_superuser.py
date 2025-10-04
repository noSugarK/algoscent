import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser for the application'
    
    def handle(self, *args, **options):
        # 超级管理员默认信息（可根据需要修改）
        SUPERUSER_USERNAME = "admin"
        SUPERUSER_EMAIL = "admin@example.com"
        SUPERUSER_PASSWORD = "admin"  # 生产环境建议修改为更安全的密码
        
        User = get_user_model()
        
        if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
            User.objects.create_superuser(
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASSWORD,
                full_name="超级管理员"  # 对应USER模型的full_name字段
            )
            self.stdout.write(self.style.SUCCESS(f"✅ 超级管理员 {SUPERUSER_USERNAME} 创建成功"))
        else:
            self.stdout.write(self.style.NOTICE(f"ℹ️ 超级管理员 {SUPERUSER_USERNAME} 已存在"))
