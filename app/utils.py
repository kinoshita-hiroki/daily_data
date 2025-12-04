# --------------------------
# Utility Functions
# --------------------------
import json
import os

import pandas as pd


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

def append_or_update(df, date_str, col, value):
    if date_str in df["date"].values:
        df.loc[df["date"] == date_str, col] = value
    else:
        df.loc[len(df)] = [date_str, value]
    return df

def iso(d: date):
    return d.isoformat()
