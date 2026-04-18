import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Register persistent views here if you have any (ticket, payment, etc.)
    print("Bot is ready!")

# Load all cogs
async def main():
    async with bot:
        await bot.load_extension("cogs.tickets")
        await bot.load_extension("cogs.welcome")
        await bot.load_extension("cogs.vouch")
        await bot.load_extension("cogs.react")
        await bot.load_extension("cogs.payment")
        # add other cogs like moderation, embed_builder etc.
        await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
