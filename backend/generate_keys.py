#!/usr/bin/env python3
"""
安全密钥生成器
用于生成 Flask 应用的 SECRET_KEY 和 JWT_SECRET_KEY
"""
import secrets
import string

def generate_secure_key(length=64):
    """生成安全的随机密钥"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_hex_key(length=32):
    """生成十六进制密钥"""
    return secrets.token_hex(length)

if __name__ == '__main__':
    print('🔐 生成安全密钥')
    print('=' * 60)
    
    # 生成 SECRET_KEY (64字符)
    secret_key = generate_hex_key(32)  # 32字节 = 64字符十六进制
    print(f'SECRET_KEY={secret_key}')
    
    # 生成 JWT_SECRET_KEY (64字符)
    jwt_secret_key = generate_hex_key(32)  # 32字节 = 64字符十六进制
    print(f'JWT_SECRET_KEY={jwt_secret_key}')
    
    print('=' * 60)
    print('✅ 密钥生成完成！请复制上面的密钥到你的 .env.production 文件中')