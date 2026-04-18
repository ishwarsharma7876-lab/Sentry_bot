# main.py
import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Register persistent views (very important for tickets, payment editor, close buttons, etc.)
    try:
        from cogs.tickets import PersistentTicketView, CloseTicketView
        bot.add_view(PersistentTicketView())
        bot.add_view(CloseTicketView())
        print("✅ Ticket views registered successfully")
    except Exception as e:
        print(f"❌ Ticket view registration failed: {e}")

    try:
        from cogs.payment import PaymentSelectView
        bot.add_view(PaymentSelectView(bot))
        print("✅ Payment view registered")
    except Exception as e:
        print(f"❌ Payment view registration failed: {e}")

    print("Bot is ready!\n")


# ====================== AUTO LOAD ALL COGS ======================
async def load_cogs():
    if not os.path.exists("cogs"):
        print("❌ 'cogs' folder not found!")
        return

    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"Loaded → {cog_name}")
            except Exception as e:
                print(f"Failed to load {cog_name}: {e}")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("BOT_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
