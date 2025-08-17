import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# setup environment variable
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# log event
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

# Giving the bot permission
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Referenceing Bot using !
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Hello From Above, {bot.user.name}")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the Server! {member.name} 😄")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "fuck" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} dont't use that word! 😠")

    await bot.process_commands(message)


# !hello trigger
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
