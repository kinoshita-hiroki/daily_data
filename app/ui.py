# --------------------------
# UI Helpers
# --------------------------
import os
from crypt.encrypt_utils import (
    get_fernet_from_env,
    load_encrypted_csv,
    save_encrypted_csv,
)
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

import app.config.config as config
from app.utils import append_or_update, iso, load_csv, load_json, save_csv, save_json
from app.weather_api import fetch_current_weather, fetch_forecast_noon


def load_key():
    load_dotenv()  # .env の読み込み

    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    return API_KEY

def get_fernet():
    fernet = get_fernet_from_env()
    if fernet is None:
        st.warning("データ暗号化キーが設定されていません。環境変数 FERNET_KEY を設定してください。")
        # ここで続行するか（非暗号化モード）止めるかはポリシー次第
    return fernet

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

def render_goal_tasks_section(data, all_data):
    st.subheader("❤️‍🔥 やりたいこと")
    feeling = st.text_input("今日一番大事にしたい気持ち", value=data.get("feeling", ""))
    data["feeling"] = feeling

    not_todo = st.text_input("今日やらないこと", value=data.get("not_todo", ""))
    data["not_todo"] = not_todo

    ideal_self = st.text_input("今日はどんな人でいたいか", value=data.get("ideal_self", ""))
    data["ideal_self"] = ideal_self

    st.subheader("🎯 タスク")
    tasks = data.setdefault("tasks", [])
    new_task = st.text_input("新しいタスクを追加", key="new_task_input")
    if st.button("追加", key="add_task_btn"):
        if new_task:
            tasks.append({"id": datetime.now().timestamp(), "name": new_task, "done": False})
            save_json(config.DATA_FILE, all_data)
            st.rerun()

    for  t in list(tasks):
        cols = st.columns([0.85, 0.15])
        task_id = t["id"]
        with cols[0]:
            done = st.checkbox(t["name"], value=t.get("done", False), key=f"task_chk_{task_id}")
            t["done"] = done
        with cols[1]:
            if st.button("🗑️", key=f"task_del_{task_id}"):
                tasks.remove(t)
                save_json(config.DATA_FILE, all_data)
                st.rerun()
    save_json(config.DATA_FILE, all_data)

def render_gastrointestinal_section(data, today):
    st.subheader("🩺 今日の体調")
    condition_map = {
        "□ 未定 ": "□",
        "◎ とても良い": "◎",
        "◯ 良い": "◯",
        "△ 普通": "△",
        "× 悪い": "×"
    }

    # 既存値があればそれを初期値に
    current = data[str(today)].get("condition", "□")

    reverse_map = {v: k for k, v in condition_map.items()}
    default_label = reverse_map.get(current, "□ 未定")

    selected = st.radio(
        "今日の体調を選んでください",
        options=list(condition_map.keys()),
        index=list(condition_map.keys()).index(default_label)
    )

    data[str(today)]["condition"] = condition_map[selected]
    save_json(config.DATA_FILE, data)



def render_everyday_checklist_section(check_items):
    today = date.today().isoformat()

    # 仮データ
    data = load_json(config.EVERY_DAY_CHECK_PATH)  # なければ {}

    # 今日のデータを初期化（前日引き継ぎ）
    if today not in data:
        data[today] = {item: False for item in check_items}

    st.subheader("1日1回でも出来ればおｋ！")

    for item in check_items:
        data[today][item] = st.checkbox(
            item,
            value=data[today].get(item, False),
            key=f"{today}_{item}"
        )

    save_json(config.EVERY_DAY_CHECK_PATH, data)


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
            save_csv(df, csv_path)
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
            save_csv(df, csv_path)
            st.success("記録しました")
            st.rerun()

def render_daily_numeric_float_section(title, csv_path, column_name, min_val, max_val, step, default, format="%.1f"):
    st.subheader(title)

    df = load_csv(csv_path, ["date", column_name])
    today = iso(date.today())

    if today in df["date"].values:
        current = float(df.loc[df["date"] == today, column_name].values[0])
        st.info(f"本日の記録あり: {current}")

        new_val = st.number_input(
            "修正する場合",
            min_value=float(min_val),
            max_value=float(max_val),
            value=current,
            step=float(step),
            format=format
        )

        if st.button(f"更新 ({title})"):
            df = append_or_update(df, today, column_name, new_val)
            save_csv(df, csv_path)
            st.success("更新しました")
            st.rerun()
    else:
        val = st.number_input(
            f"{title}を記録",
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(default),
            step=float(step),
            format=format
        )

        if st.button(f"記録する ({title})"):
            df = append_or_update(df, today, column_name, val)
            save_csv(df, csv_path)
            st.success("記録しました")
            st.rerun()

def render_rpg_section(log_csv):
    st.subheader("📖 日誌")
    try:
        df = load_csv(log_csv, ["date", "character", "exp", "note"])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "character", "exp", "note"])
    with st.form("daily_exp_form"):
        today = date.today().isoformat()
        character = st.selectbox(
            "対象",
            ["勇者", "戦士", "魔法使い", "僧侶"]
        )

        exp = st.number_input(
            "獲得経験値",
            min_value=0,
            max_value=10,
            step=1
        )

        note = st.text_area(
            "記録",
            placeholder="例：資料作成、30分運動、コードのリファクタリング"
        )
        submitted = st.form_submit_button("経験値を記録")
        if submitted:
            df = pd.concat([df, pd.DataFrame([[today, character, exp, note]], columns=df.columns)])
            save_csv(df, log_csv)
            st.success(f"✨ {character}の経験値が {exp} 増えた！")
            st.rerun()

def render_feeling_regist():
    fernet = get_fernet()
    try:
    # CSV 読み込み例（運動）
        df = load_encrypted_csv(config.ENCRYPT_SENTIMENT_CSV, fernet, columns=["日付", "対象", "事実", "感情", "詳細感情", "感想", "対処法"])
    except Exception:
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
    except Exception:
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
