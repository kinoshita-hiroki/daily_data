# My Daily Board

日々の活動や体調、学習時間などを記録・管理・可視化するためのStreamlitアプリケーションです。RPG要素を取り入れ、モチベーションを維持しながら習慣化をサポートします。

## 主な機能
- **目標・タスク管理**: 日々の目標やタスクを記録・確認できます。
- **体調管理**: メンタル状態や全般的な体調スコアを記録します。
- **活動記録**: 勉強時間や空腹時間（ファスティング）の記録が可能です。
- **アクティビティ**: 瞑想・写経、ヨガなどの実施状況を管理します。
- **RPG要素**: 日々の記録に応じて成長していくRPGのような要素を取り入れています。

## 技術スタック
- **言語**: Python3
- **フレームワーク**: Streamlit
- **主要ライブラリ**: Pandas, Pillow, python-dotenv, cryptography
- **インフラ/環境**: Docker, Docker Compose
- **テスト**: pytest, pytest-mock
- **リンター**: ruff

## セットアップと起動手順

### ローカル環境での実行
1. リポジトリのクローン後、依存パッケージをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
2. `.env`ファイルを作成し、必要な環境変数を設定してください（OpenAI APIキーなど）。
3. アプリケーションを起動します。
   ```bash
   streamlit run app.py
   ```

### Dockerを用いた実行
Dockerを利用して簡単に環境を構築・起動することができます。
```bash
docker-compose up -d --build
```
起動完了後、ブラウザで `http://localhost:8501` にアクセスしてください。

## ディレクトリ構成

- `app.py`: メインのStreamlitアプリケーションファイル
- `app/`: UIコンポーネント、設定(`config/`)、ユーティリティなどのアプリケーション内部ロジック
- `game/`: RPG要素やゲーム機能に関するロジック
- `pages/`: Streamlitのマルチページに関するファイル
- `data/` / `logs/`: 画像やログ・データファイルの保管ディレクトリ（Dockerにてマウント・永続化されます）
- `tests/`: pytestを用いたテストコード
- `docker-compose.yml` / `Dockerfile`: Dockerコンテナの構成ファイル

## 工夫した点

## 参考画像
![トップページ](docs/screenshots/top.png)
![レポートページ](docs/screenshots/report.png)
