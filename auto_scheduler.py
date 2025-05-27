
from telegram import Bot
from analyzer import analyze_market
from user_config import user_notifications, default_symbols

def analyze_and_notify_all(bot: Bot):
    for user_id, active in user_notifications.items():
        if not active:
            continue
        for symbol in default_symbols:
            result = analyze_market(symbol)
            if "Buy" in result or "Sell" in result:
                bot.send_message(chat_id=user_id, text=result)
