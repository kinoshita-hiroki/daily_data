import streamlit as st
from ui import render_observation_regist, render_feeling_regist, render_top_image_base64
import config

render_top_image_base64(config.TOP_IMAGE_PATH3)
render_feeling_regist()


