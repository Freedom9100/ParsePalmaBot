import asyncio
from telethon_client.client import run_telethon
from telegram_bot.bot import run_bot
import uvicorn

async def main():
    await asyncio.gather(
        run_telethon(),
        run_bot(),
        run_api()
    )

async def run_api():
    config = uvicorn.Config("api.main:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())