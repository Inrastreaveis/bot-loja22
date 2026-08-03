import discord

from config import CATEGORY_TICKETS, STAFF_ROLE

from database.tickets import criar_ticket

from views.botoes import TicketButtons
from views.modal_calculadora import CalculadoraRobux


def criar_embed_ticket(
    usuario: discord.Member,
    categoria: str
):

    embed = discord.Embed(
        title="🎫 Ticket de Atendimento",
        description=(
            f"👤 **Cliente:** {usuario.mention}\n"
            f"📂 **Categoria:** {categoria}\n"
            f"📌 **Status:** 🟢 Aguardando atendimento\n"
            f"👮 **Atendente:** Nenhum"
        ),
        color=discord.Color.green()
    )

    if usuario.display_avatar:
        embed.set_thumbnail(
            url=usuario.display_avatar.url
        )

    embed.set_footer(
        text="Campany • Sistema de Tickets"
    )

    return embed


class AbrirTicket(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    async def criar_ticket(
        self,
        interaction: discord.Interaction,
        categoria_nome: str
    ):

        categoria = interaction.guild.get_channel(
            CATEGORY_TICKETS
        )

        if categoria is None:
            return await interaction.response.send_message(
                "❌ Categoria de tickets não encontrada.",
                ephemeral=True
            )

        for canal in categoria.text_channels:

            if canal.topic == str(interaction.user.id):

                return await interaction.response.send_message(
                    f"❌ Você já possui um ticket aberto: {canal.mention}",
                    ephemeral=True
                )

        overwrites = {

            interaction.guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            interaction.user:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    attach_files=True,
                    read_message_history=True
                ),

            interaction.guild.get_role(STAFF_ROLE):
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                ),

            interaction.guild.me:
                discord.PermissionOverwrite(
                    view_channel=True
                )
        }

        canal = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=categoria,
            overwrites=overwrites,
            topic=str(interaction.user.id)
        )

        await criar_ticket(
            canal_id=canal.id,
            user_id=interaction.user.id,
            categoria=categoria_nome,
            robux=0,
            valor=0,
            vip=False,
            desconto=0,
            desconto_aplicado=False
        )

        await canal.send(
            content=interaction.user.mention,
            embed=criar_embed_ticket(
                interaction.user,
                categoria_nome
            ),
            view=TicketButtons()
        )

        await interaction.response.send_message(
            f"✅ Ticket criado com sucesso: {canal.mention}",
            ephemeral=True
        )

    # ==========================
    # COMPRAR ROBUX
    # ==========================
    @discord.ui.button(
        label="Comprar Robux",
        emoji="🛒",
        style=discord.ButtonStyle.green,
        custom_id="comprar_robux"
    )
    async def comprar_robux(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(
            CalculadoraRobux()
        )

    # ==========================
    # COMPRAR KORBLOX
    # ==========================
    @discord.ui.button(
        label="Comprar Korblox",
        emoji="👑",
        style=discord.ButtonStyle.blurple,
        custom_id="comprar_korblox"
    )
    async def comprar_korblox(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.criar_ticket(
            interaction,
            "👑 Comprar Korblox"
        )

    # ==========================
    # CALCULADORA
    # ==========================
    @discord.ui.button(
        label="Calcular Robux",
        emoji="🧮",
        style=discord.ButtonStyle.gray,
        custom_id="calcular_robux"
    )
    async def calcular(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(
            CalculadoraRobux()
        )

    # ==========================
    # SUPORTE
    # ==========================
    @discord.ui.button(
        label="Suporte Técnico",
        emoji="🛠️",
        style=discord.ButtonStyle.red,
        custom_id="suporte_tecnico"
    )
    async def suporte(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.criar_ticket(
            interaction,
            "🛠️ Suporte Técnico"
        )