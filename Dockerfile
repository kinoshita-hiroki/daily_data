# ベースイメージ
FROM python:3.12-slim

# === タイムゾーンをJSTに設定 ===
ENV TZ=Asia/Tokyo
RUN apt-get update && apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get clean

# 作業ディレクトリ
WORKDIR /app

# 必要なライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリコードをコピー
COPY . .

# データフォルダ作成
RUN mkdir -p /app/logs

# Streamlit 起動
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]