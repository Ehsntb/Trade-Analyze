
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from user_config import user_notifications

def notifications_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    status = user_notifications.get(user_id, False)
    text = "Do you want to receive automated signal alerts?\n(Current: {})".format("✅ Enabled" if status else "❌ Disabled")

    keyboard = [
        [
            InlineKeyboardButton("✅ Enable", callback_data="enable_notifications"),
            InlineKeyboardButton("❌ Disable", callback_data="disable_notifications"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, reply_markup=reply_markup)

def notifications_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    if query.data == "enable_notifications":
        user_notifications[user_id] = True
        query.edit_message_text("✅ Notifications enabled. You will receive real-time signals.")
    elif query.data == "disable_notifications":
        user_notifications[user_id] = False
        query.edit_message_text("❌ Notifications disabled. You will not receive auto signals.")
