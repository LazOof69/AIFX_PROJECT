import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_usdjpy():
    ticker = yf.Ticker("JPY=X")  # 美元兌日圓
    hist = ticker.history(period="7d", interval="1h")  # 近7日，每小時K
    hist.reset_index(inplace=True)
    hist.to_csv("data/usd_jpy.csv", index=False)
    print(f"[{datetime.now()}] 匯率資料已儲存！")
