import discord
from config import STAFF_ROLE


def is_staff(interaction: discord.Interaction) -> bool:
    """Verifica se o usuário é administrador ou possui o cargo de Staff."""

    # Administrador do servidor
    if interaction.user.guild_permissions.administrator:
        return True

    # Dono do servidor
    if interaction.guild.owner_id == interaction.user.id:
        return True

    # Cargo da Staff
    cargo_staff = interaction.guild.get_role(STAFF_ROLE)

    if cargo_staff and cargo_staff in interaction.user.roles:
        return True

    return False