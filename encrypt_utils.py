# encrypt_utils.py
import os
import json
import io
from cryptography.fernet import Fernet, InvalidToken
import pandas as pd

def get_fernet_from_env(env_name="FERNET_KEY"):
    """環境変数からキーを取得して Fernet オブジェクトを返す。
       Key が無ければ None を返す（呼び出し側でエラーハンドリングを）"""
    key = os.getenv(env_name)
    if not key:
        return None
    return Fernet(key.encode() if isinstance(key, str) else key)

# ---- JSON ----
def save_encrypted_json(path: str, obj, fernet: Fernet):
    """obj を JSON 化して暗号化してファイルへ書き込む"""
    assert fernet is not None, "Fernet key required"
    raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    token = fernet.encrypt(raw)
    with open(path, "wb") as f:
        f.write(token)

def load_encrypted_json(path: str, fernet: Fernet):
    """暗号化ファイルを読み込んで復号→JSONを返す"""
    if not os.path.exists(path):
        return {}
    assert fernet is not None, "Fernet key required"
    with open(path, "rb") as f:
        token = f.read()
    try:
        raw = fernet.decrypt(token)
    except InvalidToken:
        raise ValueError("Decryption failed: invalid key or corrupted file")
    return json.loads(raw.decode("utf-8"))

# ---- CSV / DataFrame ----
def save_encrypted_csv(path: str, df: pd.DataFrame, fernet: Fernet):
    """DataFrame を CSV にし、それを暗号化して保存"""
    assert fernet is not None, "Fernet key required"
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    token = fernet.encrypt(csv_bytes)
    with open(path, "wb") as f:
        f.write(token)

def load_encrypted_csv(path: str, fernet: Fernet, columns=None):
    """暗号化CSVを読み込み復号→DataFrame返す"""
    if not os.path.exists(path):
        return pd.DataFrame(columns=columns if columns else [])
    assert fernet is not None, "Fernet key required"
    with open(path, "rb") as f:
        token = f.read()
    try:
        csv_bytes = fernet.decrypt(token)
    except InvalidToken:
        raise ValueError("Decryption failed: invalid key or corrupted file")
    return pd.read_csv(io.BytesIO(csv_bytes), encoding="utf-8", header=0)
