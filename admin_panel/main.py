from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

PASSWORD = "admin123"
SESSION = {"logged_in": False}
CHANNEL_FILE = "channels.json"


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