import discord
from discord.ext import commands
from discord.ui import View, Select, Button
from discord import SelectOption, Interaction

CATEGORY_ID = 1461296075376689279


# ================================
# SELECT MENU
# ================================
class TicketSelect(Select):
    def __init__(self, cog):
        self.cog = cog

        options = [
            SelectOption(label="Report a Scam", value="scam", emoji="<:scam:1496923057384587275>"),
            SelectOption(label="General Support", value="support", emoji="<:support:1496922968989892668>"),
            SelectOption(label="VOID Authorized MM", value="mm", emoji="<:voidspace:1461678340883873852>")
        ]

        super().__init__(
            placeholder="Select ticket reason",
            options=options,
            custom_id="secure_ticket_select_v2"
        )

    async def callback(self, interaction: Interaction):
        await self.cog.create_ticket(interaction)


# ================================
# PANEL VIEW
# ================================
class SecurePanelView(View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.add_item(TicketSelect(cog))


# ================================
# CLOSE CONFIRM VIEW
# ================================
class ConfirmCloseView(View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.red)
    async def yes(self, interaction: Interaction, button: Button):
        await interaction.response.defer()
        await interaction.channel.delete(reason=f"Closed by {interaction.user}")

    @discord.ui.button(label="No", style=discord.ButtonStyle.green)
    async def no(self, interaction: Interaction, button: Button):
        await interaction.response.send_message("Cancelled.", ephemeral=True)


# ================================
# CLOSE BUTTON
# ================================
class CloseButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.red,
        emoji="🔒",
        custom_id="secure_close_ticket_btn"
    )
    async def close_ticket(self, interaction: Interaction, button: Button):
        await interaction.response.send_message(
            "Are you sure you want to close this ticket?",
            view=ConfirmCloseView(),
            ephemeral=True
        )


# ================================
# MAIN COG
# ================================
class SecureTickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ================================
    # CREATE TICKET LOGIC
    # ================================
    async def create_ticket(self, interaction: Interaction):
        try:
            guild = interaction.guild
            user = interaction.user
            reason = interaction.data.get("values", ["unknown"])[0]

            category = guild.get_channel(CATEGORY_ID)

            if category is None:
                return await interaction.response.send_message(
                    "❌ Ticket category not found.",
                    ephemeral=True
                )

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True),
            }

            channel = await category.create_text_channel(
                name=f"ticket-{user.name}".lower(),
                overwrites=overwrites,
                topic=f"UserID:{user.id} | Reason:{reason}"
            )

            # ================================
            # SCAM + SUPPORT (SIMPLE EMBED)
            # ================================
            if reason in ["scam", "support"]:

                outside_text = f"{user.mention}"

                inside_embed = discord.Embed(
                    description=(
                        f"{user.mention}, thank you for opening a ticket!\n\n"
                        "**Please describe your issue in detail.**\n"
                        "A staff member will assist you shortly."
                    ),
                    color=0x8A2BE2
                )

            # ================================
            # MM TICKETS (FULL FORMAT)
            # ================================
            else:

                outside_text = f"{user.mention}, thank you for opening a ticket!"

                inside_embed = discord.Embed(
                    title="VOID SUPPORT — MM REQUEST",
                    description=(
                        f"{user.mention}, thank you for opening a ticket!\n\n"
                        "**Please wait for a VOID MM to respond.**\n"
                        "A staff member will assist you shortly."
                    ),
                    color=0x8A2BE2
                )

            # ================================
            # SEND MESSAGES
            # ================================
            await channel.send(outside_text)
            await channel.send(embed=inside_embed, view=CloseButtonView())

            await interaction.response.send_message(
                f"✅ Ticket created → {channel.mention}",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )


    # ================================
    # PANEL COMMAND
    # ================================
    @commands.command()
    async def securepanel(self, ctx):
        embed = discord.Embed(
            description=(
                "<:Diamond:1461695789003706502> **VOID SECURE TERMINAL** <:Diamond:1461695789003706502>\n\n"
                "Select your category below to proceed:\n"
                "• Follow instructions after ticket creation\n"
                "• All secure trades must begin here."
            ),
            color=0x8A2BE2
        )

        embed.set_image(url="https://cdn.discordapp.com/attachments/1461984553953657004/1472633716307263628/Add_a_heading.jpg")
        embed.set_footer(text="VOID SPACE • Secure System")

        await ctx.send(embed=embed, view=SecurePanelView(self))


    # ================================
    # CLOSE COMMAND
    # ================================
    @commands.command()
    async def cl(self, ctx):
        if "ticket-" not in ctx.channel.name:
            return await ctx.send("❌ Use this inside a ticket.")

        await ctx.send(
            "Are you sure you want to close this ticket?",
            view=ConfirmCloseView()
        )


# ================================
# SETUP
# ================================
async def setup(bot):
    await bot.add_cog(SecureTickets(bot))
