import discord

from config import CATEGORY_TICKETS, STAFF_ROLE

from database.tickets import criar_ticket

from views.botoes import TicketButtons


class ConfirmarPedido(discord.ui.View):

    def __init__(self, robux, valor, vip, desconto_aplicado):
        super().__init__(timeout=300)

        self.robux = robux
        self.valor = valor
        self.vip = vip
        self.desconto_aplicado = desconto_aplicado

    @discord.ui.button(
    label="✅ Confirmar Pedido",
    style=discord.ButtonStyle.green
)
    async def confirmar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        try:
            categoria = interaction.guild.get_channel(CATEGORY_TICKETS)

            if categoria is None:
                return await interaction.response.send_message(
                    "❌ Categoria não encontrada.",
                    ephemeral=True
                )

            for canal in categoria.text_channels:
                if canal.topic == str(interaction.user.id):
                    return await interaction.response.send_message(
                        "Você já possui um ticket.",
                        ephemeral=True
                    )

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    view_channel=False
                ),

                interaction.user: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    attach_files=True,
                    read_message_history=True
                ),

                interaction.guild.get_role(STAFF_ROLE): discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                ),

                interaction.guild.me: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    manage_channels=True,
                    manage_messages=True
                )
            }

            canal = await interaction.guild.create_text_channel(
                name=f"pedido-{interaction.user.name}",
                category=categoria,
                overwrites=overwrites,
                topic=str(interaction.user.id)
            )

            embed = discord.Embed(
                title="🎫 Ticket de Atendimento",
                description=(
                    f"👤 **Cliente:** {interaction.user.mention}\n"
                    f"📂 **Categoria:** Compra de Robux\n"
                    f"📌 **Status:** 🟢 Aguardando atendimento\n"
                    f"👮 **Atendente:** Nenhum"
                ),
                color=discord.Color.green()
            )

            embed.set_footer(text="Campany • Sistema de Atendimento")

            await canal.send(content=interaction.user.mention, embed=embed, view=TicketButtons())

            await criar_ticket(
                canal_id=canal.id,
                user_id=interaction.user.id,
                categoria="🛒 Compra de Robux",
                robux=self.robux,
                valor=self.valor,
                vip=self.vip,
                desconto=self.desconto_aplicado,
                desconto_aplicado=self.desconto_aplicado
            )

            await interaction.response.send_message(
                f"✅ Pedido confirmado!\n\nSeu ticket foi criado com sucesso: {canal.mention}",
                ephemeral=True
            )

        except Exception as e:
            import traceback
            traceback.print_exc()

            if not interaction.response.is_done():
                await interaction.response.send_message(f"Erro:\n```{e}```", ephemeral=True)

    @discord.ui.button(
        label="❌ Cancelar",
        style=discord.ButtonStyle.red
    )
    async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(content="❌ Pedido cancelado.", embed=None, view=self)