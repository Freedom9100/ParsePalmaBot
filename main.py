from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
from telethon import TelegramClient, events
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import os
import json

API_URL = "http://localhost:3000/api/posts/telegram-post"
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = ""
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

client = TelegramClient("session", api_id, api_hash)

with open("channels.json", "r", encoding="utf-8") as f:
    telegram_channels = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Открыть админ-панель", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await update.message.reply_text("Нажми кнопку ниже для входа в админку:", reply_markup=keyboard)

@client.on(events.NewMessage(chats=telegram_channels))
async def handle_message(update: Update, context: CallbackContext):
    if update.channel_post:
        content = update.channel_post.text or ""

        data = {
            "content": content,
        }

        try:
            headers = {
                "X-Secret-Key": "R1VvGj4JMXOenOY"
            }

            requests.post(API_URL, json=data, headers=headers)
        except Exception as e:
            print(f"Ошибка при отправке данных: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Bot started")

app.run_polling()