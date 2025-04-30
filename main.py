import asyncio
import json
import os

import requests

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
from telegram.ext import ApplicationBuilder, filters, CommandHandler, ContextTypes, MessageHandler

from telethon import TelegramClient, events

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


import uvicorn
from threading import Thread

#--------CONST--------

API_URL = "http://localhost:3000/api/posts/telegram-post"
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "http://127.0.0.1:8000/admin"
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

PASSWORD = "admin123"
SESSION = {"logged_in": False}
CHANNEL_FILE = "../channels.json"

#--------FastAPI--------

app = FastAPI()
app.mount("../static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def load_channels():
    with open(CHANNEL_FILE, "r") as f:
        return json.load(f)


def save_channels(channels):
    with open(CHANNEL_FILE, "w") as f:
        json.dump(channels, f)


def is_logged_in():
    return SESSION["logged_in"]


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(password: str = Form(...)):
    if password == PASSWORD:
        SESSION["logged_in"] = True
        return RedirectResponse("/admin", status_code=302)
    return RedirectResponse("/", status_code=302)


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    if not is_logged_in():
        return RedirectResponse("/", status_code=302)
    channels = load_channels()
    return templates.TemplateResponse("admin.html", {"request": request, "channels": channels})


@app.post("/add")
async def add_channel(channel: str = Form(...)):
    if not is_logged_in():
        return RedirectResponse("/", status_code=302)
    channels = load_channels()
    if channel not in channels:
        channels.append(channel)
        save_channels(channels)
    return RedirectResponse("/admin", status_code=302)


@app.post("/delete")
async def delete_channel(channel: str = Form(...)):
    if not is_logged_in():
        return RedirectResponse("/", status_code=302)
    channels = load_channels()
    if channel in channels:
        channels.remove(channel)
        save_channels(channels)
    return RedirectResponse("/admin", status_code=302)

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

#--------Admin Button--------

async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Открыть админ-панель", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await update.message.reply_text("Нажми кнопку ниже для входа в админку:", reply_markup=keyboard)

async def run_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.ALL, start_bot))

    print("Bot started")

    app_bot.run_polling()

#--------Telethon--------

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

#--------Async start--------

async def main():
    Thread(target=run_fastapi, daemon=True).start()

    await asyncio.gather(
        run_telethon(),
        run_bot()
    )

asyncio.run(main())