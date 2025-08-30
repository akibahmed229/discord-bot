import discord
import platform
from discord.ext import commands
import logging
import os

# 🔹 Load environment variables (like DISCORD_TOKEN from .env)
prefix = os.getenv("PREFIX")
announce_channel_id = int(os.getenv("ANNOUNCE_CHANNEL_ID", 0))

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class LoggingFormattter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)


# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormattter())

# Setup logging to file and console
log_file_path = os.path.join(os.path.dirname(__file__), "..", "discord.log")
file_handler = logging.FileHandler(filename=log_file_path, encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=prefix,
            intents=intents,
            help_command=None,
        )

        self.logger = logger
        self.bot_prefix = prefix

    async def load_cogs(self) -> None:
        """Dynamically load all cogs from src/cogs"""
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py") and not file.startswith("_"):
                extension = f"src.cogs.{file[:-3]}"
                try:
                    await self.load_extension(extension)
                    self.logger.info(f"✅ Loaded extension: {extension}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        self.logger.info(f"✅ Logged in as {self.user.name}")
        self.logger.info(f"✅ discord.py API version: {discord.__version__}")
        self.logger.info(f"✅ Python version: {platform.python_version()}")
        self.logger.info(
            f"✅ Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info("-------------------")
        await self.load_cogs()
