import requests
import pandas as pd

def fetch_data(symbol, interval='5min', limit=60):
    url = f"https://api.coinex.com/v1/market/kline?market={symbol}&type={interval}&limit={limit}"
    r = requests.get(url)
    df = pd.DataFrame(r.json()['data'])[[0, 4]]
    df.columns = ['timestamp', 'close']
    df['close'] = pd.to_numeric(df['close'])
    return df

def find_swings(close_prices, min_gap=0.005):
    swings = []
    for i in range(2, len(close_prices) - 2):
        local_max = close_prices[i] > close_prices[i-1] and close_prices[i] > close_prices[i+1]
        local_min = close_prices[i] < close_prices[i-1] and close_prices[i] < close_prices[i+1]
        if local_max or local_min:
            if not swings or abs(close_prices[i] - swings[-1][1]) / swings[-1][1] > min_gap:
                swings.append((i, close_prices[i]))
    return swings

def analyze_elliott_wave(symbol):
    df = fetch_data(symbol)
    close_prices = df['close'].tolist()
    swings = find_swings(close_prices)

    report = f"Elliott Wave Analysis: {len(swings)} pivots detected.\n"

    if len(swings) >= 7:
        wave_points = swings[-7:]
        prices = [p for i, p in wave_points]
        wave_labels = ['1', '2', '3', '4', '5', 'A', 'B']
        structure = ", ".join(f"Wave {label}: {price:.2f}" for label, price in zip(wave_labels, prices))

        # بررسی قواعد موج‌ها
        valid = prices[1] > prices[0]          # موج 2 اصلاح مثبت
        valid &= prices[2] > prices[1]         # موج 3 صعودی و بزرگتر از 1
        valid &= prices[3] > prices[1]         # موج 4 نباید پایین‌تر از موج 2 بیاد
        valid &= prices[4] > prices[2]         # موج 5 بالاتر از 3
        valid &= prices[5] < prices[4]         # موج A اصلاح از 5
        valid &= prices[6] > prices[5]         # موج B برگشت جزئی

        score = 1 if valid else 0
        stage = "✔️ Wave Structure Valid – Possibly in Wave C" if score == 1 else "❌ Unclear or Incomplete Wave Structure"

        report += structure + f"\n→ {stage}"
    else:
        score = 0
        report += "Not enough wave pivots to analyze"

    return {
        "score": score,
        "weight": 1,
        "report": report
    }

