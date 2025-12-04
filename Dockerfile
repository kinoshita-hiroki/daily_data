# ベースイメージ
FROM python:3.12-slim

# 作業ディレクトリ
WORKDIR /app

# 必要なライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリコードをコピー
COPY . .

# データフォルダ作成（永続化は docker-compose で）
RUN mkdir -p /app/logs

# Streamlit を起動
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
