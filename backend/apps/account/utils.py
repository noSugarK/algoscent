import base64

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

def decrypt_with_private_key(encrypted_data: str) -> str:
    key_path = os.path.join(os.path.dirname(__file__), 'keys', 'private_key.pem')
    print(key_path)
    with open(key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # 如果私钥有密码，填在这里
        )

    # Base64 解码
    encrypted_bytes = base64.b64decode(encrypted_data)

    # RSA 解密
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.PKCS1v15()  # 或 OAEP
    )
    return decrypted.decode('utf-8')