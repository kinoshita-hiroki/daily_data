from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())   # 生成された文字列をコピーして安全な場所へ
