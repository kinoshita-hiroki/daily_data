import os
from datetime import datetime

import pandas as pd
import streamlit as st

import app.config as config
from app.ui import render_top_image_base64

# === 1. 曜日ごとのメニュー ===
circuit = [
    {"name": "スクワット", "sets": 2, "detail": "12~15"},
    {"name": "ベンチプレス", "sets": 2, "detail": "12~15"},
    {"name": "ローイング", "sets": 2, "detail": "10~12"},
    {"name": "デットリフト", "sets": 2, "detail": "12~15"},
    {"name": "ランジ", "sets": 2, "detail": "12~15"},
    {"name": "アームカール", "sets": 2, "detail": "12~15"},
    {"name": "ダンベルカーフレイズ", "sets": 2, "detail": "12~15"},
    {"name": "ダンベル腹筋", "sets": 2, "detail": "10~15"},
    {"name": "ショルダープレス", "sets": 2, "detail": "12~15"},
    {"name": "ヒップスラスト", "sets": 2, "detail": "12~15"},
]
yoga = [
    {"name": "ダウンドッグ", "sets": 1, "detail": "5呼吸"},
    {"name": "木のポーズ", "sets": 1, "detail": "5呼吸"},
    {"name": "片足前屈", "sets": 1, "detail": "5呼吸"},
    {"name": "英雄1のポーズ", "sets": 1, "detail": "5呼吸"},
    {"name": "シャバアーサナ", "sets": 1, "detail": "5呼吸"},
]
rest = [{"name": "瞑想", "sets": 1, "detail": "5分程度"}]
jump = [{"name": "なわとび", "sets": 4, "detail": "150回"}]

MENU_BY_DAY = {
    "Monday": circuit,
    "Tuesday": rest,
    "Wednesday": jump,
    "Thursday": rest,
    "Friday": circuit,
    "Saturday": rest,
    "Sunday": yoga,
}

# 保存先 CSV
CSV_PATH = "logs/workout_log.csv"


# ===== CSV 初期化 =====
def init_csv():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=["date", "weekday", "menu", "set_number", "done"])
        df.to_csv(CSV_PATH, index=False)


# ===== 今日のチェック状態を読み込む =====
def load_today_status(date_str):
    if not os.path.exists(CSV_PATH):
        return {}

    df = pd.read_csv(CSV_PATH)
    df_today = df[df["date"] == date_str]

    # key: "メニュー名-セット番号" → True/False
    status = {}
    for _, row in df_today.iterrows():
        key = f"{row['menu']}-set{int(row['set_number'])}"
        status[key] = bool(row["done"])

    return status


# ===== 状態保存（上書き） =====
def save_results(date_str, weekday, results_list):
    df = pd.read_csv(CSV_PATH)

    # ----- ① 指定日付のデータを削除（上書きのため） -----
    df = df[df["date"] != date_str]

    # ----- ② 新しいデータを作成 -----
    new_rows = []
    for r in results_list:
        new_rows.append({
            "date": date_str,
            "weekday": weekday,
            "menu": r["menu"],
            "set_number": r["set_number"],
            "done": int(r["done"]),
        })

    # ----- ③ 結合して保存 -----
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)


# ===== UI 描画 =====
def render_workout_checklist():
    st.header("📋 今日のトレーニングチェックリスト")

    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    weekday = today.strftime("%A")

    st.subheader(f"🗓️ {date_str}（{weekday}）")

    menus = MENU_BY_DAY.get(weekday, [])
    if not menus:
        st.info("今日は特にメニューがありません。")
        return

    # --------- 初期状態読み込み（永続化） ---------
    init_csv()
    today_status = load_today_status(date_str)

    results_list = []

    for menu in menus:
        name = menu["name"]
        sets = menu.get("sets", 1)
        detail = menu.get("detail")

        title = f"### {name}"
        if detail:
            title += f"（{detail}）"
        if sets > 1:
            title += f" × {sets}セット"

        st.markdown(title)

        # セットごとにチェックボックス作成
        for i in range(1, sets + 1):
            key = f"{name}-set{i}"

            # 今日の保存された状態を初期値として設定
            default = today_status.get(key, False)

            done = st.checkbox(f"セット {i}", key=f"{date_str}-{key}", value=default)

            results_list.append({
                "menu": name,
                "set_number": i,
                "done": done
            })

        st.write("---")

    # 保存
    if st.button("📁 今日の結果を保存する"):
        save_results(date_str, weekday, results_list)
        st.success("保存しました！（アプリ再起動後も状態が保持されます）")


# ========== 描画 ==========
render_top_image_base64(config.TOP_IMAGE_PATH3)
render_workout_checklist()
