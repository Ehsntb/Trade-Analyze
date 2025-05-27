import requests
import pandas as pd

def fetch_data(symbol, interval='5min', limit=50):
    url = f"https://api.coinex.com/v1/market/kline?market={symbol}&type={interval}&limit={limit}"
    r = requests.get(url)
    df = pd.DataFrame(r.json()['data'])[[0, 4]]
    df.columns = ['timestamp', 'close']
    df['close'] = pd.to_numeric(df['close'])
    return df

def find_abcd(df):
    # فرض: ۱۰ نقطه آخر برای تشکیل A, B, C, D
    close = df['close'].iloc[-10:].values
    a, b, c, d = close[0], close[3], close[6], close[9]
    ab = b - a
    cd = d - c
    ratio = abs(cd / ab) if ab != 0 else 0
    return ratio, (a, b, c, d)

def analyze_harmonic(symbol):
    df = fetch_data(symbol)
    ratio, points = find_abcd(df)
    a, b, c, d = points

    report = f"Harmonic ABCD: A={a:.2f}, B={b:.2f}, C={c:.2f}, D={d:.2f}, Ratio CD/AB = {ratio:.2f} → "

    # محدوده طلایی برای AB=CD حدود 1±10٪
    if 0.9 <= ratio <= 1.1:
        score = 1 if d > b else -1
        report += "Pattern Match"
    else:
        score = 0
        report += "No Clear Pattern"

    return {
        "score": score,
        "weight": 1,
        "report": report
    }
