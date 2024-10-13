"""crear_tabla_articulos

Revision ID: 97834b4cd94a
Revises: 3bb62d5a3c22
Create Date: 2024-09-27 20:52:13.983082

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "97834b4cd94a"
down_revision: Union[str, None] = "3bb62d5a3c22"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "articulos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.String(50), nullable=False),
        sa.Column("descripcion", sa.String(50), nullable=False),
        sa.Column("titular", sa.String(50), nullable=False),
        sa.Column("tipo", sa.String(50), nullable=False),
        sa.Column("info_fabricacion", sa.String(50), nullable=False),
        sa.Column("version", sa.Integer, nullable=False),
        sa.Column("localizacion", sa.String(50), nullable=False),
        sa.Column("fecha_de_alta", sa.String(50), nullable=False),
        sa.Column("relacion_items", sa.String(50), nullable=False),
        sa.Column("esta_activo", sa.BOOLEAN, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("articulos")
