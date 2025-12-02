# app_refactor_base64_topimage.py
import os
import json
from datetime import date, datetime, timedelta
import base64

import streamlit as st
import pandas as pd
from PIL import Image
import config


from crypt.encrypt_utils import get_fernet_from_env, load_encrypted_json, save_encrypted_json, load_encrypted_csv, save_encrypted_csv
from utils import load_json, load_csv, iso, save_json,save_csv, append_or_update
from ui import render_top_image_base64, render_weather_section, render_goal_tasks_section, render_daily_numeric_section, render_feeling_regist


# --------------------------
# Main App
# --------------------------
# トップ画像表示（Base64埋め込み・縦幅固定）
render_top_image_base64(config.TOP_IMAGE_PATH)

st.title("🤐 My Daily Board")

all_data = load_json(config.DATA_FILE)
today_dt = date.today()
today_key = iso(today_dt)
daily = all_data.setdefault(today_key, {"goal": "", "tasks": [], "city": "Tokushima", "weather": {}})

# 読み込み
#df_ex = load_encrypted_csv(EXERCISE_CSV, fernet, columns=["date","minutes"])

render_weather_section(daily, today_dt)
st.write("---")
render_goal_tasks_section(daily, all_data, today_dt)
st.write("---")
render_daily_numeric_section("💓 メンタル", config.MENTAL_CSV, "mental", 0, 10, 1, 5)
st.write("---")
render_daily_numeric_section("💤 睡眠（時間）", config.SLEEP_CSV, "hours", 0.0, 24.0, 0.5, 7.0)
st.write("---")
render_daily_numeric_section("🏃‍♂️ 運動（分）", config.EXERCISE_CSV, "minutes", 0, 1440, 5, 0)
st.write("---")
render_daily_numeric_section("💊 セルフケア（分）", config.CARE_CSV, "minutes", 0, 1430, 5, 0)
st.write("---")

save_json(config.DATA_FILE, all_data)