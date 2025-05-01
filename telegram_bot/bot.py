from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
from telegram.ext import ApplicationBuilder, ContextTypes

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "http://127.0.0.1:8000/admin"

async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Открыть админ-панель", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await update.message.reply_text("Нажми кнопку ниже для входа в админку:", reply_markup=keyboard)

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    print("Bot started")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.wait_until_closed()