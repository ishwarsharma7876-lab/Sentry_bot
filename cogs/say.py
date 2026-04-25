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
        +say #channel Your message https://image-link.com/img.png
        """

        try:
            file = None
            embed = None

            # Check if user attached a file
            if ctx.message.attachments:
                attachment = ctx.message.attachments[0]
                file = await attachment.to_file()

                embed = discord.Embed(description=message or "", color=0x71368A)
                embed.set_image(url=f"attachment://{file.filename}")

                await channel.send(embed=embed, file=file)

            else:
                # Check if message contains image URL
                if message and ("http://" in message or "https://" in message):
                    embed = discord.Embed(description=message, color=0x71368A)
                    embed.set_image(url=message.split()[-1])  # last word as URL
                    await channel.send(embed=embed)
                else:
                    # Normal message
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
