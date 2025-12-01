import streamlit as st
import pandas as pd
from datetime import datetime
import os
import io

from ui import render_observation_regist
# 暗号化を使う場合は有効化
import config




def main():
    st.title("🔍 観察メモ（人・企業）")

    render_observation_regist()


if __name__ == "__main__":
    main()
