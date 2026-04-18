# cogs/react.py
import discord
from discord.ext import commands

class React(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="react")
    @commands.has_permissions(manage_messages=True)   # Only staff can use this
    async def react(self, ctx, emoji: str = None):
        """Usage: +react [emoji] 
        Reply to a message or provide message ID"""

        if not emoji:
            return await ctx.send("❌ Please provide an emoji. Example: `+react ❤️‍🔥`", delete_after=10)

        # Check if replying to a message
        if ctx.message.reference:
            target_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        else:
            # If no reply, try to use the next argument as message ID (optional)
            try:
                message_id = int(emoji)
                target_message = await ctx.channel.fetch_message(message_id)
                emoji = ctx.message.content.split()[2]  # Get emoji from command
            except:
                return await ctx.send("❌ Reply to a message or provide a valid message ID.", delete_after=10)

        try:
            # Add the reaction
            await target_message.add_reaction(emoji)
            
            # Delete the +react command message
            await ctx.message.delete()
            
            # Optional: Send confirmation (ephemeral style but since delete, just silent)
            # await ctx.send("✅ Reacted successfully!", delete_after=5)
            
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to react: {e}", delete_after=10)
        except Exception as e:
            await ctx.send(f"❌ Error: {e}", delete_after=10)


async def setup(bot):
    await bot.add_cog(React(bot))
    print("React command loaded")