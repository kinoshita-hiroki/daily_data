# --------------------------
# UI Helpers
# --------------------------
from crypt.encrypt_utils import (
    get_fernet_from_env,
    load_encrypted_csv,
    save_encrypted_csv,
)
from datetime import date, datetime

import pandas as pd
import streamlit as st
from PIL import Image

import app.config.config as config
from app.utils import append_or_update, iso, load_csv, save_csv, save_json


def get_fernet():
    fernet = get_fernet_from_env()
    if fernet is None:
        st.warning("データ暗号化キーが設定されていません。環境変数 FERNET_KEY を設定してください。")
    return fernet

def render_top_image_base64(path):
    # 画像を開く
    img = Image.open(path)  # ← 画像ファイル名

    # トップに表示
    st.image(img, width='stretch')  # 画面幅に合わせて自動調整

def render_goal_tasks_section(data, all_data):
    st.subheader("❤️‍🔥 やりたいこと")

    ideal_self = st.text_input("今日はどんな人でいたいか", value=data.get("ideal_self", ""))
    data["ideal_self"] = ideal_self

    not_todo = st.text_input("今日やらないこと", value=data.get("not_todo", ""))
    data["not_todo"] = not_todo

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

