# app_refactor_base64_topimage.py
import os
import json
import requests
from datetime import date, datetime, timedelta
import base64

import streamlit as st
import pandas as pd
from PIL import Image

import os
from dotenv import load_dotenv

# --------------------------
# Config / Constants
# --------------------------
DATA_FILE = "daily_data.json"
MENTAL_CSV = "mental_logs.csv"
EXERCISE_CSV = "exercise_logs.csv"
SLEEP_CSV = "sleep_logs.csv"

TOP_IMAGE_PATH = "reimu.jpeg"
TOP_IMAGE_MAX_HEIGHT = 160  # px
FEEL_PATH = "feelings.json"

# --------------------------
# Utility Functions
# --------------------------
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def load_csv(path, columns):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame(columns=columns)

def save_csv(df, path):
    df.to_csv(path, index=False)

def iso(d: date):
    return d.isoformat()

def load_feelings():
    try:
        with open(FEEL_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def save_feelings(data):
    with open(FEEL_PATH, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --------------------------
# Weather API
# --------------------------
def load_key():
    load_dotenv()  # .env の読み込み

    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    SECRET = os.getenv("SECRET_KEY")

def fetch_current_weather(city: str, api_key: str):
    if not api_key:
        return None
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ja"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        d = r.json()
        return {"desc": d["weather"][0]["description"], "temp": d["main"]["temp"], "icon": d["weather"][0]["icon"]}
    except Exception:
        return None

def fetch_forecast_noon(city: str, api_key: str):
    if not api_key:
        return {}
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ja"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        forecasts = {}
        for entry in data.get("list", []):
            dt = datetime.fromtimestamp(entry["dt"])
            if dt.hour == 12:
                forecasts[dt.date().isoformat()] = {
                    "desc": entry["weather"][0]["description"],
                    "temp": entry["main"]["temp"],
                    "icon": entry["weather"][0]["icon"]
                }
        return forecasts
    except Exception:
        return {}


# --------------------------
# UI Helpers
# --------------------------
def render_top_image_base64(path):
    # 画像を開く
    img = Image.open(path)  # ← 画像ファイル名

    # トップに表示
    st.image(img, width='stretch')  # 画面幅に合わせて自動調整

def render_weather_section(data, today):
    st.subheader("🌤 天気（昨日・今日・明日）")
    city = st.text_input("都市名（例: Tokyo, Osaka）", value=data.get("city", "Tokushima"))
    data["city"] = city

    if not API_KEY:
        st.warning("天気表示には OpenWeatherMap API KEY が必要です")
        return

    today_weather = fetch_current_weather(city, API_KEY)
    forecast = fetch_forecast_noon(city, API_KEY)

    day_dict = data.setdefault("weather", {})
    if today_weather:
        day_dict[iso(today)] = today_weather
    tom_iso = iso(today + timedelta(days=1))
    if tom_iso in forecast:
        day_dict[tom_iso] = forecast[tom_iso]

    y_iso = iso(today - timedelta(days=1))
    y_weather = None
    saved_data = load_json(DATA_FILE)
    if y_iso in saved_data:
        y_weather = saved_data[y_iso].get("weather", {}).get(y_iso)

    cols = st.columns(3)
    labels = [("昨日", y_iso, y_weather), ("今日", iso(today), day_dict.get(iso(today))), ("明日", tom_iso, day_dict.get(tom_iso))]
    for col, (label, d_iso, info) in zip(cols, labels):
        with col:
            st.markdown(f"**{label}**")
            if info:
                st.image(f"http://openweathermap.org/img/wn/{info['icon']}.png", width=64)
                st.write(f"{info['desc']} / {info['temp']} ℃")
            else:
                st.write("データなし")

def render_goal_tasks_section(data, all_data, today):
    st.subheader("🎯 目標・タスク")
    goal = st.text_input("今日の目標", value=data.get("goal", ""))
    data["goal"] = goal

    tasks = data.setdefault("tasks", [])
    new_task = st.text_input("新しいタスクを追加", key="new_task_input")
    if st.button("追加", key="add_task_btn"):
        if new_task:
            tasks.append({"id": datetime.now().timestamp(), "name": new_task, "done": False})
            save_json(DATA_FILE, all_data)
            st.rerun()

    for idx, t in enumerate(list(tasks)):
        cols = st.columns([0.85, 0.15])
        with cols[0]:
            done = st.checkbox(t["name"], value=t.get("done", False), key=f"task_chk_{idx}")
            tasks[idx]["done"] = done
        with cols[1]:
            if st.button("🗑️", key=f"task_del_{idx}"):
                tasks.pop(idx)
                save_json(DATA_FILE, all_data)
                st.rerun()

def render_mental_section():
    st.subheader("💓 メンタル状態（0〜10）")
    df_m = load_csv(MENTAL_CSV, ["date", "mental"])
    today_iso = iso(date.today())

    if today_iso in df_m["date"].values:
        today_val = int(df_m.loc[df_m["date"] == today_iso, "mental"].values[0])
        st.info(f"本日の記録あり（{today_val}）")
        val = st.slider("修正する場合", 0, 10, value=today_val, key="mental_edit")
        if st.button("更新（メンタル）"):
            df_m.loc[df_m["date"] == today_iso, "mental"] = int(val)
            save_csv(df_m, MENTAL_CSV)
            st.success("更新しました")
            st.rerun()
    else:
        val = st.slider("今日の精神状態を選択", 0, 10, 5, key="mental_new")
        if st.button("記録する（メンタル）"):
            new = pd.DataFrame([{"date": today_iso, "mental": int(val)}])
            df_m = pd.concat([df_m, new], ignore_index=True)
            save_csv(df_m, MENTAL_CSV)
            st.success("記録しました")
            st.rerun()

def render_exercise_section():
    st.subheader("🏃‍♂️ 運動（分）")
    df_ex = load_csv(EXERCISE_CSV, ["date", "minutes"])
    today_iso = iso(date.today())

    if today_iso in df_ex["date"].values:
        cur = int(df_ex.loc[df_ex["date"] == today_iso, "minutes"].values[0])
        st.info(f"本日の運動記録あり（{cur} 分）")
        new_min = st.number_input("修正（分）", min_value=0, max_value=1440, value=cur, step=5, key="ex_edit")
        if st.button("更新（運動）"):
            df_ex.loc[df_ex["date"] == today_iso, "minutes"] = int(new_min)
            save_csv(df_ex, EXERCISE_CSV)
            st.success("更新しました")
            st.rerun()
    else:
        minutes = st.number_input("今日の運動時間（分）", min_value=0, max_value=1440, value=0, step=5, key="ex_new")
        if st.button("記録する（運動）"):
            new = pd.DataFrame([{"date": today_iso, "minutes": int(minutes)}])
            df_ex = pd.concat([df_ex, new], ignore_index=True)
            save_csv(df_ex, EXERCISE_CSV)
            st.success("記録しました")
            st.rerun()

def render_sleep_section():
    st.subheader("💤 睡眠（時間）")
    df_sl = load_csv(SLEEP_CSV, ["date", "hours"])
    today_iso = iso(date.today())

    if today_iso in df_sl["date"].values:
        cur = float(df_sl.loc[df_sl["date"] == today_iso, "hours"].values[0])
        st.info(f"本日の睡眠記録あり（{cur} 時間）")
        new_h = st.number_input("修正（時間）", min_value=0.0, max_value=24.0, value=cur, step=0.5, key="sl_edit")
        if st.button("更新（睡眠）"):
            df_sl.loc[df_sl["date"] == today_iso, "hours"] = float(new_h)
            save_csv(df_sl, SLEEP_CSV)
            st.success("更新しました")
            st.rerun()
    else:
        hours = st.number_input("昨晩の睡眠時間（時間）", min_value=0.0, max_value=24.0, value=7.0, step=0.5, key="sl_new")
        if st.button("記録する（睡眠）"):
            new = pd.DataFrame([{"date": today_iso, "hours": float(hours)}])
            df_sl = pd.concat([df_sl, new], ignore_index=True)
            save_csv(df_sl, SLEEP_CSV)
            st.success("記録しました")
            st.rerun()

def render_feeling_regist():

    try:
        df = pd.read_csv("sentiment_log.csv")
    except:
        df = pd.DataFrame(columns=["日付", "対象", "事実", "感情", "詳細感情", "感想", "対処法"])

    st.subheader("💞 感情の記録")

    with st.form("記録フォーム"):
        date = st.date_input("日付", datetime.today())
        obj = st.text_input("対象", key="obj")
        fact = st.text_area("事実", key="fact")
        sentiment = st.selectbox("自分の感情（任意）", ["", "ポジティブ", "ニュートラル", "ネガティブ"], key="sentiment")
        tag = st.text_input("詳細感情", key="tag")
        feeling = st.text_area("どう感じた", key="feeling")
        solution = st.text_area("対処法", key="solution")
        
        submitted = st.form_submit_button("記録する")
                
        
        if submitted:
            df = pd.concat([df, pd.DataFrame([[date, obj, fact, sentiment, tag, feeling, solution]], columns=df.columns)])
            df.to_csv("sentiment_log.csv", index=False)
            st.success("記録しました！")
            

# --------------------------
# Main App
# --------------------------

# トップ画像表示（Base64埋め込み・縦幅固定）
render_top_image_base64(TOP_IMAGE_PATH)

st.title("🤐 My Daily Board")

load_key()
all_data = load_json(DATA_FILE)
today_dt = date.today()
today_key = iso(today_dt)
daily = all_data.setdefault(today_key, {"goal": "", "tasks": [], "memo": "", "city": "Tokushima", "weather": {}})


render_weather_section(daily, today_dt)
st.write("---")
render_goal_tasks_section(daily, all_data, today_dt)
st.write("---")

render_sleep_section()
st.write("---")
render_mental_section()
st.write("---")
render_exercise_section()
st.write("---")
render_feeling_regist()


save_json(DATA_FILE, all_data)