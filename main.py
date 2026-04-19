import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="+", intents=intents)

# 🔥 Prevent multiple on_ready runs
bot.ready = False


# ====================== READY EVENT ======================
@bot.event
async def on_ready():
    if bot.ready:
        return  # 🚫 prevents duplicate execution

    bot.ready = True

    print(f"Logged in as {bot.user}")

    # ====================== REGISTER VIEWS ======================
    try:
        from cogs.tickets import PersistentTicketView, CloseTicketView
        bot.add_view(PersistentTicketView())
        bot.add_view(CloseTicketView())
        print("✅ Ticket views registered")
    except Exception as e:
        print(f"❌ Ticket view error: {e}")

    try:
        from cogs.payment import PaymentSelectView
        bot.add_view(PaymentSelectView(bot))
        print("✅ Payment view registered")
    except Exception as e:
        print(f"❌ Payment view error: {e}")

    print("✅ Bot is fully ready!\n")


# ====================== AUTO LOAD COGS ======================
async def load_cogs():
    if not os.path.exists("cogs"):
        print("❌ 'cogs' folder not found!")
        return

    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            cog = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog)
                print(f"✅ Loaded → {cog}")
            except Exception as e:
                print(f"❌ Failed → {cog}: {e}")


# ====================== MAIN START ======================
async def main():
    async with bot:
        await load_cogs()  # 🔥 auto loads everything
        await bot.start(os.getenv("BOT_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
