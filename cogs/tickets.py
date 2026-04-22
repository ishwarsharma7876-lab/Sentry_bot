import discord
from discord.ext import commands
from discord.ui import View, Select, Button
from discord import SelectOption, Interaction
import json
import os

CONFIG_PATH = "/app/data/ticket_config.json"
TRANSCRIPT_CHANNEL_ID = 1461842853209833655


def load_ticket_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_ticket_config(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

# ================================================
# Ticket Creation Panel
# ================================================
class PersistentTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

        options = [
            SelectOption(label="Buy Accounts / Enquiries",        value="buy_accounts", emoji="<:coc:1462053918740844709>"),
            SelectOption(label="Walls Maxing / Farming",          value="walls_farming", emoji="<:walls:1462055575717150974>"),
            SelectOption(label="Capital Raids / Capital Golds",   value="capital_raids", emoji="<:clancapital:1461849162248224788>"),
            SelectOption(label="Showcase / CWL Base",             value="custom_base", emoji="<:builder:1462058517904101510>"),
            SelectOption(label="Gold / Event Pass Purchase",      value="gold_purchase", emoji="<:goldpass:1461847049250275570>"),
            SelectOption(label="Raffle Tickets",                  value="raffle", emoji="<:vticket:1472623749089071315>"),
        ]

        select = Select(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="void_ticket_select_v5"
        )
        select.callback = self.create_ticket
        self.add_item(select)

    async def create_ticket(self, interaction: Interaction):
        value = interaction.data["values"][0]

        guild = interaction.guild
        user = interaction.user

        config = load_ticket_config().get(str(guild.id), {})
        category_id = config.get("ticket_category_id")

        existing = [ch for ch in guild.text_channels if ch.name.startswith("ticket-")]
        ticket_number = len(existing) + 1
        ticket_name = f"ticket-{ticket_number:05d}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True),
        }

        topic = f"Ticket: {value.replace('_',' ').title()} | UserID:{user.id}"

        if category_id:
            category = guild.get_channel(category_id)
            if isinstance(category, discord.CategoryChannel):
                channel = await category.create_text_channel(name=ticket_name, topic=topic, overwrites=overwrites)
            else:
                channel = await guild.create_text_channel(name=ticket_name, topic=topic, overwrites=overwrites)
        else:
            channel = await guild.create_text_channel(name=ticket_name, topic=topic, overwrites=overwrites)

        # ✅ UPDATED MESSAGE (ONLY CHANGE)
        embed = discord.Embed(
            title="#VOID Support Terminal",
            description=(
                "Meanwhile tell us what you’re here for:\n"
                "• Account Purchase\n"
                "• Gold or Event Pass Purchase\n"
                "• COC Services (farming, raids, bases, etc.)\n"
                "• Raffle Tickets\n\n"
                "The VOID Team will be with you shortly."
            ),
            color=0x71368A
        )
        embed.set_footer(text="VOID SPACE • Official Ticket System")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1461984553953657004/1472633716307263628/Add_a_heading.jpg")

        await channel.send(
            content=f"Hey {user.mention}!  You've entered a safe space!  Kindly wait, <@223110396871966728> / <@645693323104878623> will assist you soon!",
            embed=embed
        )

        close_view = CloseTicketView()
        await channel.send("**Click below to close this ticket**", view=close_view)

        await interaction.response.send_message(f"✅ Ticket created → {channel.mention}", ephemeral=True)

# ================================================
# Close Ticket Button
# ================================================
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🔒")
    async def ask_close(self, interaction: Interaction, button: Button):
        confirm_view = ConfirmCloseView(interaction.channel)

        embed = discord.Embed(
            title="Are you sure you want to close this ticket?",
            description="This ticket will be completely removed after closing.",
            color=0x71368A
        )

        await interaction.response.send_message(embed=embed, view=confirm_view)

# ================================================
# Confirm Close
# ================================================
class ConfirmCloseView(View):
    def __init__(self, channel: discord.TextChannel):
        super().__init__(timeout=180)
        self.channel = channel

    @discord.ui.button(label="Send Transcript", style=discord.ButtonStyle.blurple, emoji="📜")
    async def send_transcript(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message("❌ Only staff can send transcripts.", ephemeral=True)

        transcript_channel = interaction.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
        if not transcript_channel:
            return await interaction.response.send_message("❌ Transcript channel not found.", ephemeral=True)

        messages = []
        async for msg in self.channel.history(limit=100):
            time = msg.created_at.strftime("%H:%M")
            messages.append(f"[{time}] {msg.author}: {msg.content}")

        transcript_text = "\n".join(reversed(messages))

        await transcript_channel.send(
            f"**Transcript for {self.channel.name}**\nClosed by {interaction.user.mention}\n\n```{transcript_text}```"
        )

        await interaction.response.send_message("📜 Transcript sent!", ephemeral=True)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="❌")
    async def yes_close(self, interaction: Interaction, button: Button):
        await interaction.response.defer()
        await self.channel.delete(reason=f"Closed by {interaction.user}")

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.green, emoji="✅")
    async def cancel(self, interaction: Interaction, button: Button):
        await interaction.response.send_message("Cancelled.", ephemeral=True)
        self.stop()

# ================================================
# Commands
# ================================================
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticketpanel(self, ctx):
        embed = discord.Embed(
            title="✦ VOID SUPPORT TERMINAL ✦",
            description="Use this ticket to purchase COC accounts\nor access VOID-approved services.",
            color=0x71368A
        )
        embed.set_footer(text="VOID SPACE OFFICIAL TICKET TOOL")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1461984553953657004/1472633716307263628/Add_a_heading.jpg")

        await ctx.send(embed=embed, view=PersistentTicketView())

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setticketcategory(self, ctx, category: discord.CategoryChannel):
        config = load_ticket_config()
        gid = str(ctx.guild.id)

        if gid not in config:
            config[gid] = {}

        config[gid]["ticket_category_id"] = category.id
        save_ticket_config(config)

        await ctx.send(f"✅ Tickets will now be created in: **{category.name}**")

    @commands.command()
    async def close(self, ctx):
        if "ticket-" not in ctx.channel.name:
            return await ctx.send("❌ Use this inside a ticket.", delete_after=8)

        is_staff = ctx.author.guild_permissions.manage_channels
        is_creator = str(ctx.author.id) in (ctx.channel.topic or "")

        if not (is_staff or is_creator):
            return await ctx.send("❌ Only creator or staff can close.", delete_after=8)

        embed = discord.Embed(
            title="Are you sure you want to close this ticket?",
            description="This ticket will be deleted.",
            color=0x71368A
        )

        await ctx.send(embed=embed, view=ConfirmCloseView(ctx.channel))

async def setup(bot):
    await bot.add_cog(Tickets(bot))
