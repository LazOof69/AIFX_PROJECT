import pandas as pd
import json

def make_final_decision(price_path="data/usd_jpy.csv", sentiment_path="data/news_sentiment.json"):
    print("\n📊 綜合技術分析與新聞情緒進行決策...")

    # --- 1. 技術分析 ---
    df = pd.read_csv(price_path)
    df = df.dropna(subset=["EMA_5", "EMA_20", "MACD", "MACD_Signal", "RSI"])  # 避免 NaN
    latest = df.iloc[-1]

    tech_signals = []
    if latest["EMA_5"] > latest["EMA_20"]:
        tech_signals.append("EMA短期上穿 → 看多")
    else:
        tech_signals.append("EMA短期下穿 → 看空")

    if latest["MACD"] > latest["MACD_Signal"]:
        tech_signals.append("MACD 多頭排列 → 看多")
    else:
        tech_signals.append("MACD 空頭排列 → 看空")

    if latest["RSI"] > 70:
        tech_signals.append("RSI 過熱 (>70) → 看多")
    elif latest["RSI"] < 30:
        tech_signals.append("RSI 超賣 (<30) → 看空")
    else:
        tech_signals.append("RSI 中性")

    # 統計技術面看多 / 看空分數
    tech_score = sum("看多" in signal for signal in tech_signals) - sum("看空" in signal for signal in tech_signals)

    # --- 2. 新聞情緒分析 ---
    with open(sentiment_path, "r", encoding="utf-8") as f:
        sentiment_data = json.load(f)

    pos, neg, neu = 0, 0, 0
    for item in sentiment_data:
        analysis = item.get("analysis", "")
        if "positive" in analysis or "看多" in analysis:
            pos += 1
        elif "negative" in analysis or "看空" in analysis:
            neg += 1
        elif "neutral" in analysis or "中性" in analysis:
            neu += 1

    total_news = pos + neg + neu
    news_score = pos - neg

    # --- 綜合評估 ---
    final_score = tech_score + news_score
    if final_score >= 3:
        conclusion = "📈 今日判斷：看多"
    elif final_score <= -3:
        conclusion = "📉 今日判斷：看空"
    else:
        conclusion = "⚖️ 今日判斷：中性"

    # --- 結果輸出 ---
    print(conclusion)
    print("\n🔍 技術分析依據：")
    for s in tech_signals:
        print(" -", s)

    print(f"\n📰 新聞分析統計：{total_news} 則（看多 {pos} / 看空 {neg} / 中性 {neu}）")
    print(f"📊 綜合分數：技術 {tech_score:+d} + 新聞 {news_score:+d} = 總分 {final_score:+d}\n")

