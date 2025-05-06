import feedparser
import pandas as pd
from datetime import datetime
import os

# Define project root relative to this file
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Ensure top-level data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# Define RSS feeds
RSS_FEEDS = {
    "Economic Times - Tech": "https://economictimes.indiatimes.com/rss/tech/rssfeeds/13357270.cms",
    "LiveMint - Companies": "https://www.livemint.com/rss/companies",
    "Business Standard - Deals": "https://www.business-standard.com/rss/companies-10202.rss",
    "MoneyControl - Market News": "https://www.moneycontrol.com/rss/MCtopnews.xml"
}

def fetch_news():
    all_articles = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            published = entry.get("published", datetime.now().isoformat())
            
            try:
                published_time = datetime(*entry.published_parsed[:6]).isoformat()
            except:
                published_time = published

            article = {
                "title": title,
                "source": source,
                "url": link,
                "published": published_time
            }

            all_articles.append(article)

    return all_articles

def save_news(articles):
    df = pd.DataFrame(articles)
    df = df.drop_duplicates(subset=["title", "url"])
    df = df.sort_values("published", ascending=False)

    # Save inside top-level 'data' directory
    csv_path = os.path.join(DATA_DIR, "news_feed.csv")
    txt_path = os.path.join(DATA_DIR, "news_feed.txt")

    df.to_csv(csv_path, index=False)

    with open(txt_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(f"{row['title']} ({row['source']})\n{row['url']}\n\n")

    print(f"✅ Fetched and saved {len(df)} news articles to top-level 'data' folder.")

if __name__ == "__main__":
    articles = fetch_news()
    save_news(articles)
