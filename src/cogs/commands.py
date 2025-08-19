import discord
from discord.ext import commands


class GeneralCommands(commands.Cog):
    """General commands like hello, assign, poll, etc."""

    def __init__(self, bot):
        self.bot = bot

    # Command: hello → greets the user
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}!")

    # Command: assign @user RoleName → Admins can assign roles
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

    # Command: remove @user RoleName → Admins can remove roles
    @commands.command()
    @commands.has_role("Administrator")
    async def remove(self, ctx, member: discord.Member, *, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await member.remove_roles(role)
            await ctx.send(f"{member.mention} has been removed from {role} ❌")
        else:
            await ctx.send("❌ Role doesn't exist")

    # Command: secret → Only Admins can use
    @commands.command()
    @commands.has_role("Administrator")
    async def secret(self, ctx):
        await ctx.send("🤫 Welcome to the secret service!")

    @secret.error
    async def secret_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("❌ You don't have permission for this command!")

    # Command: reply → Replies directly to user’s last message
    @commands.command()
    async def reply(self, ctx):
        await ctx.reply("This is a reply to your message!")

    # Command: dm message → Sends DM to self
    @commands.command()
    async def dm(self, ctx, *, msg):
        await ctx.author.send(f"You said: {msg}")

    # Command: poll Question → Creates poll with 👍 👎 reactions
    @commands.command()
    async def poll(self, ctx, *, question):
        embed = discord.Embed(title="📊 Poll", description=question)
        poll_message = await ctx.send(embed=embed)
        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")

    # Command: ping -> check bot latency
    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # Convert to ms
        await ctx.send(f"🏓 Pong! Latency: {latency}ms")

    # Command: invite → Generates server invite link
    @commands.command()
    async def invite(self, ctx):
        invite_link = await ctx.channel.create_invite(
            max_age=3600, max_uses=5, reason="Invite requested"  # 1 hour  # 5 uses
        )
        await ctx.send(f"🔗 Here is your invite link: {invite_link}")

    # Command: serverinfo → Displays server information
    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title=f"Server Info: {guild.name}",
            description=guild.description or "No description",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(
            name="Created At", value=guild.created_at.strftime("%Y-%m-%d"), inline=True
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        await ctx.send(embed=embed)

    # Command: userinfo → Displays user information
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title=f"User Info: {member.name}",
            description=member.mention,
            color=discord.Colour.blue(),
        )
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(
            name="Joined At",
            value=member.joined_at.strftime("%Y-%m-%d"),
            inline=True,
        )
        embed.add_field(
            name="Created At",
            value=member.created_at.strftime("%Y-%m-%d"),
            inline=True,
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
