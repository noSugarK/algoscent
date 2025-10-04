from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate RSA keys for the application'

    def handle(self, *args, **options):
        # 生成私钥
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # 生成公钥
        public_key = private_key.public_key()

        # PEM 格式序列化
        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # 写入文件
        keys_dir = os.path.join(os.path.dirname(__file__), '../../keys')
        os.makedirs(keys_dir, exist_ok=True)

        with open(os.path.join(keys_dir, 'private_key.pem'), 'wb') as f:
            f.write(pem_private)
            self.stdout.write(self.style.SUCCESS('✅ 私钥已保存：private_key.pem'))

        with open(os.path.join(keys_dir, 'public_key.pem'), 'wb') as f:
            f.write(pem_public)
            self.stdout.write(self.style.SUCCESS('✅ 公钥已保存：public_key.pem'))