import logging
import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          CallbackQueryHandler, ContextTypes, filters)
from analyzer.core import analyze_market
from user_config import USERS, default_symbols
from keep_alive import keep_alive
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

keep_alive()
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

# دکمه‌های کیبورد اصلی
custom_keyboard = [["🟠 BTC/USDT", "🔵 ETH/USDT"], ["🟣 SOL/USDT", "🟢 XRP/USDT"],
                   ["🟡 BNB/USDT"], ["⚙️ Notification Settings"]]
reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)


# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ارز مورد نظر رو انتخاب کن:",
                                    reply_markup=reply_markup)


# هندلر کلی برای تحلیل دستی
async def handle_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USERS:
        await update.message.reply_text("دسترسی غیرمجاز")
        return

    text = update.message.text.strip().lower()
    mapping = {
        "🟠 btc/usdt": "btcusdt",
        "🔵 eth/usdt": "ethusdt",
        "🟣 sol/usdt": "solusdt",
        "🟢 xrp/usdt": "xrpusdt",
        "🟡 bnb/usdt": "bnbusdt"
    }

    if text.startswith("/signal"):
        parts = text.split()
        if len(parts) != 2:
            await update.message.reply_text("استفاده صحیح: /signal BTCUSDT")
            return
        symbol = parts[1].lower()
    elif text in mapping:
        symbol = mapping[text]
    elif text == "⚙️ notification settings":
        await notifications_command(update, context)
        return
    else:
        await update.message.reply_text("دستور ناشناس یا ارز نامعتبر.")
        return

    await update.message.reply_text("در حال تحلیل...")
    result = analyze_market(symbol)
    await update.message.reply_text(result)


# تنظیمات نوتیفیکیشن برای هر کاربر
async def notifications_command(update: Update,
                                context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USERS:
        await update.message.reply_text(
            "شما مجاز به استفاده از این دستور نیستید.")
        return
    status = USERS[user_id].get("notifications_enabled", False)
    text = f"Do you want to receive automated signal alerts?\n(Current: {'✅ Enabled' if status else '❌ Disabled'})"
    keyboard = [[
        InlineKeyboardButton("✅ Enable", callback_data="enable_notifications"),
        InlineKeyboardButton("❌ Disable",
                             callback_data="disable_notifications"),
    ]]
    await update.message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard))


# پاسخ به دکمه تنظیم نوتیفیکیشن
async def notifications_callback(update: Update,
                                 context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in USERS:
        await query.edit_message_text("دسترسی ندارید.")
        return
    if query.data == "enable_notifications":
        USERS[user_id]["notifications_enabled"] = True
        await query.edit_message_text(
            "✅ Notifications enabled. You will receive real-time signals.")
    elif query.data == "disable_notifications":
        USERS[user_id]["notifications_enabled"] = False
        await query.edit_message_text(
            "❌ Notifications disabled. You will not receive auto signals.")


# تحلیل خودکار برای کاربران فعال هر ۲ دقیقه
async def auto_analysis(context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    for user_id, info in USERS.items():
        if not info.get("notifications_enabled", False):
            continue
        for symbol in default_symbols:
            result = analyze_market(symbol)
            if "🟢 Strong Buy" in result or "🔴 Strong Sell" in result:
                await bot.send_message(chat_id=user_id, text=result)


# اجرای ربات
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("signal", handle_signal))
app.add_handler(CommandHandler("notifications", notifications_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_signal))
app.add_handler(CallbackQueryHandler(notifications_callback))

# برنامه‌ریزی تحلیل اتوماتیک
job_queue = app.job_queue
job_queue.run_repeating(auto_analysis, interval=120, first=10)

if __name__ == "__main__":
    app.run_polling()
