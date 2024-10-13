"""crear_tabla_problemas

Revision ID: e09aeb65d6d5
Revises: fee7133dd962
Create Date: 2024-10-12 22:52:07.401507

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e09aeb65d6d5"
down_revision: Union[str, None] = "fee7133dd962"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "problemas",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("prioridad", sa.String(50), nullable=False),
        sa.Column(
            "id_usuario", sa.Integer, sa.ForeignKey("usuarios.id"), nullable=False
        ),
        sa.Column("fecha_de_deteccion", sa.String(50), nullable=False),
        sa.Column("sintomas", sa.String(50), nullable=False),
        sa.Column("categoria", sa.String(50), nullable=False),
        sa.Column("estado", sa.String(50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("problemas")
