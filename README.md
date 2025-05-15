# AIFX_PROJECT
AIFX 是一套自動化的外匯分析系統，專為 USD/JPY 匯率打造。  
透過技術分析 + 新聞情緒判斷，產出每日交易建議（看多 / 看空 / 中性）。

---

## 🚀 功能 Features

- 📈 自動抓取 USD/JPY 匯率（來自 Yahoo Finance）
- 📰 多來源新聞整合（NHK、WSJ、BBC、CNBC）
- 🤖 使用 HuggingFace FinBERT 模型分析每則新聞情緒（看多 / 看空 / 中性）
- 📊 計算 RSI、EMA、MACD 等技術指標
- 🧠 綜合技術 + 新聞情緒，自動判斷今日交易方向
- 📂 所有分析儲存為 JSON/CSV 檔案（可供進一步使用）

---

## 📂 專案結構

```bash
AIFX/
├── data/                  # 暫存抓取的資料與分析結果
│   ├── usd_jpy.csv
│   ├── news_today.json
│   └── news_sentiment.json
├── fetch_price.py         # 抓取匯率
├── fetch_news.py          # 抓取新聞（多來源 RSS）
├── analyze.py             # 技術指標計算
├── sentiment.py           # 使用 HuggingFace API 進行情緒分析
├── decision.py            # 綜合技術與情緒輸出每日建議
├── main.py                # 主流程整合
├── config.py              # 儲存 API key（不上傳）
└── requirements.txt       # 套件安裝清單


⚙️安裝與執行方式
pip install -r requirements.txt #安裝套件
python main.py  #執行主流程

🔐 注意事項
請自行建立 config.py 並加入以下內容：
HUGGINGFACE_API_KEY = "hf_你的token"

config.py 已透過 .gitignore 忽略，不會被上傳

