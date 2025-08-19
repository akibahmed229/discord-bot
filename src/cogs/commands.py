import discord
from discord.ext import commands


class GeneralCommands(commands.Cog):
    """General commands like hello, assign, poll, etc."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}!")

    @commands.command()
    @commands.has_role("Administrator")
    async def assign(self, ctx, member: discord.Member, *, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await member.add_roles(role)
            await ctx.send(
                f"{member.mention} has been assigned the role {role_name} ✅"
            )
        else:
            await ctx.send("❌ Role doesn't exist")

    @commands.command()
    async def remove(self, ctx, member: discord.Member, *, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await member.remove_roles(role)
            await ctx.send(f"{member.mention} has been removed from {role} ❌")
        else:
            await ctx.send("❌ Role doesn't exist")

    @commands.command()
    @commands.has_role("Administrator")
    async def secret(self, ctx):
        await ctx.send("🤫 Welcome to the secret service!")

    @secret.error
    async def secret_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("❌ You don't have permission for this command!")

    @commands.command()
    async def dm(self, ctx, *, msg):
        await ctx.author.send(f"You said: {msg}")

    @commands.command()
    async def reply(self, ctx):
        await ctx.reply("This is a reply to your message!")

    @commands.command()
    async def poll(self, ctx, *, question):
        embed = discord.Embed(title="📊 Poll", description=question)
        poll_message = await ctx.send(embed=embed)
        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")


async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
