# External imports
from flask import Flask
import threading
import os
import logging
from dotenv import load_dotenv

# Load environment variables (like DISCORD_TOKEN from .env)
load_dotenv()

# internal imports
from src import bot, handler, token

host = os.getenv("HOST")
port = os.getenv("PORT")

app = Flask("")


@app.route("/")
def home():
    return "Discord Bot 🆗!"


# run web server
def run_flask():
    """Run Flask server in separate thread for Render health check"""
    app.run(host=host, port=port)


if __name__ == "__main__":
    # Start Flask in a thread
    threading.Thread(target=run_flask).start()

    # Start Discord bot
    bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
