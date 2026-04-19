from groq import Groq
import discord
from discord.ext import commands
import os

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
                    chat = self.client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile"  # ✅ FIXED MODEL
                    )

                reply = chat.choices[0].message.content[:2000]
                await message.reply(reply)

            except Exception as e:
                print("ERROR:", e)
                await message.reply(f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(AI(bot))
