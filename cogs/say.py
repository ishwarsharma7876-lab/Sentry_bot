import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message: str = None):
        """
        Usage:
        +say #channel message
        + attach multiple files (images/docs/etc)
        """

        try:
            files = []

            # Collect ALL attachments (multiple supported)
            if ctx.message.attachments:
                for attachment in ctx.message.attachments:
                    file = await attachment.to_file()
                    files.append(file)

            # Send message + files (or only files / only message)
            await channel.send(
                content=message if message else None,
                files=files if files else None
            )

            await ctx.send(f"✅ Sent to {channel.mention}", delete_after=5)

            try:
                await ctx.message.delete()
            except:
                pass

        except discord.Forbidden:
            await ctx.send("❌ No permission in that channel.")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(Say(bot))
