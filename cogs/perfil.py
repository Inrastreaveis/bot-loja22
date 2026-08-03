import discord

from discord import app_commands
from discord.ext import commands

from database.database import get_db, buscar_cliente
from database.vip import obter_usos


class Perfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="perfil",
        description="Mostra o perfil do cliente."
    )
    async def perfil(
        self,
        interaction: discord.Interaction,
        usuario: discord.Member = None
    ):

        if usuario is None:
            usuario = interaction.user

        db = await get_db()

        cliente = await buscar_cliente(
            db,
            usuario.id
        )

        if cliente is None:
            await db.close()

            return await interaction.response.send_message(
                "❌ Este usuário ainda não possui compras.",
                ephemeral=True
            )

        usos = await obter_usos(usuario.id)

        (
            user_id,
            nome,
            total_gasto,
            robux,
            compras,
            primeira,
            ultima,
            maior,
            vip
        ) = cliente

        embed = discord.Embed(
            title="👤 Perfil do Cliente",
            color=0x5865F2
        )

        embed.set_thumbnail(
            url=usuario.display_avatar.url
        )

        embed.add_field(
            name="💰 Total Gasto",
            value=f"R$ {total_gasto:.2f}",
            inline=True
        )

        embed.add_field(
            name="💎 Robux",
            value=f"{robux:,}".replace(",", "."),
            inline=True
        )

        embed.add_field(
            name="🛒 Compras",
            value=str(compras),
            inline=True
        )

        embed.add_field(
            name="📅 Primeira Compra",
            value=primeira or "Nenhuma",
            inline=False
        )

        embed.add_field(
            name="🕒 Última Compra",
            value=ultima or "Nenhuma",
            inline=False
        )

        embed.add_field(
            name="💵 Maior Compra",
            value=f"R$ {maior:.2f}",
            inline=True
        )

        embed.add_field(
            name="👑 VIP",
            value=vip,
            inline=True
        )

        embed.add_field(
            name="🎁 Descontos VIP",
            value=f"{usos}/2 usados",
            inline=True
        )

        embed.set_footer(
            text=f"ID: {usuario.id}"
        )

        await db.close()

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Perfil(bot))