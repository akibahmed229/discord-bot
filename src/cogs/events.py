import discord
from discord.ext import commands
from src.bot import announce_channel_id


class GeneralEvents(commands.Cog):
    """Events like join, leave, delete, bad words"""

    def __init__(self, bot):
        self.bot = bot

    #  Event: When a new member joins
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send(f"Welcome to the Server! {member.name} 😄")
        role = discord.utils.get(member.guild.roles, name="Member")
        if role:
            try:
                await member.add_roles(role)
                print(f"✅ Added role {role.name} to {member.name}")
            except discord.Forbidden:
                print("❌ Missing permissions to assign roles!")
        else:
            print("❌ Role 'Member' not found")

    #  Event: Watch every message
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot's own messages
        if message.author == self.bot.user:
            return

        # Delete & warn if someone use bad word
        if any(word in message.content.lower() for word in ["fuck", "suck", "dick"]):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, don't use that word! 😠"
            )
            return

        # command list on "!"
        if message.content.strip() == "!":
            commands_list = [cmd.name for cmd in self.bot.commands]
            commands_text = "\n".join([f"• !{c}" for c in commands_list])
            embed = discord.Embed(
                title="🤖 Available Commands",
                description=commands_text,
                color=discord.Colour.blue(),
            )
            await message.channel.send(embed=embed)
            return

    # Event: When a member leaves or is removed
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(announce_channel_id)
        if channel:
            await channel.send(f"👋 {member.mention} has left the server.")

    # Event: When a member is banned
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = self.bot.get_channel(announce_channel_id)
        if channel:
            await channel.send(f"❌ {user.mention} has been banned from the server.")

    # Event: When a member delete a message
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
        if any(word in message.content.lower() for word in ["fuck", "suck", "dick"]):
            return
        msg = f"{message.author} has deleted the last message"
        await message.channel.send(msg)


async def setup(bot):
    await bot.add_cog(GeneralEvents(bot))
