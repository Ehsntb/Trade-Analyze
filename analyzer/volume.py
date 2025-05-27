import requests
import pandas as pd

def fetch_data(symbol, interval='5min', limit=10):
    url = f"https://api.coinex.com/v1/market/kline?market={symbol}&type={interval}&limit={limit}"
    r = requests.get(url)
    df = pd.DataFrame(r.json()['data'])[[0, 5]]
    df.columns = ['timestamp', 'volume']
    df['volume'] = pd.to_numeric(df['volume'])
    return df

def analyze_volume(symbol):
    df = fetch_data(symbol)

    current_volume = df['volume'].iloc[-1]
    avg_volume = df['volume'].iloc[-6:-1].mean()

    # امتیازدهی بر اساس حجم فعلی نسبت به میانگین ۵ کندل قبل
    if current_volume > avg_volume * 1.2:
        score = 1
        strength = "Strong Volume"
    elif current_volume < avg_volume * 0.8:
        score = -1
        strength = "Weak Volume"
    else:
        score = 0
        strength = "Neutral Volume"

    report = f"Volume: {current_volume:.2f} (Avg: {avg_volume:.2f}) → {strength}"

    return {
        "score": score,
        "weight": 1,
        "report": report
    }
