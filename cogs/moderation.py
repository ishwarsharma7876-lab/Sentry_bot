from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member} kicked. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member} banned. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Cleared {amount} messages", delete_after=3)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: commands.MemberConverter, *, reason="No reason"):
        self.warnings[member.id] = self.warnings.get(member.id, 0) + 1
        await ctx.send(f"⚠️ {member} warned ({self.warnings[member.id]} warns)")

    @commands.command()
    async def warns(self, ctx, member: commands.MemberConverter):
        count = self.warnings.get(member.id, 0)
        await ctx.send(f"{member} has {count} warnings")

async def setup(bot):
    await bot.add_cog(Moderation(bot))