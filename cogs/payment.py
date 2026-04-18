import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
import json
import os

CONFIG_PATH = "/app/data/payment_methods.json"


# ---------------- CONFIG ---------------- #

def load_payment_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}


def save_payment_config(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)


# ---------------- PAYMENT BUTTON VIEW ---------------- #

class PaymentSelectView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def send_payment(self, interaction, method):
        data = load_payment_config().get(method, {})

        if not data:
            await interaction.response.send_message(
                f"❌ No setup for {method}. Use +paymentedit",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=data.get("title"),
            description=data.get("description"),
            color=0x71368A
        )

        if data.get("image"):
            embed.set_image(url=data["image"])

        if data.get("footer"):
            embed.set_footer(text=data["footer"])

        # ✅ PUBLIC MESSAGE
        await interaction.response.send_message(
            content=f"{interaction.user.mention} selected **{method.upper()}**",
            embed=embed
        )

    @discord.ui.button(label="UPI", emoji="<:upi:1493301499181138162>")
    async def upi(self, i, b):
        await self.send_payment(i, "upi")

    @discord.ui.button(label="Wise", emoji="<:wise:1493539277563498598>")
    async def wise(self, i, b):
        await self.send_payment(i, "wise")

    @discord.ui.button(label="PayPal", emoji="<:paypal:1493300900289052726>")
    async def paypal(self, i, b):
        await self.send_payment(i, "paypal")

    @discord.ui.button(label="Venmo", emoji="<:venmo:1493301369933795368>")
    async def venmo(self, i, b):
        await self.send_payment(i, "venmo")

    @discord.ui.button(label="Cash App", emoji="<:cashapp:1493301256830189729>")
    async def cashapp(self, i, b):
        await self.send_payment(i, "cashapp")

    @discord.ui.button(label="Zelle", emoji="<:zelle:1493302248434958459>")
    async def zelle(self, i, b):
        await self.send_payment(i, "zelle")

    @discord.ui.button(label="Crypto", emoji="<:crypto:1493300772912369736>")
    async def crypto(self, i, b):
        await self.send_payment(i, "crypto")


# ---------------- MAIN COMMANDS ---------------- #

class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="payment")
    @commands.has_permissions(manage_messages=True)
    async def payment(self, ctx):
        embed = discord.Embed(
            title="💳 Secure Payment Panel",
            description=(
                "⚠️ **Important:**\n"
                "Please verify all payment details carefully before completing your transaction. "
                "Payments sent to incorrect accounts cannot be reversed.\n\n"
                "📌 **Rules:**\n"
                "• Only use official payment methods listed here\n"
                "• Do not send payments without confirmation\n"
                "• Always keep your transaction proof\n\n"
                "🔒 **Security Notice:**\n"
                "• We never ask for passwords, OTPs, or private details\n"
                "• Staff will not DM you first for payments\n"
                "• Beware of impersonators\n\n"
                "For assistance, open a ticket or contact support.\n\n"
                "We appreciate your trust 🤍"
            ),
            color=0x71368A
        )

        await ctx.send(embed=embed, view=PaymentSelectView(self.bot))

        try:
            await ctx.message.delete()
        except:
            pass

    @commands.command(name="paymentedit")
    @commands.has_permissions(manage_messages=True)
    async def paymentedit(self, ctx):
        await ctx.send("Choose method to edit:", view=PaymentMethodSelectView(self.bot))


# ---------------- EDIT SELECT ---------------- #

class PaymentMethodSelectView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def open_editor(self, interaction, method):
        view = PaymentEditorView(self.bot, method)
        await interaction.response.send_message(
            embed=view.get_embed(),
            view=view,
            ephemeral=True
        )

    @discord.ui.button(label="UPI")
    async def upi(self, i, b): await self.open_editor(i, "upi")

    @discord.ui.button(label="Wise")
    async def wise(self, i, b): await self.open_editor(i, "wise")

    @discord.ui.button(label="PayPal")
    async def paypal(self, i, b): await self.open_editor(i, "paypal")

    @discord.ui.button(label="Venmo")
    async def venmo(self, i, b): await self.open_editor(i, "venmo")

    @discord.ui.button(label="Cash App")
    async def cashapp(self, i, b): await self.open_editor(i, "cashapp")

    @discord.ui.button(label="Zelle")
    async def zelle(self, i, b): await self.open_editor(i, "zelle")

    @discord.ui.button(label="Crypto")
    async def crypto(self, i, b): await self.open_editor(i, "crypto")


# ---------------- EDITOR VIEW ---------------- #

class PaymentEditorView(View):
    def __init__(self, bot, method):
        super().__init__(timeout=None)
        self.bot = bot
        self.method = method

        self.config = load_payment_config().get(method, {
            "title": f"{method.upper()} Payment",
            "description": "Enter payment details here.",
            "image": "",
            "footer": "VOID SPACE • Secure Payments"
        })

    def get_embed(self):
        embed = discord.Embed(
            title=self.config["title"],
            description=self.config["description"],
            color=0x71368A
        )

        if self.config["image"]:
            embed.set_image(url=self.config["image"])

        embed.set_footer(text=self.config["footer"])
        return embed

    async def update(self, interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.edit_original_response(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Title", emoji="✏️")
    async def title(self, i, b):
        await i.response.send_modal(TitleModal(self))

    @discord.ui.button(label="Description", emoji="📝")
    async def desc(self, i, b):
        await i.response.send_modal(DescriptionModal(self))

    @discord.ui.button(label="Image", emoji="🖼️")
    async def image(self, i, b):
        await i.response.send_modal(ImageModal(self))

    @discord.ui.button(label="Footer", emoji="🔻")
    async def footer(self, i, b):
        await i.response.send_modal(FooterModal(self))

    @discord.ui.button(label="Save", style=discord.ButtonStyle.green, emoji="💾")
    async def save(self, i, b):
        data = load_payment_config()
        data[self.method] = self.config
        save_payment_config(data)
        await i.response.send_message("✅ Saved!", ephemeral=True)


# ---------------- MODALS ---------------- #

class TitleModal(Modal, title="Edit Title"):
    text = TextInput(label="Title")

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.text.default = view.config["title"]

    async def on_submit(self, i):
        self.view.config["title"] = self.text.value
        await self.view.update(i)


class DescriptionModal(Modal, title="Edit Description"):
    text = TextInput(label="Description", style=discord.TextStyle.paragraph)

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.text.default = view.config["description"]

    async def on_submit(self, i):
        self.view.config["description"] = self.text.value
        await self.view.update(i)


class ImageModal(Modal, title="Image URL"):
    text = TextInput(label="URL")

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.text.default = view.config["image"]

    async def on_submit(self, i):
        self.view.config["image"] = self.text.value
        await self.view.update(i)


class FooterModal(Modal, title="Footer"):
    text = TextInput(label="Footer")

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.text.default = view.config["footer"]

    async def on_submit(self, i):
        self.view.config["footer"] = self.text.value
        await self.view.update(i)


# ---------------- SETUP ---------------- #

async def setup(bot):
    await bot.add_cog(Payment(bot))
    print("Payment system loaded")
