import requests
import pandas as pd

def fetch_data(symbol, interval='5min', limit=10):
    url = f"https://api.coinex.com/v1/market/kline?market={symbol}&type={interval}&limit={limit}"
    r = requests.get(url)
    df = pd.DataFrame(r.json()['data'])[[0, 1, 2, 3, 4]]
    df.columns = ['timestamp', 'open', 'high', 'low', 'close']
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    return df

def detect_pattern(df):
    prev = df.iloc[-2]
    curr = df.iloc[-1]

    if prev['close'] < prev['open'] and curr['close'] > curr['open'] and curr['close'] > prev['open'] and curr['open'] < prev['close']:
        return "Bullish Engulfing", 1
    elif prev['close'] > prev['open'] and curr['close'] < curr['open'] and curr['close'] < prev['open'] and curr['open'] > prev['close']:
        return "Bearish Engulfing", -1
    elif curr['close'] > curr['open'] and (curr['open'] - curr['low']) > 2 * abs(curr['close'] - curr['open']):
        return "Hammer", 1
    elif curr['close'] < curr['open'] and (curr['high'] - curr['close']) > 2 * abs(curr['close'] - curr['open']):
        return "Inverted Hammer", -1
    elif abs(curr['open'] - curr['close']) < 0.1 * (curr['high'] - curr['low']):
        return "Doji", 0
    elif abs(curr['open'] - curr['close']) > 0.9 * (curr['high'] - curr['low']):
        return "Marubozu", 1 if curr['close'] > curr['open'] else -1

    return "None", 0

def analyze_patterns(symbol):
    df = fetch_data(symbol)
    pattern, score = detect_pattern(df)
    report = f"Pattern: {pattern} ({'Buy' if score > 0 else 'Sell' if score < 0 else 'Neutral'})"
    return {
        "score": score,
        "weight": 1,
        "report": report
    }
