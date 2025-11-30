import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import config
from ui import get_fernet
from crypt.encrypt_utils import save_encrypted_csv, load_encrypted_csv, get_fernet_from_env

load_dotenv()
KEY = os.getenv("FERNET_KEY").encode()

st.title("デバッグ用暗号化 / 復号化ツール")

mode = st.radio("モードを選択", ["暗号化", "復号化"])
fernet = get_fernet()
if mode == "暗号化":
    if st.button("暗号化"):
        #どちらかをコメントアウト
        #df = load_encrypted_csv(config.ENCRYPT_SENTIMENT_CSV, fernet, columns=["日付", "対象", "事実", "感情", "詳細感情", "感想", "対処法"])
        df = pd.read_csv(config.SENTIMENT_CSV)
        # 保存
        save_encrypted_csv(config.ENCRYPT_SENTIMENT_TMP_CSV, df, fernet)
        st.success("暗号化しました！")
elif mode == "復号化":
    if st.button("復号化"):
        try:
            df = load_encrypted_csv(config.ENCRYPT_SENTIMENT_CSV, fernet, columns=["日付", "対象", "事実", "感情", "詳細感情", "感想", "対処法"])
            df.to_csv(config.SENTIMENT_TMP_CSV, index=False)
            st.success("復号しました！")
        except Exception as e:
            st.error(f"復号に失敗: {e}")
