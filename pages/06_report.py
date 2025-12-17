
import streamlit as st

import app.config.config as config
from app.pages_ui import aggregate_data, build_prompt, llm
from app.utils import load_json

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

