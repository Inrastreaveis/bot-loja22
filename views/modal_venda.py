import traceback
from datetime import datetime

import discord

from config import CLIENTE_ROLE, FUTURO_CLIENTE_ROLE

from database.database import (
    get_db,
    adicionar_cliente,
    registrar_venda,
    atualizar_cliente,
    adicionar_staff,
    atualizar_staff,
    atualizar_ticket_venda
)
from database.vip import obter_usos

class RegistrarVenda(discord.ui.Modal, title="💰 Registrar Venda"):
    robux = discord.ui.TextInput(
        label="Quantidade de Robux",
        placeholder="Ex: 800",
        required=True
    )

    valor = discord.ui.TextInput(
        label="Valor Pago (R$)",
        placeholder="Ex: 100",
        required=True
    )

    pagamento = discord.ui.TextInput(
        label="Forma de Pagamento",
        placeholder="PIX, Cartão, Mercado Pago...",
        required=True
    )

    observacao = discord.ui.TextInput(
        label="Observação",
        style=discord.TextStyle.paragraph,
        required=False
    )

    def __init__(self, robux: int = 0, valor: float = 0):
        super().__init__()

        if robux > 0:
            self.robux.default = str(robux)

        if valor > 0:
            self.valor.default = f"{valor:.2f}"

    async def on_submit(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        db = None

        try:

            cliente_id = int(interaction.channel.topic)

            robux = int(self.robux.value)

            valor = float(
                self.valor.value.replace(",", ".")
            )

            data = datetime.now().strftime("%d/%m/%Y %H:%M")

            db = await get_db()

            await adicionar_cliente(
                db,
                cliente_id,
                interaction.user.display_name
            )

            venda_id = await registrar_venda(
                db,
                cliente_id,
                interaction.user.id,
                valor,
                robux,
                self.pagamento.value,
                data,
                self.observacao.value
            )

            await atualizar_cliente(
                db,
                cliente_id,
                valor,
                robux,
                data
            )

            await adicionar_staff(
                db,
                interaction.user.id,
                interaction.user.display_name
            )

            await atualizar_staff(
                db,
                interaction.user.id,
                valor,
                robux
            )

            await atualizar_ticket_venda(
                db=db,
                canal_id=interaction.channel.id,
                staff_id=interaction.user.id,
                robux=robux,
                valor=valor
            )

            cliente = interaction.guild.get_member(cliente_id)
            usos_vip = await obter_usos(cliente_id)

            if cliente:

                cargo_futuro = interaction.guild.get_role(
                    FUTURO_CLIENTE_ROLE
                )

                cargo_cliente = interaction.guild.get_role(
                    CLIENTE_ROLE
                )

                if cargo_futuro:
                    await cliente.remove_roles(cargo_futuro)

                if cargo_cliente:
                    await cliente.add_roles(cargo_cliente)

            embed = discord.Embed(
                title="✅ Venda Registrada",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )

            embed.add_field(
                name="🆔 ID da Venda",
                value=f"#{venda_id}",
                inline=False
            )

            embed.add_field(
                name="👤 Cliente",
                value=cliente.mention if cliente else f"`{cliente_id}`",
                inline=False
            )

            embed.add_field(
                name="🪙 Robux",
                value=f"{robux:,}".replace(",", "."),
                inline=True
            )

            embed.add_field(
                name="💰 Valor",
                value=f"R$ {valor:.2f}".replace(".", ","),
                inline=True
            )

            embed.add_field(
                name="👑 VIP",
                value=f"{usos_vip}/2 utilizado(s)",
                inline=True
            )

            embed.add_field(
                name="💳 Pagamento",
                value=self.pagamento.value,
                inline=False
            )

            if self.observacao.value:

                embed.add_field(
                    name="📝 Observação",
                    value=self.observacao.value,
                    inline=False
                )

            embed.set_footer(
                text=f"Registrado por {interaction.user.display_name}"
            )

            await interaction.followup.send(
                embed=embed,
                ephemeral=True
            )

            embed_ticket = discord.Embed(
                title="✅ Venda Finalizada",
                description=(
                    "A venda foi registrada com sucesso.\n\n"
                    "Clique em **🔒 Fechar Ticket** para solicitar a avaliação do cliente."
                ),
                color=discord.Color.green()
            )

            await interaction.channel.send(embed=embed_ticket)

        except Exception as e:

            traceback.print_exc()

            if interaction.response.is_done():

                await interaction.followup.send(
                    f"❌ Erro ao registrar venda:\n```{e}```",
                    ephemeral=True
                )

            else:

                await interaction.response.send_message(
                    f"❌ Erro ao registrar venda:\n```{e}```",
                    ephemeral=True
                )

        finally:

            if db:
                await db.close()