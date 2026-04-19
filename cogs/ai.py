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
                    return await message.reply("Hey... say something 😊")

                async with message.channel.typing():
                    chat = self.client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a warm, friendly, emotionally intelligent AI. "
                                    "Talk like a close friend. Be supportive, slightly playful, "
                                    "and natural. Use simple language. Sometimes use emojis 😊. "
                                    "Don't sound robotic or like a teacher. Keep replies engaging."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.9  # 🔥 makes it more human-like
                    )

                reply = chat.choices[0].message.content[:2000]
                await message.reply(reply)

            except Exception as e:
                print("ERROR:", e)
                await message.reply("Hmm... something went wrong 😔")

async def setup(bot):
    await bot.add_cog(AI(bot))
