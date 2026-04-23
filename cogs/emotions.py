# cogs/emotions.py
import discord
from discord.ext import commands
import random

class Emotions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ====================== KISS ======================
    kiss_gif = "https://cdn.discordapp.com/attachments/1461276954383749155/1495316182985740409/anime-kiss-gif-7.gif"

    kiss_messages = [
        "{author} kissed {target} deeply and passionately 💋",
        "{author} gave {target} a soft and loving kiss",
        "{author} pulled {target} close and kissed them intensely ❤️",
        "{author} sneaked a cute kiss on {target}'s lips 😘",
        "{author} kissed {target} so deeply the world stopped for a moment 💕",
        "With full love, {author} kissed {target} passionately 🔥",
    ]

    @commands.command(name="kiss")
    async def kiss(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Please mention someone to kiss! Example: `+kiss @user`")

        if member == ctx.author:
            return await ctx.send("You can't kiss yourself... or can you? 😏")

        message = random.choice(self.kiss_messages).format(
            author=ctx.author.mention,
            target=member.mention
        )

        embed = discord.Embed(description=message, color=0x71368A)
        embed.set_image(url=self.kiss_gif)

        await ctx.send(embed=embed)

    # ====================== TOUCH ======================
    touch_gifs = [
        "https://cdn.discordapp.com/attachments/1461276954383749155/1495317462671953940/animesher.com_gif-fate-rintohsaka-1777663.gif",
        "https://cdn.discordapp.com/attachments/1461276954383749155/1495317462319628308/tumblr_pdfrxwL3P31vhnny1o1_400.gif",
        "https://cdn.discordapp.com/attachments/1461276954383749155/1495317462026293258/tumblr_pdfsjua6ht1vhnny1o1_500.gif"
    ]

    touch_messages = [
        "{author} gently ran their fingers over {target}'s body",
        "{author} touched {target} teasingly 😏",
        "{author} slowly caressed {target}'s skin 🔥",
        "{author} gave {target} a sensual touch",
        "{author} traced their fingers down {target}'s back seductively",
        "{author} touched {target} in a very naughty way\~",
        "With a sly smile, {author} touched {target} intimately 💦"
    ]

    @commands.command(name="touch")
    async def touch(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Please mention someone to touch! Example: `+touch @user`")

        if member == ctx.author:
            return await ctx.send("Touching yourself? Bold... 😳")

        message = random.choice(self.touch_messages).format(
            author=ctx.author.mention,
            target=member.mention
        )

        embed = discord.Embed(description=message, color=0x71368A)
        embed.set_image(url=random.choice(self.touch_gifs))

        await ctx.send(embed=embed)

    # ====================== FUCK ======================
    fuck_gifs = [
        "https://cdn.discordapp.com/attachments/1461276954383749155/1495312139575890032/download_1.gif",
        "https://cdn.discordapp.com/attachments/1461276954383749155/1495318402544308335/download_2.gif"
    ]

    fuck_messages = [
        "{author} fucked {target} hard and deep 💦",
        "{author} pinned {target} down and went rough 😈",
        "{author} gave {target} the best night of their life 🔥",
        "{author} thrusted into {target} passionately",
        "{author} made {target} moan loudly while fucking them",
        "{author} fucked {target} senseless\~",
        "In a heated moment, {author} fucked {target} intensely 💦"
    ]

    @commands.command(name="fuck")
    async def fuck(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Please mention someone! Example: `+fuck @user`")

        if member == ctx.author:
            return await ctx.send("Sorry, self-fuck is not supported yet 😭")

        message = random.choice(self.fuck_messages).format(
            author=ctx.author.mention,
            target=member.mention
        )

        embed = discord.Embed(description=message, color=0x71368A)
        embed.set_image(url=random.choice(self.fuck_gifs))

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Emotions(bot))
    print("Emotions (kiss, touch, fuck) system loaded")
