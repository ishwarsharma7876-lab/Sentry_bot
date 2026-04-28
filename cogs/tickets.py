# cogs/tickets.py
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
#  Ticket Creation Panel
# ================================================
class PersistentTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

        options = [
            SelectOption(label="Buy Accounts / Enquiries",        value="buy_accounts",       emoji="<:coc:1462053918740844709>"),
            SelectOption(label="Walls Maxing / Farming",          value="walls_farming",      emoji="<:walls:1462055575717150974>"),
            SelectOption(label="Capital Raids / Capital Golds",   value="capital_raids",      emoji="<:clancapital:1461849162248224788>"),
            SelectOption(label="Showcase Bases",                  value="showcase_bases",     emoji="<:Builder:1488534056554598452>"),
            SelectOption(label="CWL Base Packs",                  value="cwl_base_packs",     emoji="<:cyberqueen:1461710904885514354>"),  # Fixed value
            SelectOption(label="Gold / Event Pass Purchase",      value="gold_purchase",      emoji="<:goldpass:1461847049250275570>"),
            SelectOption(label="Raffle Tickets",                  value="raffle",             emoji="<:vticket:1472623749089071315>"),
        ]

        select = Select(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="void_ticket_select_v6"
        )
        select.callback = self.create_ticket
        self.add_item(select)

    async def create_ticket(self, interaction: Interaction):
        value = interaction.data["values"][0]
        label = next((opt.label for opt in self.children[0].options if opt.value == value), value)

        guild = interaction.guild
        user = interaction.user

        config = load_ticket_config().get(str(guild.id), {})
        category_id = config.get("ticket_category_id")

        existing = [ch for ch in guild.text_channels if ch.name.startswith("ticket-")]
        ticket_number = len(existing) + 1
        ticket_name = f"ticket-{ticket_number:05d}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True, manage_channels=True),
        }

        if category_id:
            category = guild.get_channel(category_id)
            if isinstance(category, discord.CategoryChannel):
                channel = await category.create_text_channel(
                    name=ticket_name, 
                    topic=f"Ticket: {label} | Opened by {user}", 
                    overwrites=overwrites
                )
            else:
                channel = await guild.create_text_channel(name=ticket_name, topic=..., overwrites=overwrites)
        else:
            channel = await guild.create_text_channel(name=ticket_name, topic=..., overwrites=overwrites)

        embed = discord.Embed(
            title=f"✦ VOID SUPPORT TERMINAL ✦ – {label}",
            description=f"{user.mention}, thank you for opening a ticket!\n\n**Please describe your issue in detail.**\nA staff member will assist you shortly.",
            color=0x71368A
        )
        embed.set_footer(text="VOID SPACE • Official Ticket System")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1461984553953657004/1472633716307263628/Add_a_heading.jpg")

        await channel.send(embed=embed, content=user.mention)

        close_view = CloseTicketView()
        await channel.send("**Click below to close this ticket**", view=close_view)

        await interaction.response.send_message(f"✅ Ticket created → {channel.mention}", ephemeral=True)


# ================================================
#  Close Ticket System (Unchanged)
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
        await interaction.response.send_message(embed=embed, view=confirm_view, ephemeral=False)


class ConfirmCloseView(View):
    def __init__(self, channel: discord.TextChannel):
        super().__init__(timeout=180)
        self.channel = channel

    @discord.ui.button(label="Send Transcript", style=discord.ButtonStyle.blurple, emoji="📜")
    async def send_transcript(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ Only staff can send transcripts.", ephemeral=True)
            return

        transcript_channel = interaction.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
        if not transcript_channel:
            await interaction.response.send_message("❌ Transcript channel not found.", ephemeral=True)
            return

        messages = []
        async for msg in self.channel.history(limit=100):
            time = msg.created_at.strftime("%H:%M")
            messages.append(f"[{time}] {msg.author}: {msg.content}")

        transcript_text = "\n".join(reversed(messages))

        await transcript_channel.send(
            f"**Transcript for {self.channel.name}**\nClosed by {interaction.user.mention}\n\n"
            f"```{transcript_text}```"
        )

        await interaction.response.send_message("📜 Transcript sent!", ephemeral=True)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="❌")
    async def yes_close(self, interaction: Interaction, button: Button):
        await interaction.response.defer()
        try:
            await self.channel.delete(reason=f"Ticket closed by {interaction.user}")
        except Exception as e:
            await interaction.followup.send(f"Failed to close: {e}", ephemeral=True)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.green, emoji="✅")
    async def cancel(self, interaction: Interaction, button: Button):
        await interaction.response.send_message("Cancelled.", ephemeral=True, delete_after=10)
        self.stop()


# ================================================
#  Commands
# ================================================
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ticketpanel")
    @commands.has_permissions(administrator=True)
    async def ticketpanel(self, ctx):
        embed = discord.Embed(
            title="✦ VOID SUPPORT TERMINAL ✦",
            description="Use this ticket to purchase COC accounts\nor access VOID-approved services.",
            color=0x71368A
        )
        embed.set_footer(text="VOID SPACE OFFICIAL TICKET TOOL")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1461984553953657004/1472633716307263628/Add_a_heading.jpg")

        view = PersistentTicketView()
        await ctx.send(embed=embed, view=view)

    @commands.command(name="setticketcategory")
    @commands.has_permissions(administrator=True)
    async def setticketcategory(self, ctx, category: discord.CategoryChannel):
        config = load_ticket_config()
        guild_id = str(ctx.guild.id)
        if guild_id not in config:
            config[guild_id] = {}
        config[guild_id]["ticket_category_id"] = category.id
        save_ticket_config(config)
        await ctx.send(f"✅ New tickets will now be created in category: **{category.name}**")

    @commands.command(name="close")
    async def close(self, ctx):
        if not ctx.channel.name.startswith("ticket-"):
            return await ctx.send("❌ This command can only be used inside a ticket channel.", delete_after=10)

        is_staff = ctx.author.guild_permissions.manage_channels
        is_creator = ctx.author.mention in (ctx.channel.topic or "")

        if not (is_staff or is_creator):
            return await ctx.send("❌ Only the ticket creator or staff can close this ticket.", delete_after=8)

        confirm_view = ConfirmCloseView(ctx.channel)
        embed = discord.Embed(
            title="Are you sure you want to close this ticket?",
            description="This ticket will be completely removed after closing.",
            color=0x71368A
        )
        await ctx.send(embed=embed, view=confirm_view)


async def setup(bot):
    await bot.add_cog(Tickets(bot))
