import pandas as pd
import ta

def analyze_technical_indicators():
    df = pd.read_csv("data/usd_jpy.csv")

    if 'Datetime' in df.columns:
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df.set_index('Datetime', inplace=True)

    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['EMA_5'] = ta.trend.EMAIndicator(df['Close'], window=5).ema_indicator()
    df['EMA_20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()

    df.to_csv("data/usd_jpy.csv", index=False)  # ✅ 加上這行
    print("\n📊 最新技術指標已分析並儲存！")
    return df

