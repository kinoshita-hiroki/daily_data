# app_refactor_base64_topimage.py
from datetime import date

import streamlit as st

import app.config.config as config
from app.ui import (
    render_daily_numeric_section,
    render_diary_section,
    render_goal_tasks_section,
    render_rpg_section,
    render_top_image_base64,
)
from app.utils import iso, load_json

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

st.write("---")
render_goal_tasks_section(daily, all_data)
st.write("---")
render_daily_numeric_section("💓 メンタル", config.MENTAL_CSV, "mental", 0, 10, 1, 5)
st.write("---")
render_daily_numeric_section("👨‍⚕️ 体調", config.CONDITION_CSV, "condition", 0, 10, 2, 2)
st.write("---")
render_daily_numeric_section("✍ 勉強時間", config.STUDY_TIME_CSV, "study_time", 0, 600, 15, 0)
st.write("---")
activity_type = st.radio("Activity", ["瞑想", "ヨガ"], horizontal=True, label_visibility="collapsed")
if activity_type == "瞑想":
    render_daily_numeric_section("🧘 瞑想・写経", config.MEDITATION_CSV, "meditation", 0, 120, 5, 0)
else:
    render_daily_numeric_section("🧘 ヨガ", config.YOGA_CSV, "yoga", 0, 120, 5, 0)
st.write("---")
render_diary_section(config.ENCRYPT_DIARY_CSV)
st.write("---")
