
import pandas as pd
import streamlit as st

import app.config.config as config
from app.utils import load_json


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

all_data = load_json(config.DATA_FILE)
df = aggregate_data(all_data)
st.subheader("過去のタスク達成数")
st.bar_chart(
    df.set_index("date")["done"]
)
st.subheader("過去のタスク非達成数")
st.bar_chart(
    df.set_index("date")["cant"]
)
if st.button("先週の振り返りを生成"):
    st.subheader("先週の振り返り")
    list_keys = []
    for i in range(0, len(list(all_data)), 7):
        if i + 7 < len(list(all_data)):
            keys = list(all_data)[i: i+7]
        else:
            keys = list(all_data)[i: len(list(all_data)) - 1]
        list_keys.append(keys)
    tasks_list = []
    for keys in list_keys:
        week_tasks = []
        for day in keys:
            for task in all_data[day]["tasks"]:
                if task["done"]:
                    week_tasks.append(task["name"])
        tasks_list.append(week_tasks)
    for tasks, keys in zip(tasks_list, list_keys):
        prompt = build_prompt(tasks)
        res = llm(prompt)
        st.subheader(str(keys[0])+ "~" + str(keys[-1]))
        st.write(res)

