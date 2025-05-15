import pandas as pd
import ta  # pip install ta

def analyze_technical_indicators():
    # 讀取先前抓好的匯率資料
    df = pd.read_csv("data/usd_jpy.csv")

    # 若 Datetime 是欄位就轉成 index，方便技術指標對齊
    if "Datetime" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Datetime"])
        df.set_index("Datetime", inplace=True)

    # --- 趨勢（EMA） ---
    df["EMA_5"]  = ta.trend.EMAIndicator(df["Close"], window=5).ema_indicator()
    df["EMA_20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()

    # --- 動能（RSI & 隨機震盪） ---
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    stoch     = ta.momentum.StochasticOscillator(df["High"], df["Low"], df["Close"])
    df["STOCH_K"] = stoch.stoch()  # %K 線

    # --- 波動度（布林通道寬度 & ATR） ---
    bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
    df["BB_WIDTH"] = (bb.bollinger_hband() - bb.bollinger_lband()) / df["Close"]
    df["ATR"]      = ta.volatility.AverageTrueRange(df["High"], df["Low"], df["Close"]).average_true_range()

    # --- 趨勢強度（ADX） ---
    df["ADX"] = ta.trend.ADXIndicator(df["High"], df["Low"], df["Close"]).adx()

    # 將含新指標的資料覆寫存回，後續 decision.py 會讀到
    df.reset_index().to_csv("data/usd_jpy.csv", index=False)
    print("📊 技術指標已更新並寫入 data/usd_jpy.csv")

    return df
