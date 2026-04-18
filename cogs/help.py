# cogs/help.py
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")  # Remove default help to avoid conflict

    @commands.command(name="help")
    async def help_command(self, ctx, command_name: str = None):
        if command_name is None:
            # Show all commands grouped nicely
            embed = discord.Embed(
                title="🔰 VOID SPACE Bot Help",
                description="Here are all available commands:",
                color=0x71368A
            )

            embed.add_field(
                name="🎟️ Tickets",
                value="`+ticketpanel` — Show ticket creation panel\n`+close` — Close current ticket",
                inline=False
            )

            embed.add_field(
                name="💳 Payments",
                value="`+payment` — Show payment methods\n`+paymentedit` — Edit payment methods",
                inline=False
            )

            embed.add_field(
                name="👋 Welcome & Others",
                value="`+react <emoji>` — React to a message (reply to it)",
                inline=False
            )

            embed.set_footer(text="Use +help <command> for more details | VOID SPACE")
            await ctx.send(embed=embed)

        else:
            # Specific command help
            cmd = self.bot.get_command(command_name.lower())
            if cmd:
                embed = discord.Embed(
                    title=f"Command: +{cmd.name}",
                    description=cmd.help or "No description available.",
                    color=0x71368A
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Command `+{command_name}` not found.")

async def setup(bot):
    await bot.add_cog(Help(bot))
    print("Help command loaded")
