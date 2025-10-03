import asyncio
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.api import router as health_router
# Internal imports
from src.bot import DiscordBot

# Load env
load_dotenv()
host = os.getenv("HOST")
port = int(os.getenv("PORT", 8000))
token = os.getenv("DISCORD_TOKEN")

# Create FastAPI app
app = FastAPI()
app.include_router(health_router)


async def start_fastapi():
    """Run FastAPI inside same event loop"""
    config = uvicorn.Config(app=app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)

    await server.serve()


async def main():
    bot = DiscordBot()

    # Run FastAPI + Discord bot concurrently
    await asyncio.gather(bot.start(token), start_fastapi())


if __name__ == "__main__":
    asyncio.run(main())
