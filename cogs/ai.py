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
                    return await message.reply("Say something 😄")

                # 🔥 GET ALL COMMANDS AUTOMATICALLY
                command_names = [cmd.name for cmd in self.bot.commands]

                # 🔥 AI CHOOSES COMMAND
                intent = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                f"You are a command classifier.\n"
                                f"Available commands: {', '.join(command_names)}\n\n"
                                f"Return ONLY the exact command name from the list.\n"
                                f"If none match, return: chat"
                            )
                        },
                        {"role": "user", "content": prompt}
                    ]
                )

                result = intent.choices[0].message.content.strip().lower()

                # 🔥 AUTO EXECUTE COMMAND
                if result != "chat":
                    command = self.bot.get_command(result)
                    if command:
                        ctx = await self.bot.get_context(message)
                        return await ctx.invoke(command)

                # 🔥 NORMAL CHAT
                chat = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a friendly, emotional AI. Talk like a close friend."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9
                )

                reply = chat.choices[0].message.content[:2000]
                await message.reply(reply)

            except Exception as e:
                print("ERROR:", e)
                await message.reply("Something went wrong 😔")

async def setup(bot):
    await bot.add_cog(AI(bot))
