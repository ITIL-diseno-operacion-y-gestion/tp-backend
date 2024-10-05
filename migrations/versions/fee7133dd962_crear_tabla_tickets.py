"""crear_tabla_tickets

Revision ID: fee7133dd962
Revises: 8385f6d8e555
Create Date: 2024-10-04 23:58:20.988332

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fee7133dd962"
down_revision: Union[str, None] = "8385f6d8e555"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "id_usuario", sa.Integer, sa.ForeignKey("usuarios.id"), nullable=False
        ),
        sa.Column("fecha_de_alta", sa.String(50), nullable=False),
        sa.Column("forma_de_notificacion", sa.String(50), nullable=False),
        sa.Column("reportador", sa.String(50), nullable=False),
        sa.Column("usuarios_afectados", sa.String(50), nullable=False),
        sa.Column("servicios_afectados", sa.String(50), nullable=False),
        sa.Column("prioridad", sa.String(50), nullable=False),
        sa.Column("categoria", sa.String(50), nullable=False),
        sa.Column("informacion_adicional", sa.String(50), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("tickets")
    pass
