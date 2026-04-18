import discord
from discord.ext import commands
from discord.ui import View, Button
import json
import os

DATA_FILE = "/app/data/coc_bases.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


class BaseView(View):
    def __init__(self, base_id):
        super().__init__(timeout=None)
        self.base_id = base_id

    @discord.ui.button(label="🔗 Link", style=discord.ButtonStyle.primary)
    async def link_button(self, interaction: discord.Interaction, button: Button):
        data = load_data()

        if self.base_id not in data:
            await interaction.response.send_message("❌ Base not found.", ephemeral=True)
            return

        base = data[self.base_id]

        # track unique downloads
        if str(interaction.user.id) not in base["users"]:
            base["users"].append(str(interaction.user.id))
            base["downloads"] += 1
            save_data(data)

        await interaction.response.send_message(
            f"📥 **Base Link:**\n{base['link']}",
            ephemeral=True
        )

    @discord.ui.button(label="📊 Downloads", style=discord.ButtonStyle.secondary)
    async def download_list(self, interaction: discord.Interaction, button: Button):
        data = load_data()

        if self.base_id not in data:
            await interaction.response.send_message("❌ Base not found.", ephemeral=True)
            return

        base = data[self.base_id]
        users = base["users"]

        if not users:
            text = "No downloads yet."
        else:
            text = "\n".join([f"➤ <@{uid}>" for uid in users])

        embed = discord.Embed(
            title="📊 Base Downloads",
            description=text,
            color=0x71368A
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


class CoCBase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addbase")
    @commands.has_permissions(manage_messages=True)
    async def addbase(self, ctx, link, *, description):

        # ❌ No attachment
        if not ctx.message.attachments:
            await ctx.send("❌ Please attach a base image.")
            return

        attachment = ctx.message.attachments[0]

        # ✅ Convert to file (fix image loading forever)
        file = await attachment.to_file()

        base_id = str(ctx.message.id)

        data = load_data()
        data[base_id] = {
            "link": link,
            "description": description,
            "downloads": 0,
            "users": []
        }
        save_data(data)

        # 💎 BEAUTIFUL THEME
        styled_description = description

        embed = discord.Embed(
            title=" Clash of Clans Base",
            description=styled_description,
            color=0x71368A
        )

        # ✅ Use uploaded file (PERMANENT FIX)
        embed.set_image(url=f"attachment://{file.filename}")
        embed.set_footer(text="VOID SPACE")

        view = BaseView(base_id)

        await ctx.send(embed=embed, view=view, file=file)

        try:
            await ctx.message.delete()
        except:
            pass


async def setup(bot):
    await bot.add_cog(CoCBase(bot))