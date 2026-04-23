import discord
from discord.ext import commands
from discord.ui import View, Button
from discord import Interaction

# ================================
# OPEN BUTTON VIEW
# ================================
class SecurePanelView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.blurple, emoji="🔐", custom_id="secure_open_ticket_v1")
    async def open_ticket(self, interaction: Interaction, button: Button):
        guild = interaction.guild
        user = interaction.user

        ticket_name = f"secure-{user.name}".lower()

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True),
        }

        channel = await guild.create_text_channel(name=ticket_name, overwrites=overwrites)

        # ================================
        # YOUR CUSTOM EMBED
        # ================================
        embed = discord.Embed(
            title="VOID SUPPORT — TICKET OPENED",
            description=(
                "Your request has been successfully registered.\n\n"
                "Please clearly provide:\n\n"
                "• <:Builder:1488534056554598452>  `Buyer & Seller usernames`\n"
                "• <:coc:1462053918740844709>  `(Acc/Clan) trade`\n"
                "• <:cashapp:1493301256830189729>  `Agreed price (exact amount)`\n"
                "• 💳  `Payment method`\n"
                "• 📎  `Screenshots/images of the deal`\n\n"
                "<a:arrowp:1462066642778329171> NEXT STEP\n\n"
                "• A VOID MM will be assigned shortly\n"
                "• No direct trades outside this system\n"
                "• No payments before MM verification\n"
                "• Failure to follow results in loss of protection"
            ),
            color=0xFF4FD8
        )

        embed.set_footer(text="VOID SPACE • Secure System")

        # ================================
        # CLOSE BUTTON
        # ================================
        close_view = CloseTicketView()

        await channel.send(
            content=f"{user.mention} <@&1461344309193347092>",
            embed=embed,
            view=close_view
        )

        await interaction.response.send_message(
            f"✅ Ticket created → {channel.mention}",
            ephemeral=True
        )

# ================================
# CLOSE BUTTON VIEW
# ================================
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id="secure_close_ticket_v1")
    async def close_ticket(self, interaction: Interaction, button: Button):
        await interaction.response.defer()
        await interaction.channel.delete(reason=f"Closed by {interaction.user}")

# ================================
# COG
# ================================
class SecureTickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def securepanel(self, ctx):
        embed = discord.Embed(
            description=(
                "<:Diamond:1461695789003706502> **VOID SECURE TERMINAL** <:Diamond:1461695789003706502>\n\n"
                "Select your category below to proceed:\n"
                "• Follow instructions after ticket creation\n"
                "• All secure trades must begin here."
            ),
            color=0xFF4FD8
        )

        embed.set_footer(text="VOID SPACE • Secure System")

        await ctx.send(embed=embed, view=SecurePanelView())

# ================================
# SETUP
# ================================
async def setup(bot):
    await bot.add_cog(SecureTickets(bot))
