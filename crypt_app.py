import pandas as pd
import streamlit as st
from dotenv import load_dotenv

import app.config.config as config
from app.crypt.encrypt_utils import load_encrypted_csv, save_encrypted_csv
from app.ui import get_fernet, render_top_image_base64


def crypt_debug(header, raw_csv, encrypted_tmp_csv, encrypted_csv, tmp_csv, column_names, keys):
    load_dotenv()
    st.subheader(header)

    mode = st.radio("モードを選択", ["暗号化", "復号化"], key=keys[0])
    fernet = get_fernet()
    if mode == "暗号化":
        if st.button("暗号化", key=keys[1]):
            df = pd.read_csv(raw_csv)
            save_encrypted_csv(encrypted_tmp_csv, df, fernet)
            st.success("暗号化しました！")
    elif mode == "復号化":
        if st.button("復号化", key=keys[2]):
            try:
                df = load_encrypted_csv(encrypted_csv, fernet, columns=column_names)
                df.to_csv(tmp_csv, index=False)
                st.success("復号しました！")
            except Exception as e:
                st.error(f"復号に失敗: {e}")


render_top_image_base64(config.TOP_IMAGE_PATH5)
st.title("🧑‍🔧 デバッグ用暗号化 / 復号化ツール")
crypt_debug("内省用", config.SENTIMENT_CSV, config.ENCRYPT_SENTIMENT_TMP_CSV, config.ENCRYPT_SENTIMENT_CSV, config.SENTIMENT_TMP_CSV, ["日付", "対象", "事実", "感情", "詳細感情", "感想", "対処法"], [1, 2, 3])
crypt_debug("観察用", config.OBSERVATION_CSV, config.ENCRYPT_OBSERVATION_TMP_CSV, config.ENCRYPT_OBSERVATION_CSV, config.OBSERVATION_TMP_CSV, ["日付", "対象", "事実", "感情", "洞察", "対処法"], [4, 5, 6])
