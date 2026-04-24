import discord
from discord.ext import commands
import os
import asyncio

# ======================
# INTENTS
# ======================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# ======================
# BOT SETUP
# ======================
bot = commands.Bot(command_prefix="+", intents=intents)

# ======================
# REGISTER VIEWS (IMPORTANT)
# ======================
# Register persistent views BEFORE bot starts
try:
    from cogs.tickets import PersistentTicketView, CloseTicketView as OldCloseView
    bot.add_view(PersistentTicketView())
    bot.add_view(OldCloseView())
    print("✅ Old ticket views registered")
except Exception as e:
    print(f"❌ Old ticket view error: {e}")

try:
    from cogs.secure_tickets import SecurePanelView, CloseTicketView as SecureCloseView
    bot.add_view(SecurePanelView())
    bot.add_view(SecureCloseView())
    print("✅ Secure ticket views registered")
except Exception as e:
    print(f"❌ Secure ticket view error: {e}")
    
# ======================
# ON READY
# ======================
@bot.event
async def on_ready():
    print(f"🔥 Logged in as {bot.user} (ID: {bot.user.id})")
    print("🚀 Bot is ready!\n")

# ======================
# AUTO LOAD ALL COGS
# ======================
async def load_cogs():
    if not os.path.exists("cogs"):
        print("❌ 'cogs' folder not found!")
        return

    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"✅ Loaded → {cog_name}")
            except Exception as e:
                print(f"❌ Failed to load {cog_name}: {e}")

# ======================
# MAIN START
# ======================
async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("BOT_TOKEN"))

# ======================
# RUN
# ======================
if __name__ == "__main__":
    asyncio.run(main())
