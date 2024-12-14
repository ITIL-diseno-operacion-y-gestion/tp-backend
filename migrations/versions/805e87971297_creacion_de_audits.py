"""creacion de audits

Revision ID: 805e87971297
Revises: ca990995234a
Create Date: 2024-11-04 01:31:10.783704

"""

from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import JSON
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "805e87971297"
down_revision: Union[str, None] = "ca990995234a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "auditorias",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("clase_entidad", sa.String(), nullable=True),
        sa.Column("id_entidad", sa.String(), nullable=True),
        sa.Column("fecha_de_accion", sa.DateTime(), nullable=True),
        sa.Column("accion", sa.String(), nullable=True),
        sa.Column("estado_anterior", JSON(), nullable=True),
        sa.Column("estado_nuevo", JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("auditorias")
