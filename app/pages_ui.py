import os
from datetime import datetime

import altair as alt
import pandas as pd
import streamlit as st

import app.config.config as config
import app.config.training as training
from app.ui import (
    render_daily_numeric_float_section,
    render_daily_numeric_section,
)
from app.utils import load_json
from game.rpg_ui import (
    render_command,
    render_enemy_state,
    render_level_up,
    render_log,
    render_party_state,
)
from game.session_state import init_state

# 保存先 CSV
CSV_PATH = config.WORKOUT_CSV


# ===== CSV 初期化 =====
def init_csv():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=["date", "weekday", "category", "menu", "set_number", "done"])
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
            "category": r.get("category", "General"),
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

    # メニューが dict ならカテゴリ分け、list なら従来のフラットリスト（カテゴリ="General"）
    if isinstance(menus, dict):
        menu_items_with_category = []
        for category, items in menus.items():
            for item in items:
                # 辞書型などオブジェクトをコピーして category を付与するか、タプルで扱う
                # ここでは単純にループ処理を回す
                menu_items_with_category.append((category, item))
    else:
        # 従来のリスト形式
        menu_items_with_category = [("General", item) for item in menus]

    # カテゴリごとにヘッダーを出し分けるための制御
    current_category = None

    for category, menu in menu_items_with_category:
        # カテゴリが変わったらヘッダーを表示 (General以外、もしくは区切りが必要なら)
        if category != current_category:
            if category != "General":
                st.markdown(f"## {category}")
            current_category = category

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
                "category": category,
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
    # 7日間移動平均の計算を追加
    df["done_ma"] = df["done"].rolling(window=7, min_periods=1).mean()
    return df


def render_self_check_page():
    st.title("👩‍⚕️ 定期検診")

    render_daily_numeric_float_section("📉 体重", config.WEIGHT_CSV, "weight", 0, 100, 1, 60)
    render_daily_numeric_section("⛔ ハーディネスの記録", config.HARDINESS_CSV, "hardiness", 0, 50, 1, 20)
    # render_daily_numeric_section("💤 セルフケアの記録", config.SELF_CARE_CSV, "self_care", 0, 20, 1, 15)
    render_daily_numeric_section("🗣️ ヒューマンスキル記録", config.HUMAN_SKILL_CSV, "human_skill", 0, 55, 1, 30)
    render_daily_numeric_section("🗨️ 境界線の記録", config.BOUNDARY_CSV, "boundary", 0, 5, 1, 5)

def fill_missing_dates(df, date_col, value_col, fill_value=0):
    """
    日付の欠損を埋めるヘルパー関数
    """
    if df.empty:
        return df
    df[date_col] = pd.to_datetime(df[date_col])
    min_date = df[date_col].min()
    max_date = datetime.now()
    all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
    df = df.set_index(date_col).reindex(all_dates).fillna(fill_value).reset_index()
    df.columns = [date_col, value_col]
    return df


def render_report_page():
    all_data = load_json(config.DATA_FILE)
    df = aggregate_data(all_data)
    st.subheader("過去のタスク達成数")
    # Altairを使用して棒グラフと折れ線グラフを重ねる
    base = alt.Chart(df).encode(x=alt.X('date:T', title='日付'))
    
    bar = base.mark_bar(color='lightblue', opacity=0.7).encode(
        y=alt.Y('done:Q', title='達成数')
    )
    
    line = base.mark_line(color='green', strokeWidth=3).encode(
        y=alt.Y('done_ma:Q', title='達成数')
    )
    
    chart_task = (bar + line).interactive()
    st.altair_chart(chart_task, use_container_width=True)
    df_mental = pd.read_csv(config.MENTAL_CSV)
    st.subheader("メンタルログ")
    df_mental["mental_ma"] = df_mental["mental"].rolling(window=7, min_periods=1).mean()
    st.line_chart(
        df_mental.set_index("date")[["mental", "mental_ma"]]
    )

    st.subheader("体調ログ")
    df_condition = pd.read_csv(config.CONDITION_CSV)
    df_condition["condition_ma"] = df_condition["condition"].rolling(window=7, min_periods=1).mean()
    st.line_chart(
        df_condition.set_index("date")[["condition", "condition_ma"]]
    )

    st.subheader("体重推移")
    df_weight = pd.read_csv(config.WEIGHT_CSV)
    chart_weight = alt.Chart(df_weight).mark_line(point=True).encode(
        x=alt.X('date:T', title='日付'),
        y=alt.Y('weight:Q', scale=alt.Scale(domain=[60, 70]), title='体重 (kg)')
    ).interactive()
    st.altair_chart(chart_weight, width="stretch")

    # st.subheader("ハーディネス（精神的弾力性）")
    # df_hardiness = pd.read_csv(config.HARDINESS_CSV)
    # st.line_chart(df_hardiness.set_index("date")["hardiness"])

    st.subheader("ヒューマンスキル")
    df_human_skill = pd.read_csv(config.HUMAN_SKILL_CSV)
    st.line_chart(df_human_skill.set_index("date")["human_skill"])

    st.subheader("✍ 勉強時間（分）")
    try:
        df_study = pd.read_csv(config.STUDY_TIME_CSV)
        df_study = fill_missing_dates(df_study, "date", "study_time")
        st.bar_chart(df_study.set_index("date")["study_time"])
    except FileNotFoundError:
        st.info("データがありません")

    st.subheader("🧘 瞑想・写経（分）")
    df_meditation = pd.read_csv(config.MEDITATION_CSV)
    df_meditation = fill_missing_dates(df_meditation, "date", "meditation")
    st.bar_chart(df_meditation.set_index("date")["meditation"])

    st.subheader("🧘‍♀️ ヨガ（分）")
    df_yoga = pd.read_csv(config.YOGA_CSV)
    df_yoga = fill_missing_dates(df_yoga, "date", "yoga")
    st.bar_chart(df_yoga.set_index("date")["yoga"])

    st.subheader("ワークアウト種目別達成数")
    df_workout = pd.read_csv(config.WORKOUT_CSV)
    df_workout = df_workout.loc[df_workout["category"] == "戦士"]
    # 種目ごとにdoneの合計を集計
    df_workout_stats = df_workout.groupby("menu")["done"].sum().reset_index()
    # 降順でソートして表示
    df_workout_stats = df_workout_stats.sort_values(by="done", ascending=False)

    chart_workout = alt.Chart(df_workout_stats).mark_bar().encode(
        x=alt.X('done:Q', title='達成セット数'),
        y=alt.Y('menu:N', sort='-x', title='種目'),
        color=alt.Color('done:Q', scale=alt.Scale(scheme='greens'))
    ).interactive()
    st.altair_chart(chart_workout, width="stretch")


def render_rpg_page():
    st.title("⚔️ 4人パーティバトル")

    # 初期化
    init_state()

    battle = st.session_state.battle

    render_enemy_state(battle)
    st.divider()
    render_party_state(battle)
    st.divider()
    render_command(battle)
    st.divider()
    render_log(battle)
    st.divider()
    render_level_up(battle)
