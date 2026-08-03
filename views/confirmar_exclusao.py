import discord

from database.database import (
    get_db,
    remover_venda,
    atualizar_cliente_remocao,
    atualizar_staff_remocao
)


class ConfirmarExclusao(discord.ui.View):

    def __init__(self, venda_id: int):
        super().__init__(timeout=60)
        self.venda_id = venda_id

    @discord.ui.button(
        label="🗑️ Confirmar",
        style=discord.ButtonStyle.danger
    )
    async def confirmar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        db = await get_db()

        try:

            venda = await remover_venda(
                db,
                self.venda_id
            )

            if venda is None:

                return await interaction.response.edit_message(
                    content="❌ Essa venda não existe mais.",
                    embed=None,
                    view=None
                )

            await atualizar_cliente_remocao(
                db,
                venda["user_id"],
                venda["valor"],
                venda["robux"]
            )

            await atualizar_staff_remocao(
                db,
                venda["staff_id"],
                venda["valor"],
                venda["robux"]
            )

            await interaction.response.edit_message(
                content=f"✅ Venda **#{self.venda_id}** excluída com sucesso.",
                embed=None,
                view=None
            )

        finally:
            await db.close()

    @discord.ui.button(
        label="❌ Cancelar",
        style=discord.ButtonStyle.secondary
    )
    async def cancelar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.edit_message(
            content="❌ Operação cancelada.",
            embed=None,
            view=None
        )