from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
import requests
import os

API_URL = "http://palma-forum.io/api/posts/telegram-post"
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: CallbackContext):
    if update.channel_post:
        content = update.channel_post.text or ""

        data = {
            "content": content,
        }

        try:
            headers = {
                "X-Secret-Key": "secret"
            }

            requests.post(API_URL, json=data, headers=headers)
        except Exception as e:
            print(f"Ошибка при отправке данных: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Bot started")

app.run_polling()