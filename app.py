# app_refactor_base64_topimage.py
from datetime import date

import streamlit as st

import app.config.config as config
import app.config.training as training
from app.ui import (
    render_daily_numeric_section,
    render_everyday_checklist_section,
    render_goal_tasks_section,
    render_rpg_section,
    render_top_image_base64,
    render_weather_section,
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

render_weather_section(daily, today_dt)
st.write("---")
render_goal_tasks_section(daily, all_data)
st.write("---")
render_everyday_checklist_section(training.EVERY_DAY_CHECKLIST)
st.write("---")
render_daily_numeric_section("💓 メンタル", config.MENTAL_CSV, "mental", 0, 10, 1, 5)
st.write("---")
render_daily_numeric_section("💤 睡眠（時間）", config.SLEEP_CSV, "hours", 0.0, 24.0, 0.5, 7.0)
st.write("---")
render_rpg_section(config.RPG_EX_CSV)
st.write("---")
