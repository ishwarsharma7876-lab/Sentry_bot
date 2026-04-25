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
        +say #channel Your message
        +say #channel Your message + attach image
        """

        try:
            # Check for attachment (image/file)
            if ctx.message.attachments:
                attachment = ctx.message.attachments[0]
                file = await attachment.to_file()

                await channel.send(content=message or None, file=file)
            else:
                # Only message
                await channel.send(message)

            await ctx.send(f"✅ Message sent to {channel.mention}", delete_after=6)

            try:
                await ctx.message.delete()
            except:
                pass

        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to send messages in that channel.")
        except Exception as e:
            await ctx.send(f"❌ Failed to send: {e}")


async def setup(bot):
    await bot.add_cog(Say(bot))
