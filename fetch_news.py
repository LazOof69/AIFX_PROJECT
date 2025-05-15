import feedparser
import json
from datetime import datetime

# 多個新聞來源：可自由增刪
FEED_URLS = {
    "WSJ": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "NHK": "https://www3.nhk.or.jp/rss/news/cat0.xml",
    "BBC": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
}

def fetch_news():
    all_news = []

    print(f"\n[{datetime.now()}] 正在抓取新聞...")

    for name, url in FEED_URLS.items():
        feed = feedparser.parse(url)
        count = 0

        for entry in feed.entries[:5]:  # 每個來源最多抓 5 篇
            news_item = {
                "title": entry.title,
                "summary": getattr(entry, "summary", ""),
                "link": entry.link,
                "source": name
            }
            all_news.append(news_item)
            count += 1

        print(f"✅ {name} - 取得 {count} 則")

    # 去重：根據 title 做唯一判斷
    unique_news = {item['title']: item for item in all_news}.values()

    # 寫入檔案
    with open("data/news_today.json", "w", encoding="utf-8") as f:
        json.dump(list(unique_news), f, ensure_ascii=False, indent=2)

    print(f"\n📦 總共寫入 {len(unique_news)} 則新聞到 data/news_today.json\n")

