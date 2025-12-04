from app.ui import render_daily_numeric_section, render_top_image_base64
import streamlit as st
import app.config as config

render_top_image_base64(config.TOP_IMAGE_PATH5)
st.title("👩‍⚕️ 定期検診")

render_daily_numeric_section("📉 体重", config.WEIGHT_CSV, "weight", 0, 100, 1, 60)
render_daily_numeric_section("⛔ ハーディネスの記録", config.HARDINESS_CSV, "hardiness", 0, 50, 1, 5)
render_daily_numeric_section("💤 セルフケアの記録", config.SELF_CARE_CSV, "self_care", 0, 20, 1, 1)
render_daily_numeric_section("🗣️ ヒューマンスキル記録", config.HUMAN_SKILL_CSV, "human_skill", 0, 50, 1, 5)
