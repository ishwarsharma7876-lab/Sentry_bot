import discord
from discord.ext import commands
import google.generativeai as genai
import os

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Configure Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Ignore commands
        if message.content.startswith("+"):
            return

        # ✅ Only reply when bot is mentioned
        if self.bot.user.mentioned_in(message):
            try:
                prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

                if not prompt:
                    return await message.reply("👀 Say something after mentioning me!")

                response = self.model.generate_content(prompt)

                reply = response.text[:2000]  # Discord limit

                await message.reply(reply)

            except Exception as e:
                await message.reply("❌ AI error, try again later.")

async def setup(bot):
    await bot.add_cog(AI(bot))
