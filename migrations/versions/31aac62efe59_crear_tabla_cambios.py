"""crear_tabla_cambios

Revision ID: 31aac62efe59
Revises: 05a944b76ed9
Create Date: 2024-10-25 23:16:22.293451

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "31aac62efe59"
down_revision: Union[str, None] = "05a944b76ed9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cambios",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fecha_de_creacion", sa.DateTime, nullable=False),
        sa.Column(
            "id_solicitante", sa.Integer, sa.ForeignKey("usuarios.id"), nullable=False
        ),
        sa.Column("estado", sa.String(50), nullable=False),
        sa.Column("motivo_de_implementacion", sa.String(50), nullable=False),
        sa.Column("descripcion", sa.String(50), nullable=False),
        sa.Column("prioridad", sa.String(50), nullable=False),
        sa.Column("categoria", sa.String(50), nullable=False),
        sa.Column("impacto", sa.String(50), nullable=False),
        sa.Column("fecha_de_implementacion", sa.DateTime, nullable=False),
        sa.Column("horas_necesarias", sa.Float, nullable=False),
        sa.Column("costo_estimado", sa.Float, nullable=False),
        sa.Column("riesgos_asociados", sa.String(50), nullable=False),
    )
    op.create_table(
        "articulos_cambios",
        sa.Column(
            "id_articulo",
            sa.Integer,
            sa.ForeignKey("articulos.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "id_cambio",
            sa.Integer,
            sa.ForeignKey("cambios.id"),
            primary_key=True,
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("cambios")
    op.drop_table("articulos_cambios")
