# ingestion/sentiment.py

import pandas as pd
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon (only needed once)
nltk.download("vader_lexicon")

# Dynamically get path to data/ directory (one level up from current file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

INPUT_FILE = os.path.join(DATA_DIR, "news_feed.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "news_sentiment.csv")
OUTPUT_TXT = os.path.join(DATA_DIR, "news_sentiment_summary.txt")

# Ensure data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

def analyze_sentiment():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"{INPUT_FILE} not found. Run news.py first.")

    df = pd.read_csv(INPUT_FILE)
    sid = SentimentIntensityAnalyzer()
    sentiments = []

    for title in df["title"]:
        score = sid.polarity_scores(title)["compound"]
        if score >= 0.05:
            sentiment = "Positive"
        elif score <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        sentiments.append(sentiment)

    df["sentiment"] = sentiments
    df.to_csv(OUTPUT_CSV, index=False)

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(f"[{row['sentiment']}] {row['title']} ({row['source']})\n")

    print(f"✅ Sentiment analysis complete: {len(df)} headlines analyzed.")

if __name__ == "__main__":
    analyze_sentiment()
