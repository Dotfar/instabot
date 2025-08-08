#<<<<<<< HEAD
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
#=======
#>>>>>>> 6511069 (Fix: downgrade telegram bot to 13.15 for compatibility)
from flask import Flask
from threading import Thread
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)


TOKEN = os.getenv("6368579330:AAFfXOvMLYDdKHkSsw9hvQ512klIpQxrBmg") 
CHANNEL = os.getenv("@Learndotfar")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def is_subscribed(bot, user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if await is_subscribed(context.bot, user.id):
        await update.message.reply_text("✅ عضو هستی! خوش اومدی.")
    else:
        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL[1:]}")],
            [InlineKeyboardButton("عضو شدم ✅", callback_data='check')]
        ]
        await update.message.reply_text(
            "برای استفاده از ربات باید عضو کانال بشی:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if await is_subscribed(context.bot, user_id):
        await query.edit_message_text("✅ عضویت تأیید شد! حالا از ربات استفاده کن.")
    else:
        await query.answer("❌ هنوز عضو نشدی!", show_alert=True)

async def main():
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join))
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())