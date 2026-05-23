import json
import os

import pandas as pd

from app.config.config import (
    CONDITION_CSV,
    DATA_FILE,
    HUMAN_SKILL_CSV,
    MEDITATION_CSV,
    STUDY_TIME_CSV,
    WORKOUT_CSV,
    YOGA_CSV,
)


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def calculate_task_sum() -> int:
    # logs/daily_data.json から done の合計を取得
    # 実行時のカレントディレクトリに注意が必要だが、通常はプロジェクトルート
    path = DATA_FILE
    if not os.path.exists(path):
        return 5 # デフォルト値

    data = load_json(path)
    total_done = 0
    for date_data in data.values():
        tasks = date_data.get("tasks", [])
        for task in tasks:
            if task.get("done") is True:
                total_done += 1
    return total_done

def calculate_condition_avg() -> float:
    path = CONDITION_CSV 
    if not os.path.exists(path):
        return 3 # デフォルト値

    df = pd.read_csv(path)
    df_tail = df.tail(5)
    df_tail["condition"] = df_tail["condition"].astype(float).copy()
    avg = df_tail["condition"].mean()
    return avg
def calculate_workout_done_sum(job) -> int:
    path = WORKOUT_CSV
    if not os.path.exists(path):
        return 0

    try:
        df = pd.read_csv(path)
        done_total = df[df["done"] == 1]
        done_total = done_total[done_total["category"] == job.name]
        return len(done_total)
    except Exception:
        return 0

def calculate_human_skill_last_value() -> int:
    path = HUMAN_SKILL_CSV
    if not os.path.exists(path):
        return 0

    try:
        df = pd.read_csv(path)
        if df.empty:
            return 0
        return int(df.iloc[-1]["human_skill"])
    except Exception:
        return 0

def calculate_study_time_ma() -> float:
    path = STUDY_TIME_CSV
    if not os.path.exists(path):
        return 0.0

    try:
        df = pd.read_csv(path)
        if df.empty:
            return 0.0
        # 最後の7日間の平均を計算
        ma = df.tail(7)["study_time"].mean()
        return float(ma)
    except Exception:
        return 0.0

def calculate_yoga_total_time() -> int:
    path = YOGA_CSV
    if not os.path.exists(path):
        return 0

    try:
        df = pd.read_csv(path)
        if df.empty:
            return 0
        total = df["yoga"].sum()
        return int(total)
    except Exception:
        return 0

def calculate_meditation_total_time() -> int:
    path = MEDITATION_CSV
    if not os.path.exists(path):
        return 0

    try:
        df = pd.read_csv(path)
        if df.empty:
            return 0
        total = df["meditation"].sum()
        return int(total)
    except Exception:
        return 0
