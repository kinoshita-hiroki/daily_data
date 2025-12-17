import os
from datetime import datetime

import pandas as pd
import streamlit as st

import app.config.config as config
import app.config.training as training

# 保存先 CSV
CSV_PATH = config.WORKOUT_CSV


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

    menus = training.MENU_BY_DAY.get(weekday, [])
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


def aggregate_data(all_data):
    records = []


    for day, content in all_data.items():
        sucess = 0
        false = 0
        tasks = content.get("tasks", {})
        for task in tasks:
            if task["done"]:
                sucess = sucess + 1
            else:
                false = false + 1
        if (sucess+false) == 0:
            per = 0
        else:
            per = sucess/(sucess+false)
        records.append({
            "date": day,
            "done": sucess,
            "cant": false,
            "per": per
        })
    df = pd.DataFrame(records).sort_values("date")
    return df


def build_prompt(all_data) -> str:
    """
    先週のタスク記録から振り返り用レポートを生成するためのプロンプト
    """
    system_instruction = """
        あなたは、個人の行動記録を客観的に整理するアシスタントです。
        また、以下のルールを必ず守ってください。
        ・必ず日本語のみで回答してください。
        ・英語は一切使用しないでください。
        ・事実に基づいて要約して下さい。
    """

    data_section = "【過去のタスク記録】\n"
    prompt = (
        system_instruction
        + "\n\n"
        + data_section
        + str(all_data)
        + "\n\n"
        + "上記の記録をもとに、50字程度でタスクを日本語でまとめてください。"
    )
    return prompt


def llm(prompt):
    import requests

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3:8b",
        "prompt": prompt,
        "stream": False
    }

    res = requests.post(url, json=payload)
    return res.json()["response"]
