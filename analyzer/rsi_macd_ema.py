import requests
import pandas as pd
import ta

def fetch_data(symbol, interval='5min', limit=100):
    url = f"https://api.coinex.com/v1/market/kline?market={symbol}&type={interval}&limit={limit}"
    r = requests.get(url)
    df = pd.DataFrame(r.json()['data'])[[0, 4]]
    df.columns = ['timestamp', 'close']
    df['close'] = pd.to_numeric(df['close'])
    return df

def analyze_rsi_macd_ema(symbol):
    df = fetch_data(symbol)
    close = df['close']

    # محاسبه RSI
    rsi_val = ta.momentum.RSIIndicator(close, window=14).rsi().iloc[-1]

    # محاسبه MACD Histogram
    macd = ta.trend.MACD(close)
    macd_val = macd.macd_diff().iloc[-1]

    # کراس EMA
    ema7 = ta.trend.EMAIndicator(close, window=7).ema_indicator().iloc[-1]
    ema30 = ta.trend.EMAIndicator(close, window=30).ema_indicator().iloc[-1]

    # سیستم امتیازدهی ترکیبی
    score = 0
    if macd_val > 0:
        score += 1
    elif macd_val < 0:
        score -= 1

    if rsi_val > 70:
        score -= 1
    elif rsi_val < 30:
        score += 1

    if ema7 > ema30:
        score += 1
    elif ema7 < ema30:
        score -= 1

    final_score = max(min(score, 1), -1)

    report = f"RSI: {rsi_val:.2f}, MACD: {macd_val:.4f}, EMA7: {ema7:.2f}, EMA30: {ema30:.2f} → "
    if final_score > 0:
        report += "Buy"
    elif final_score < 0:
        report += "Sell"
    else:
        report += "Neutral"

    return {
        "score": final_score,
        "weight": 1,
        "report": report
    }
