import streamlit as st
from app.ui import render_observation_regist, render_feeling_regist, render_top_image_base64
import app.config as config

render_top_image_base64(config.TOP_IMAGE_PATH4)
render_observation_regist()
