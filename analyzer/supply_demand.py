import requests
import pandas as pd

def fetch_data(symbol, interval='5min', limit=20):
    url = f"https://api.coinex.com/v1/market/kline?market={symbol}&type={interval}&limit={limit}"
    r = requests.get(url)
    df = pd.DataFrame(r.json()['data'])[[0, 2, 3, 4]]
    df.columns = ['timestamp', 'high', 'low', 'close']
    df[['high', 'low', 'close']] = df[['high', 'low', 'close']].astype(float)
    return df

def find_zones(df):
    # ناحیه عرضه: بیشترین قیمت در فاز فشردگی
    supply_zone = df['high'].rolling(window=3).max().iloc[-6:-1].mean()
    # ناحیه تقاضا: کمترین قیمت در فاز فشردگی
    demand_zone = df['low'].rolling(window=3).min().iloc[-6:-1].mean()
    return supply_zone, demand_zone

def analyze_supply_demand(symbol):
    df = fetch_data(symbol)
    price = df['close'].iloc[-1]
    supply_zone, demand_zone = find_zones(df)

    distance_to_supply = abs(price - supply_zone)
    distance_to_demand = abs(price - demand_zone)

    # اگر قیمت نزدیک یکی از زون‌ها باشه، سیگنال بده
    threshold = (supply_zone - demand_zone) * 0.25
    score = 0
    bias = "Neutral"

    if distance_to_demand < threshold:
        score = 1
        bias = "Buy Zone"
    elif distance_to_supply < threshold:
        score = -1
        bias = "Sell Zone"

    report = f"Supply Zone: {supply_zone:.2f}, Demand Zone: {demand_zone:.2f}, Price: {price:.2f} → {bias}"

    return {
        "score": score,
        "weight": 1,
        "report": report
    }
