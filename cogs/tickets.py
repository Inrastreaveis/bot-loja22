import discord
from discord.ext import commands
from discord import app_commands

from views.painel import AbrirTicket
from utils.permissions import is_staff


class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="painel",
        description="Enviar painel de atendimento."
    )
    async def painel(self, interaction: discord.Interaction):

        if not is_staff(interaction):
            return await interaction.response.send_message(
                "❌ Você não possui permissão.",
                ephemeral=True
            )

        embed = discord.Embed(
            title="🛒 Atendimento Campany",
            description=(
                "Seja bem-vindo à **Campany**!\n\n"
                "Escolha uma das opções abaixo para abrir um atendimento.\n\n"
                "🛒 **Comprar Robux**\n"
                "👑 **Comprar Korblox**\n"
                "🧮 **Calcular Robux**\n"
                "🛠️ **Suporte Técnico**"
            ),
            color=discord.Color.blue()
        )

        embed.set_image(
            url="https://via.placeholder.com/1000x300.png?text=Campany"
        )

        embed.set_footer(
            text="Campany • Atendimento Automático"
        )

        await interaction.channel.send(
            embed=embed,
            view=AbrirTicket()
        )

        await interaction.response.send_message(
            "✅ Painel enviado com sucesso.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Tickets(bot))