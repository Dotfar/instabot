import os
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# از این به بعد فقط توکن رو مستقیم نذار، بذار تو محیط Railway ست شه
TOKEN = os.getenv("BOT_TOKEN")  # تو Railway باید متغیر محیطی بذاری با اسم BOT_TOKEN
CHANNEL = os.getenv("CHANNEL_USERNAME")  # مثلاً: @yourchannel یا بدون @

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def is_subscribed(bot, user_id: int) -> bool:
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
            [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL}")],
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

def main():
    keep_alive()
    app_builder = ApplicationBuilder().token(TOKEN)
    app = app_builder.build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join))

    app.run_polling()

if __name__ == '__main__':
    main()
