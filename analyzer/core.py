from analyzer.patterns import analyze_patterns
from analyzer.rsi_macd_ema import analyze_rsi_macd_ema
from analyzer.volume import analyze_volume
from analyzer.bos import analyze_bos
from analyzer.supply_demand import analyze_supply_demand
from analyzer.harmonic import analyze_harmonic
from analyzer.elliott_wave import analyze_elliott_wave
from analyzer.trade_plan import generate_trade_plan
from utils.fetch_data import fetch_data
from datetime import datetime

def analyze_market(symbol):
    df = fetch_data(symbol)
    price = df['close'].iloc[-1]
    time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # اجرای همه ماژول‌های تحلیل
    results = [
        analyze_patterns(symbol),
        analyze_rsi_macd_ema(symbol),
        analyze_volume(symbol),
        analyze_bos(symbol),
        analyze_supply_demand(symbol),
        analyze_harmonic(symbol),
        analyze_elliott_wave(symbol)
    ]

    total_weight = sum(r['weight'] for r in results)
    total_score = sum(r['score'] for r in results)
    final_score = round(total_score - total_weight / 2)

    # تعیین سیگنال نهایی
    if final_score >= 4:
        signal = "🟢 Strong Buy"
    elif final_score == 3:
        signal = "🟢 Buy"
    elif final_score == 2:
        signal = "🟡 Watch Buy"
    elif final_score == 1:
        signal = "⚪ Neutral"
    elif final_score == 0:
        signal = "⚪ Neutral"
    elif final_score == -1:
        signal = "🟠 Watch Sell"
    elif final_score == -2:
        signal = "🟠 Watch Sell"
    elif final_score == -3:
        signal = "🔴 Sell"
    else:
        signal = "🔴 Strong Sell"

    # ساخت گزارش خروجی
    output = f"""📈 Market: {symbol.upper()}
⏱️ Time: {time}
💰 Live Price: {price:.2f} USDT

-------------------------------"""
    for r in results:
        output += f"\n{r['report']}"

    output += f"\n-------------------------------\n\n📊 Final Signal: {signal} ({final_score}/{total_weight})"

    # اضافه کردن تارگت و استاپ اگر سیگنال خرید/فروش باشد
    if "Buy" in signal or "Sell" in signal:
        trade = generate_trade_plan(price, signal)
        entry = trade.get("entry", "-")
        target = trade.get("target", "-")
        stop_loss = trade.get("stop_loss", "-")

        output += f"""\n\n🎯 Entry: {entry}
✅ Target: {target}
⛔ Stop Loss: {stop_loss}"""

    return output
