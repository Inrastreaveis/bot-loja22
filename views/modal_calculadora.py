import discord

from config import VIP_ROLE
from views.confirmar_pedido import ConfirmarPedido
from database.vip import pode_usar, obter_usos

DESCONTO_VIP = 0.07


class CalculadoraRobux(discord.ui.Modal, title="🧮 Calculadora de Robux"):

    robux = discord.ui.TextInput(
        label="Quantidade de Robux",
        placeholder="Ex: 1600",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):

        try:
            quantidade = int(self.robux.value)

            if quantidade <= 0:
                return await interaction.response.send_message(
                    "❌ Informe uma quantidade válida.",
                    ephemeral=True
                )

        except ValueError:
            return await interaction.response.send_message(
                "❌ Informe apenas números.",
                ephemeral=True
            )

        # ==========================
        # TABELA DE PREÇOS
        # ==========================
        milhares = quantidade // 1000
        restante = quantidade % 1000
        valor = (milhares * 27) + (restante * 0.03)

        vip = interaction.user.get_role(VIP_ROLE)
        pode_desconto = False

        if vip:
            usos = await obter_usos(interaction.user.id)
            pode_desconto = await pode_usar(interaction.user.id)

        embed = discord.Embed(
            title="🧮 Calculadora Campany",
            color=0x5865F2
        )

        embed.add_field(
            name="💎 Robux",
            value=f"{quantidade:,}".replace(",", "."),
            inline=False
        )

        desconto = 0
        total = valor

        if vip and pode_desconto:

            desconto = valor * DESCONTO_VIP
            total = valor - desconto

            embed.add_field(
                name="👑 Cliente VIP",
                value="✅ 7% de desconto aplicado.",
                inline=False
            )

            embed.add_field(
                name="💵 Valor Original",
                value=f"R$ {valor:.2f}".replace(".", ","),
                inline=True
            )

            embed.add_field(
                name="🏷️ Desconto",
                value=f"R$ {desconto:.2f}".replace(".", ","),
                inline=True
            )

            embed.add_field(
                name="💚 Total",
                value=f"R$ {total:.2f}".replace(".", ","),
                inline=False
            )

        elif vip:

            embed.add_field(
                name="👑 Cliente VIP",
                value="⚠️ Você já utilizou seus 2 descontos deste mês.",
                inline=False
            )

            embed.add_field(
                name="💰 Total",
                value=f"R$ {valor:.2f}".replace(".", ","),
                inline=False
            )

        else:

            embed.add_field(
                name="💰 Total",
                value=f"R$ {valor:.2f}".replace(".", ","),
                inline=False
            )

        await interaction.response.send_message(
            embed=embed,
            view=ConfirmarPedido(
                robux=quantidade,
                valor=round(total, 2),
                vip=vip is not None,
                desconto_aplicado=vip is not None and pode_desconto
            ),
            ephemeral=True
        )
