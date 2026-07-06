import sqlite3
from pathlib import Path

# プロジェクトルート
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# DBファイル
DB_PATH = PROJECT_ROOT / "data" / "task_rpg.db"


def get_connection():
    """SQLiteへの接続を返す"""
    return sqlite3.connect(DB_PATH)
