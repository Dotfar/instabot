from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio

# دریافت توکن از Railway
TOKEN='6368579330:AAFfXOvMLYDdKHkSsw9hvQ512klIpQxrBmg'


# سرور ساده برای Railway
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# دستور استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! خوش اومدی به ربات من 🌟")

# اجرای ربات
async def main():
    keep_alive()
    bot = ApplicationBuilder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    await bot.run_polling()

# شروع برنامه
if __name__ == '__main__':
    asyncio.run(main())
