import aiosqlite
from datetime import datetime

from database.database import DATABASE


async def atualizar_cliente(
    user_id: int,
    nome: str,
    valor: float
):

    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    async with aiosqlite.connect(str(DATABASE)) as db:

        cursor = await db.execute(
            """
            SELECT
                total_gasto,
                compras,
                primeira_compra,
                ultima_compra,
                maior_compra
            FROM clientes
            WHERE user_id = ?
            """,
            (user_id,)
        )

        cliente = await cursor.fetchone()

        if cliente is None:

            await db.execute(
                """
                INSERT INTO clientes (
                    user_id,
                    nome,
                    total_gasto,
                    robux_comprados,
                    compras,
                    primeira_compra,
                    ultima_compra,
                    maior_compra,
                    vip
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    nome,
                    valor,
                    0,
                    1,
                    data,
                    data,
                    valor,
                    "Bronze"
                )
            )

        else:

            total_gasto, compras, primeira, ultima, maior = cliente

            await db.execute(
                """
                UPDATE clientes
                SET
                    nome = ?,
                    total_gasto = ?,
                    compras = ?,
                    ultima_compra = ?,
                    maior_compra = ?
                WHERE user_id = ?
                """,
                (
                    nome,
                    total_gasto + valor,
                    compras + 1,
                    data,
                    max(maior, valor),
                    user_id
                )
            )

        await db.commit()