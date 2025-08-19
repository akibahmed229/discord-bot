import os
import threading
from dotenv import load_dotenv
from flask import Flask
import asyncio

load_dotenv()

# Internal imports
from src.bot import bot, token, load_cogs

host = os.getenv("HOST")
port = os.getenv("PORT")

app = Flask("")


@app.route("/")
def home():
    return "Discord Bot 🆗!"


def run_flask():
    app.run(host=host, port=port)


if __name__ == "__main__":
    threading.Thread(target=run_flask).start()

    async def main():
        await load_cogs()
        await bot.start(token)

    asyncio.run(main())
