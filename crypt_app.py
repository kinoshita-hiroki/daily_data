import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import random
import config
from ui import get_fernet
from crypt.encrypt_utils import save_encrypted_csv, load_encrypted_csv, get_fernet_from_env

def crypt_debug(header, raw_csv, encrypted_tmp_csv, encrypted_csv, tmp_csv, column_names):
    load_dotenv()
    KEY = os.getenv("FERNET_KEY").encode()
    st.subheader(header)

    mode = st.radio("モードを選択", ["暗号化", "復号化"], key=random.random())
    fernet = get_fernet()
    if mode == "暗号化":
        if st.button("暗号化", key=random.random()):
            df = pd.read_csv(raw_csv)
            save_encrypted_csv(encrypted_tmp_csv, df, fernet)
            st.success("暗号化しました！")
    elif mode == "復号化":
        if st.button("復号化", key=random.random()):
            try:
                df = load_encrypted_csv(encrypted_csv, fernet, columns=column_names)
                df.to_csv(tmp_csv, index=False)
                st.success("復号しました！")
            except Exception as e:
                st.error(f"復号に失敗: {e}")

st.title("デバッグ用暗号化 / 復号化ツール")
crypt_debug("内省用", config.SENTIMENT_CSV, config.ENCRYPT_SENTIMENT_TMP_CSV, config.ENCRYPT_SENTIMENT_CSV, config.SENTIMENT_TMP_CSV, ["日付", "対象", "事実", "感情", "詳細感情", "感想", "対処法"])
crypt_debug("観察用", config.OBSERVATION_CSV, config.ENCRYPT_OBSERVATION_TMP_CSV, config.ENCRYPT_OBSERVATION_CSV, config.OBSERVATION_TMP_CSV, ["日付", "対象", "事実", "感情", "洞察", "対処法"])