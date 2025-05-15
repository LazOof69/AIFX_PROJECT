import json
import requests
from config import HUGGINGFACE_API_KEY

API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        result = response.json()
        print("\n📨 HuggingFace 回傳內容：")
        print(json.dumps(result, indent=2, ensure_ascii=False))  # 可讀性更好
        return result
    except Exception as e:
        print(f"\n❌ JSON 解碼失敗：{e}")
        print("🔴 原始回傳：", response.text)
        return {"error": "JSON decode error"}




def analyze_news_sentiment(news_path="data/news_today.json"):
    with open(news_path, "r", encoding="utf-8") as f:
        news_list = json.load(f)

    results = []

    print(f"\n📡 使用 HuggingFace FinBERT 模型進行情緒分析...")

    for i, news in enumerate(news_list):
        text = f"{news['title']} {news['summary']}"
        try:
            hf_result = query({"inputs": text})

            # 處理雙層 list 回傳：[[{label, score}, ...]]
            if (
                isinstance(hf_result, list)
                and len(hf_result) > 0
                and isinstance(hf_result[0], list)
                and len(hf_result[0]) > 0
                and isinstance(hf_result[0][0], dict)
            ):
                predictions = hf_result[0]
                top = max(predictions, key=lambda x: x.get("score", 0))
                label = top.get("label", "未知")
                score = round(top.get("score", 0), 3)
                analysis = f"判斷：{label}（置信度：{score}）"

            elif isinstance(hf_result, dict) and "error" in hf_result:
                analysis = f"API 錯誤：{hf_result['error']}"

            else:
                analysis = "⚠️ HuggingFace 回傳格式異常，無法解析"

        except Exception as e:
            analysis = f"❌ 分析錯誤：{e}"



        results.append({
            "title": news['title'],
            "summary": news['summary'],
            "source": news.get("source", ""),
            "analysis": analysis
        })
        print(f"✅ 第 {i+1} 則分析完成：{analysis}")

    with open("data/news_sentiment.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n🧠 全部分析完成，共 {len(results)} 則，已儲存至 data/news_sentiment.json")
