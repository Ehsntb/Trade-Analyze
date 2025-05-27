from analyzer.patterns import analyze_patterns
from analyzer.rsi_macd_ema import analyze_rsi_macd_ema
from analyzer.volume import analyze_volume
from analyzer.bos import analyze_bos
from analyzer.supply_demand import analyze_supply_demand
from analyzer.harmonic import analyze_harmonic
from analyzer.elliott_wave import analyze_elliott_wave
from analyzer.trade_plan import generate_trade_plan
from datetime import datetime


def analyze_market(symbol):
    results = []

    # اجرای تحلیل‌ها
    pattern = analyze_patterns(symbol)
    rsi_macd = analyze_rsi_macd_ema(symbol)
    volume = analyze_volume(symbol)
    bos = analyze_bos(symbol)
    sd = analyze_supply_demand(symbol)
    harmonic = analyze_harmonic(symbol)
    elliott = analyze_elliott_wave(symbol)

    results.extend([pattern, rsi_macd, volume, bos, sd, harmonic, elliott])

    total_score = sum(r['score'] for r in results)
    total_weight = sum(r['weight'] for r in results)

    # تصمیم نهایی
    if total_score >= 4:
        decision = "🟢 Strong Buy"
    elif total_score >= 2:
        decision = "🟡 Watch Buy"
    elif total_score <= -4:
        decision = "🔴 Strong Sell"
    elif total_score <= -2:
        decision = "🟠 Watch Sell"
    else:
        decision = "⚪ Neutral"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # استخراج قیمت لحظه‌ای
    try:
        price_line = [r for r in results if "Price:" in r["report"]][0]["report"]
        price = float(price_line.split("Price:")[1].split(",")[0].strip().split()[0])
    except:
        price = 0.0

    # ساخت پیام نهایی
    output = (
        f"📈 Market: {symbol.upper()}\n"
        f"⏱️ Time: {now}\n"
        f"💰 Live Price: {price:.2f} USDT\n\n"
        "-------------------------------\n"
    )

    labels = [
        "🔯 Pattern",
        "📊 RSI/MACD/EMA",
        "📉 Volume",
        "📀 BoS",
        "📦 S&D Zone",
        "🔏 Harmonic",
        "🌊 Elliott"
    ]

    for label, r in zip(labels, results):
        output += f"{label}: {r['report']}\n"

    output += "-------------------------------\n"
    output += f"\n📊 Final Signal: {decision} ({total_score}/{total_weight})\n"

    # تحلیل Watch Mode حرفه‌ای
    if decision.startswith("\ud83d\udfe1") or decision.startswith("\ud83d\udfe0"):
        output += ("\n⚠️ Watch Mode Active\n")
        if "Weak" in volume['report']:
            output += "• Volume: Not Confirmed\n"
        if "Break Down" in bos['report'] or "Break Up" in bos['report']:
            output += "• Structure: Potential Breakout\n"
        if "Neutral" not in sd['report']:
            output += f"• Price near {sd['report'].split('→')[1].strip()}\n"
        if elliott['score'] == 0 and "5 pivots" in elliott['report']:
            output += "• Elliott Wave Impulse Completed\n"
        output += "→ Recommendation: Wait for confirmation before entering position.\n"

    # محاسبه تارگت و استاپ فقط در سیگنال Buy/Sell قطعی
    if decision.startswith("\ud83d\udfe2") or decision.startswith("\ud83d\udd34"):
        context_data = {
            "price": price,
            "bollinger_upper": float(rsi_macd["report"].split("EMA30:")[1].split()[0]) + 100,
            "bollinger_lower": float(rsi_macd["report"].split("EMA30:")[1].split()[0]) - 100,
            "supply": float(sd["report"].split("Supply Zone:")[1].split(",")[0].strip()),
            "demand": float(sd["report"].split("Demand Zone:")[1].split(",")[0].strip())
        }
        plan = generate_trade_plan(symbol, decision, context_data)
        if plan:
            output += (
                f"\n🎯 Entry: {plan['entry']}\n"
                f"✅ Target: {plan['target']}\n"
                f"⛔ Stop Loss: {plan['stop']}\n"
            )

    return output
