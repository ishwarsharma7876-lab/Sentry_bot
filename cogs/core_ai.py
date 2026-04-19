import discord
from discord.ext import commands
from groq import Groq
import os
import time

class CoreAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.user_last_message = {}

        # 🔥 Spam cooldown (light protection)
        self.cooldown = 2  

    # =========================
    # 📢 SAY COMMAND
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message: str):
        await channel.send(message)
        await ctx.send(f"✅ Sent in {channel.mention}")

    # =========================
    # 🧠 MAIN LISTENER
    # =========================
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # =========================
        # ⚡ LIGHT ANTI-SPAM
        # =========================
        now = time.time()
        last = self.user_last_message.get(message.author.id, 0)

        if now - last < self.cooldown:
            return  # silently ignore spam (no delete)

        self.user_last_message[message.author.id] = now

        # =========================
        # 🤖 AI CONTROL SYSTEM
        # =========================
        if self.bot.user.mentioned_in(message):
            try:
                prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

                if not prompt:
                    return

                # 🔥 Auto get commands
                command_names = [cmd.name for cmd in self.bot.commands]

                intent = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                f"Available commands: {', '.join(command_names)}\n\n"
                                f"If user wants a command, return exact command name.\n"
                                f"If user wants to send message to a channel, return: send\n"
                                f"Otherwise return: none\n"
                                f"ONLY return one word."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ]
                )

                result = intent.choices[0].message.content.strip().lower()

                # =========================
                # ⚙️ COMMAND EXECUTION
                # =========================
                if result in command_names:
                    command = self.bot.get_command(result)
                    if command:
                        ctx = await self.bot.get_context(message)
                        return await ctx.invoke(command)

                # =========================
                # 📢 SEND MESSAGE TO CHANNEL
                # =========================
                if result == "send":
                    for ch in message.guild.text_channels:
                        if ch.name in prompt.lower():
                            msg = prompt.lower().replace(ch.name, "").strip()
                            await ch.send(msg)
                            await message.reply(f"✅ Sent in #{ch.name}")
                            return

            except Exception as e:
                print("AI ERROR:", e)

    # =========================
    # 📝 DELETE LOG
    # =========================
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild:
            return

        log_channel = discord.utils.get(message.guild.text_channels, name="logs")
        if log_channel and message.author:
            await log_channel.send(
                f"🗑️ {message.author} deleted:\n{message.content}"
            )

    # =========================
    # ✏️ EDIT LOG
    # =========================
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.guild:
            return

        log_channel = discord.utils.get(before.guild.text_channels, name="logs")
        if log_channel:
            await log_channel.send(
                f"✏️ {before.author} edited:\nBefore: {before.content}\nAfter: {after.content}"
            )

async def setup(bot):
    await bot.add_cog(CoreAI(bot))
