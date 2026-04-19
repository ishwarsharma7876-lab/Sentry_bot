import discord
from discord.ext import commands
from groq import Groq
import os

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # 🔥 VERY IMPORTANT → DO NOT TOUCH COMMANDS
        if message.content.startswith("+"):
            return

        # Only respond when mentioned
        if not self.bot.user.mentioned_in(message):
            return

        try:
            # Remove bot mention
            prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

            if not prompt:
                return await message.reply("Yeah? 😄")

            async with message.channel.typing():
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a friendly and smart assistant. "
                                "Talk like a natural human. "
                                "Keep answers clear, helpful, and slightly casual. "
                                "Do NOT act like a bot. Keep it engaging."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.8
                )

            reply = response.choices[0].message.content[:2000]

            await message.reply(reply)

        except Exception as e:
            print("AI ERROR:", e)
            await message.reply("Hmm… something went wrong 😔")

async def setup(bot):
    await bot.add_cog(AIChat(bot))
