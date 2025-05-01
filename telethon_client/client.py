from telethon import TelegramClient, events
from telegram import Update
from telegram.ext import ContextTypes

import json
import os
import requests

API_URL = "http://localhost:3000/api/posts/telegram-post"
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

client = TelegramClient("session", api_id, api_hash)

async def run_telethon():
    with open("channels.json", "r", encoding="utf-8") as f:
        telegram_channels = json.load(f)

    @client.on(events.NewMessage(chats=telegram_channels))
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    await client.start()
    await client.run_until_disconnected()