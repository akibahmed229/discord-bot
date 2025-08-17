from flask import Flask
from threading import Thread
from dotenv import load_dotenv
import os

# 🔹 Load environment variables (like DISCORD_TOKEN from .env)
load_dotenv()
host = os.getenv("HOST")
port = os.getenv("PORT")


app = Flask("")


@app.route("/")
def home():
    return "Discord Bot 🆗!"


def run():
    app.run(host=host, port=port)


def kee_alive():
    t = Thread(target=run)
    t.start()
