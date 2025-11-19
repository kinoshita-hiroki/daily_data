from transformers import pipeline

def get_sentiment_score(text: str):
    # 初回ロード（少し時間かかる）
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
    )
    if not text.strip():
        return None
    
    result = sentiment_analyzer(text)[0]
    label = result["label"]  # Positive / Negative / Neutral
    score = result["score"]  # 0〜1 の確信度
    print(f"score:{score}")
    # スコア方式の例（好きに調整可）
    if label == "positive":
        mapped = 5 + score * 5        # 5〜10
    elif label == "negative":
        mapped = (1 - score) * 5      # 0〜5
    else:
        mapped = 5                    # 中立
    print(f"score:{mapped}")
    return {
        "label": label,
        "raw_score": score,
        "mapped_score": round(mapped, 2)
    }
