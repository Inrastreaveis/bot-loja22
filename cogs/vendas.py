import discord
from discord.ext import commands
from discord import app_commands

from views.modal_venda import RegistrarVenda


class Vendas(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="venda",
        description="Registrar uma venda de Robux."
    )
    async def venda(self, interaction: discord.Interaction):

        await interaction.response.send_modal(RegistrarVenda())


async def setup(bot):
    await bot.add_cog(Vendas(bot))