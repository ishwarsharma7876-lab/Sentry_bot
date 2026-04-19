import discord
from discord.ext import commands
import google.generativeai as genai
import os

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        # ✅ NEW WORKING MODEL
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith("+"):
            return

        if self.bot.user.mentioned_in(message):
            try:
                prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

                if not prompt:
                    return await message.reply("👀 Say something!")

                async with message.channel.typing():
                    response = self.model.generate_content(prompt)

                reply = response.text[:2000]
                await message.reply(reply)

            except Exception as e:
                print("FULL ERROR:", e)
                await message.reply(f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(AI(bot))
