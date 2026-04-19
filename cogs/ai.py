import discord
from discord.ext import commands
import google.generativeai as genai
import os
import warnings

# 🔕 Hide deprecation warning
warnings.filterwarnings("ignore")

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # 🔑 Configure API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)

        # ✅ WORKING MODEL (no 404 error)
        self.model = genai.GenerativeModel("gemini-pro")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bots
        if message.author.bot:
            return

        # Ignore commands
        if message.content.startswith("+"):
            return

        # ✅ Trigger only when bot is mentioned
        if self.bot.user.mentioned_in(message):
            try:
                # Remove bot mention
                prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

                # Empty message check
                if not prompt:
                    return await message.reply("👀 Say something after mentioning me!")

                # Optional: typing effect
                async with message.channel.typing():
                    response = self.model.generate_content(prompt)

                # Safe response
                reply = response.text if response.text else "🤖 No response generated."

                # Discord limit
                reply = reply[:2000]

                await message.reply(reply)

            except Exception as e:
                print("🔥 GEMINI FULL ERROR:", e)
                await message.reply(f"❌ Error: {e}")

# 🔌 Load cog
async def setup(bot):
    await bot.add_cog(AI(bot))
