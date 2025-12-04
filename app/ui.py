# --------------------------
# UI Helpers
# --------------------------
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
import os

import app.config as config
from app.weather_api import fetch_current_weather, fetch_forecast_noon
from datetime import date, datetime, timedelta
from app.utils import load_json, load_csv, iso, save_json,save_csv, append_or_update, iso
import pandas as pd
from crypt.encrypt_utils import save_encrypted_csv, load_encrypted_csv, get_fernet_from_env
import random

def load_key():
    load_dotenv()  # .env の読み込み

    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    return API_KEY

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
    saved_data = load_json(config.DATA_FILE)
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
            save_json(config.DATA_FILE, all_data)
            st.rerun()

    for idx, t in enumerate(list(tasks)):
        cols = st.columns([0.85, 0.15])
        with cols[0]:
            done = st.checkbox(t["name"], value=t.get("done", False), key=f"task_chk_{idx}")
            tasks[idx]["done"] = done
        with cols[1]:
            if st.button("🗑️", key=f"task_del_{idx}"):
                tasks.pop(idx)
                save_json(config.DATA_FILE, all_data)
                st.rerun()

def render_daily_numeric_section(title, csv_path, column_name, min_val, max_val, step, default):
    st.subheader(title)

    df = load_csv(csv_path, ["date", column_name])
    today = iso(date.today())

    if today in df["date"].values:
        current = df.loc[df["date"] == today, column_name].values[0]
        st.info(f"本日の記録あり: {current}")

        new_val = st.number_input(
            "修正する場合",
            min_value=min_val,
            max_value=max_val,
            value=type(default)(current),
            step=step
        )

        if st.button(f"更新 ({title})"):
            df = append_or_update(df, today, column_name, new_val)
            df.to_csv(csv_path, index=False)
            st.success("更新しました")
            st.rerun()
    else:
        val = st.number_input(
            f"{title}を記録",
            min_value=min_val,
            max_value=max_val,
            value=default,
            step=step
        )

        if st.button(f"記録する ({title})"):
            df = append_or_update(df, today, column_name, val)
            df.to_csv(csv_path, index=False)
            st.success("記録しました")
            st.rerun()
def get_fernet():
    fernet = get_fernet_from_env()
    if fernet is None:
        st.warning("データ暗号化キーが設定されていません。環境変数 FERNET_KEY を設定してください。")
        # ここで続行するか（非暗号化モード）止めるかはポリシー次第
    return fernet

def render_feeling_regist():
    fernet = get_fernet()
    try:
    # CSV 読み込み例（運動）
        df = load_encrypted_csv(config.ENCRYPT_SENTIMENT_CSV, fernet, columns=["日付", "対象", "事実", "感情", "詳細感情", "感想", "対処法"])
    except Exception as e:
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
            # 保存
            save_encrypted_csv(config.ENCRYPT_SENTIMENT_CSV, df, fernet)
            st.success("記録しました！")

def render_observation_regist():
    observation_columns = ["日付", "対象", "事実", "感情", "洞察", "対処法"]
    fernet = get_fernet()
    try:
    # CSV 読み込み例（運動）
        df = load_encrypted_csv(config.ENCRYPT_OBSERVATION_CSV, fernet, columns=observation_columns)
    except Exception as e:
        df = pd.DataFrame(columns=observation_columns)

    st.subheader("👀 観察の記録")

    with st.form("記録フォーム"):
        date = st.date_input("日付", datetime.today())
        obj = st.text_input("対象", key="obj")
        fact = st.text_area("事実", key="fact")
        sentiment = st.selectbox("自分の感情（任意）", ["", "ポジティブ", "ニュートラル", "ネガティブ"], key="sentiment")
        insight = st.text_area("洞察", key="insight")
        solution = st.text_area("対処法", key="solution")
        
        submitted = st.form_submit_button("記録する")
                
        
        if submitted:
            df = pd.concat([df, pd.DataFrame([[date, obj, fact, sentiment, insight, solution]], columns=df.columns)])
            # 保存
            save_encrypted_csv(config.ENCRYPT_OBSERVATION_CSV, df, fernet)
            st.success("記録しました！")
            
API_KEY = load_key()