import os
from datetime import datetime

import pandas as pd
import streamlit as st

# === 1. 曜日ごとのメニュー ===
circuit = [
        {"name": "スクワット", "sets": 2, "detail": "12~15"},
        {"name": "ベンチプレス", "sets": 2, "detail": "12~15"},
        {"name": "ローイング", "sets": 2, "detail": "10~12"},
        {"name": "デットリフト", "sets": 2, "detail": "12~15"},
        {"name": "ランジ", "sets": 2, "detail": "12~15"},
        {"name": "プランク", "sets": 2, "detail": "30秒"},
        {"name": "ヒップリフト", "sets": 2, "detail": "12~15"},
        ]
#yoga = ["キャット＆カウ", "ダウンドッグ", "三角ポーズ", "ウォーリアII", "プランク", "チェア", "ツイストチェア", "ハーフムーン", "ダウンドッグ", "片足前屈", "シャバアーサナ"]
yoga = [
        {"name": "キャット＆カウ", "sets": 1, "detail": "5呼吸"},
        {"name": "ダウンドッグ", "sets": 1, "detail": "5呼吸"},
        {"name": "三角ポーズ", "sets": 1, "detail": "5呼吸"},
        {"name": "ウォーリアII", "sets": 1, "detail": "5呼吸"},
        {"name": "プランク", "sets": 1, "detail": "5呼吸"},
        {"name": "チェア", "sets": 1, "detail": "5呼吸"},
        {"name": "ツイストチェア", "sets": 1, "detail": "5呼吸"},
        {"name": "ハーフムーン", "sets": 1, "detail": "5呼吸"},
        {"name": "片足前屈", "sets": 1, "detail": "5呼吸"},
        {"name": "シャバアーサナ", "sets": 1, "detail": "5呼吸"},
        ]
rest = [[{"name": "軽めのストレッチ・瞑想", "sets": 1, "detail": "15分程度"}]]
jump = [{"name": "なわとび", "sets": 4, "detail": "200回"}]
MENU_BY_DAY = {
    "Monday": circuit,
    "Tuesday": rest,
    "Wednesday": yoga,
    "Thursday": rest,
    "Friday": circuit,
    "Saturday": rest,
    "Sunday": jump
}

# 保存先 CSV
CSV_PATH = "logs/workout_log.csv"


# # === 2. CSV がなければ初期化 ===
# def init_csv():
#     if not os.path.exists(CSV_PATH):
#         df = pd.DataFrame(columns=["date", "weekday", "menu", "done"])
#         df.to_csv(CSV_PATH, index=False)


# # === 3. 保存処理 ===
# def save_result(date_str, weekday, results):
#     """
#     results: dict { "なわとび..." : True/False }
#     """
#     df = pd.read_csv(CSV_PATH)

#     new_rows = []
#     for menu, done in results.items():
#         new_rows.append({
#             "date": date_str,
#             "weekday": weekday,
#             "menu": menu,
#             "done": int(done),
#         })

#     df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
#     df.to_csv(CSV_PATH, index=False)


# # === 4. UI 描画部分 ===
# def render_workout_checklist():
#     st.header("📋 今日の筋トレチェックリスト")

#     # 今日の情報取得
#     today = datetime.now()
#     date_str = today.strftime("%Y-%m-%d")
#     weekday = today.strftime("%A")

#     st.subheader(f"🗓️ {date_str}（{weekday}）")

#     menus = MENU_BY_DAY.get(weekday, [])
#     if not menus:
#         st.info("今日はメニューがありません。")
#         return

#     # チェック UI
#     st.write("### ✔ トレーニング項目")
#     results = {}
#     for m in menus:
#         key = f"{date_str}-{m}"
#         results[m] = st.checkbox(m, key=key)

#     st.write("---")

#     # 保存ボタン
#     if st.button("📁 今日の結果を保存する"):
#         init_csv()
#         save_result(date_str, weekday, results)
#         st.success("保存しました！")

# render_workout_checklist()



# ===== CSV 初期化 =====
def init_csv():
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=["date", "weekday", "menu", "set_number", "done"])
        df.to_csv(CSV_PATH, index=False)

# ===== 保存 =====
# def save_results(date_str, weekday, results_list):
#     """
#     results_list = [
#         {"menu": "なわとび", "set_number": 1, "done": True },
#         ...
#     ]
#     """
#     df = pd.read_csv(CSV_PATH)
#     new_rows = []

#     for r in results_list:
#         new_rows.append({
#             "date": date_str,
#             "weekday": weekday,
#             "menu": r["menu"],
#             "set_number": r["set_number"],
#             "done": int(r["done"]),
#         })

#     df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
#     df.to_csv(CSV_PATH, index=False)
def save_results(date_str, weekday, results_list):
    """
    results_list = [
        {"menu": "なわとび", "set_number": 1, "done": True },
        ...
    ]
    """
    df = pd.read_csv(CSV_PATH)

    # ----- ① 指定日付のデータを削除（上書き用） -----
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

    # ----- ③ 結合 -----
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

    # ----- ④ 保存 -----
    df.to_csv(CSV_PATH, index=False)



# ===== UI 描画 =====
def render_workout_checklist():
    st.header("📋 今日の筋トレチェックリスト")

    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    weekday = today.strftime("%A")

    st.subheader(f"🗓️ {date_str}（{weekday}）")

    menus = MENU_BY_DAY.get(weekday, [])
    if not menus:
        st.info("今日は特にメニューがありません。")
        return

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

        # セット数分のチェックボックス生成
        for i in range(1, sets + 1):
            key = f"{date_str}-{name}-set{i}"
            done = st.checkbox(f"セット {i}", key=key)

            results_list.append({
                "menu": name,
                "set_number": i,
                "done": done
            })

        st.write("---")

    # 保存
    if st.button("📁 今日の結果を保存する"):
        init_csv()
        save_results(date_str, weekday, results_list)
        st.success("保存しました！")
render_workout_checklist()
