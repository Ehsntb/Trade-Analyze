def generate_trade_plan(symbol, signal_type, context):
    try:
        price = float(context.get("price", 0))
        bollinger_upper = float(context.get("bollinger_upper", 0))
        bollinger_lower = float(context.get("bollinger_lower", 0))
        supply = float(context.get("supply", 0))
        demand = float(context.get("demand", 0))
    except:
        return None  # اطلاعات ناقص

    entry = price
    target = "-"
    stop = "-"

    # پاکسازی اموجی یا واژه اضافی از سیگنال
    clean_signal = signal_type.lower()
    for emoji in ["🟢", "🔴", "🟡", "🟠", "⚪"]:
        clean_signal = clean_signal.replace(emoji, "")
    clean_signal = clean_signal.strip()

    if clean_signal.startswith("strong buy") or clean_signal.startswith("buy"):
        target = round(min(bollinger_upper, supply), 2)
        stop = round(demand, 2)
    elif clean_signal.startswith("strong sell") or clean_signal.startswith("sell"):
        target = round(max(bollinger_lower, demand), 2)
        stop = round(supply, 2)

    return {
        "entry": round(entry, 2),
        "target": target,
        "stop": stop
    }
