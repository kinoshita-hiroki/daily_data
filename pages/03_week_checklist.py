import app.config.config as config
from app.ui import render_top_image_base64
from app.pages_ui import render_workout_checklist


# ========== 描画 ==========
render_top_image_base64(config.TOP_IMAGE_PATH3)
render_workout_checklist()
