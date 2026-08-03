import discord
from discord.ext import commands
from discord import app_commands

from database.database import get_db, buscar_cliente


class Clientes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="cliente",
        description="Mostra o perfil de um cliente."
    )
    async def cliente(
        self,
        interaction: discord.Interaction,
        usuario: discord.Member
    ):
        db = await get_db()

        cliente = await buscar_cliente(db, usuario.id)

        await db.close()

        if cliente is None:
            await interaction.response.send_message(
                "❌ Esse cliente ainda não possui compras.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="👤 Perfil do Cliente",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Nome",
            value=usuario.mention,
            inline=False
        )

        embed.add_field(
            name="💰 Total Gasto",
            value=f"R$ {cliente[2]:.2f}",
            inline=True
        )

        embed.add_field(
            name="🪙 Robux",
            value=str(cliente[3]),
            inline=True
        )

        embed.add_field(
            name="🛒 Compras",
            value=str(cliente[4]),
            inline=True
        )

        embed.add_field(
            name="💎 VIP",
            value=cliente[8],
            inline=True
        )

        embed.add_field(
            name="📅 Última compra",
            value=cliente[6] or "Nunca",
            inline=False
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Clientes(bot))