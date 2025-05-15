import pandas as pd
import json
from textwrap import shorten

def make_final_decision(price_path="data/usd_jpy.csv",
                        sentiment_path="data/news_sentiment.json",
                        sample_titles=3):
    print("\n📊 綜合技術分析與新聞情緒進行決策...\n")

    # ==========  1. 技術分析  ==================================================
    df = pd.read_csv(price_path).dropna(subset=[
        "EMA_5", "EMA_20", "RSI", "STOCH_K",
        "ADX", "BB_WIDTH"
    ])
    latest = df.iloc[-1]
    tech_signals = []
    bull_tech, bear_tech = 0.0, 0.0       # 用浮點數方便含權重

    # ---- 趨勢：EMA 交叉（需 ADX ≥ 25） ----
    if latest["ADX"] >= 25:
        if latest["EMA_5"] > latest["EMA_20"]:
            tech_signals.append("EMA 5>20 且 ADX≥25 → 趨勢偏多 (+1)")
            bull_tech += 1
        else:
            tech_signals.append("EMA 5<20 且 ADX≥25 → 趨勢偏空 (-1)")
            bear_tech += 1
    else:
        tech_signals.append("ADX<25 → 趨勢不明，不計分")

    # ---- 動能：RSI ----
    if latest["RSI"] > 70:
        tech_signals.append(f"RSI {latest['RSI']:.1f}>70 → 多頭動能 (+1)")
        bull_tech += 1
    elif latest["RSI"] < 30:
        tech_signals.append(f"RSI {latest['RSI']:.1f}<30 → 空頭動能 (-1)")
        bear_tech += 1

    # ---- 動能：Stochastic K ----
    if latest["STOCH_K"] > 80:
        tech_signals.append(f"Stoch_K {latest['STOCH_K']:.1f}>80 → 動能轉弱 (-1)")
        bear_tech += 1
    elif latest["STOCH_K"] < 20:
        tech_signals.append(f"Stoch_K {latest['STOCH_K']:.1f}<20 → 動能轉強 (+1)")
        bull_tech += 1

    # ---- 波動：BB_WIDTH ----
    if latest["BB_WIDTH"] > 0.04:  # >4%
        tech_signals.append(f"布林寬度 {latest['BB_WIDTH']:.2%}>4% → 趨勢延續，技術總分 ×1.5")
        bull_tech *= 1.5
        bear_tech *= 1.5

    tech_score = bull_tech - bear_tech
    tech_total = bull_tech + bear_tech
    tech_bull_pct = (bull_tech / tech_total * 100) if tech_total else 0
    tech_bear_pct = (bear_tech / tech_total * 100) if tech_total else 0

    # ==========  2. 新聞情緒  ==================================================
    with open(sentiment_path, "r", encoding="utf-8") as f:
        sentiment_data = json.load(f)

    bull_news, bear_news, neu_news = 0, 0, 0
    bull_titles, bear_titles = [], []

    for item in sentiment_data:
        analysis = item.get("analysis", "").lower()
        if "positive" in analysis or "看多" in analysis:
            bull_news += 1
            if len(bull_titles) < sample_titles:
                bull_titles.append(shorten(item["title"], 80))
        elif "negative" in analysis or "看空" in analysis:
            bear_news += 1
            if len(bear_titles) < sample_titles:
                bear_titles.append(shorten(item["title"], 80))
        else:
            neu_news += 1

    total_news = bull_news + bear_news + neu_news
    news_score = bull_news - bear_news
    news_bull_pct = bull_news / total_news * 100 if total_news else 0
    news_bear_pct = bear_news / total_news * 100 if total_news else 0

    # ==========  3. 綜合結論  ==================================================
    final_score = tech_score + news_score
    if final_score >= 3:
        conclusion = "📈 **今日總體偏多**"
    elif final_score <= -3:
        conclusion = "📉 **今日總體偏空**"
    else:
        conclusion = "⚖️ **今日觀望 / 中性**"

    # ==========  4. 輸出報告  =================================================
    print(conclusion)
    print(f"➡️ 多空比 (技術/新聞綜合): {bull_tech + bull_news:.1f} 多 ╱ {bear_tech + bear_news:.1f} 空")

    print("\n--- 技術面詳解 ----------------")
    for s in tech_signals:
        print("•", s)
    print(f"🔢 技術得分：{tech_score:+.1f}　(多 {tech_bull_pct:.1f}% / 空 {tech_bear_pct:.1f}%)")

    print("\n--- 新聞面詳解 ----------------")
    print(f"總計 {total_news} 則 ｜ 多 {bull_news} ({news_bull_pct:.1f}%) / 空 {bear_news} ({news_bear_pct:.1f}%) / 中性 {neu_news}")
    if bull_titles:
        print("📚 多方代表標題:")
        for t in bull_titles:
            print("  -", t)
    if bear_titles:
        print("📚 空方代表標題:")
        for t in bear_titles:
            print("  -", t)

    print(f"\n🧮 綜合評分：技術 {tech_score:+.1f}  +  新聞 {news_score:+.0f}  =  {final_score:+.1f}\n")
