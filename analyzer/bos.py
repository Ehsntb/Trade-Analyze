import requests
import pandas as pd

def fetch_data(symbol, interval='5min', limit=10):
    url = f"https://api.coinex.com/v1/market/kline?market={symbol}&type={interval}&limit={limit}"
    r = requests.get(url)
    df = pd.DataFrame(r.json()['data'])[[0, 2, 3, 4]]
    df.columns = ['timestamp', 'high', 'low', 'close']
    df[['high', 'low', 'close']] = df[['high', 'low', 'close']].astype(float)
    return df

def analyze_bos(symbol):
    df = fetch_data(symbol)

    price = df['close'].iloc[-1]
    highest = df['high'].iloc[-6:-1].max()
    lowest = df['low'].iloc[-6:-1].min()

    bos = "None"
    score = 0

    if price > highest:
        bos = "Break Up"
        score = 1
    elif price < lowest:
        bos = "Break Down"
        score = -1

    report = f"Break of Structure: {bos} (Price: {price:.2f}, High: {highest:.2f}, Low: {lowest:.2f})"

    return {
        "score": score,
        "weight": 1,
        "report": report
    }
