import app.config.config as config
from app.pages_ui import render_self_check_page
from app.ui import render_top_image_base64

render_top_image_base64(config.TOP_IMAGE_PATH4)
render_self_check_page()
