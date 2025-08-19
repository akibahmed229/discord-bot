import discord
from discord.ext import commands
import logging
import os

# 🔹 Load environment variables (like DISCORD_TOKEN from .env)
token = os.getenv("DISCORD_TOKEN")
prefix = os.getenv("PREFIX")
announce_channel_id = int(os.getenv("ANNOUNCE_CHANNEL_ID", 0))

# 🔹 Setup logging (only file, no console)
log_file_path = os.path.join(os.path.dirname(__file__), "..", "discord.log")
handler = logging.FileHandler(filename=log_file_path, encoding="utf-8", mode="w")

logging.basicConfig(
    level=logging.INFO,  # change to DEBUG if you want more detail
    handlers=[handler],  # only file logging
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# 🔹 Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# 🔹 Bot instance
bot = commands.Bot(command_prefix=prefix, intents=intents)


# Cog loader
async def load_cogs():
    """Dynamically load all cogs from src/cogs"""
    for ext in ["src.cogs.commands", "src.cogs.events"]:
        await bot.load_extension(ext)


__all__ = ["bot", "handler", "token", "announce_channel_id", "load_cogs"]
