import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import threading
from server import app


# 🔹 Load environment variables (like DISCORD_TOKEN from .env)
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
host = os.getenv("HOST")
port = os.getenv("PORT")
announce_channel_id = int(os.getenv("ANNOUNCE_CHANNEL_ID", 0))


# 🔹 Setup logging (saves bot logs to discord.log)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

# 🔹 Define permissions/intents the bot can use
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.members = True  # Required for member join events

# 🔹 Create bot with "!" as prefix (commands start with !)
bot = commands.Bot(command_prefix="!", intents=intents)


# Event: Bot is online
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")


#  Event: When a new member joins
@bot.event
async def on_member_join(member):
    # Send welcome message in DM
    await member.send(f"Welcome to the Server! {member.name} 😄")

    # Automatically assign "Member" role
    role = discord.utils.get(member.guild.roles, name="Member")
    if role:
        await member.add_roles(role)


#  Event: Watch every message
@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Delete & warn if someone swears
    if "fuck" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, don't use that word! 😠")

    # Let other commands still work
    await bot.process_commands(message)


# Event: When a member leaves or is removed
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(announce_channel_id)
    if channel:
        await channel.send(f"👋 {member.mention} has left the server.")


# Event: When a member is banned
@bot.event
async def on_member_ban(guild, user):
    channel = bot.get_channel(announce_channel_id)
    if channel:
        await channel.send(f"❌ {user.mention} has been banned from the server.")


# Command: !hello → greets the user
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


# Command: !assign @user RoleName → Admins can assign roles
@bot.command()
@commands.has_role("Administrator")
async def assign(ctx, member: discord.Member, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} has been assigned the role {role_name} ✅")
    else:
        await ctx.send("❌ Role doesn't exist")


# Command: !remove @user RoleName → Admins can remove roles
@bot.command()
async def remove(ctx, member: discord.Member, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role:
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} has been removed from {role} ❌")
    else:
        await ctx.send("❌ Role doesn't exist")


# Command: !secret → Only Admins can use
@bot.command()
@commands.has_role("Administrator")
async def secret(ctx):
    await ctx.send("🤫 Welcome to the secret service!")


@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ You don't have permission for this command!")


# Command: !dm message → Sends DM to self
@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said: {msg}")


# Command: !reply → Replies directly to user’s last message
@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")


# Command: !poll Question → Creates poll with 👍 👎 reactions
@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="📊 Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")


# run web server
def run_flask():
    """Run Flask server in separate thread for Render health check"""
    app.run(host=host, port=port)


if __name__ == "__main__":
    # Start Flask in a thread
    threading.Thread(target=run_flask).start()

    # Start Discord bot
    bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
