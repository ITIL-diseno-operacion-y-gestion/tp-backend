"""agregar_columna_estado_a_articulos

Revision ID: fb83ff82c21b
Revises: d22594b29d6d
Create Date: 2024-10-19 13:56:12.983150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fb83ff82c21b'
down_revision: Union[str, None] = 'd22594b29d6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "articulos",
        sa.Column("estado", sa.String(50), nullable=False, server_default="PLANEADO"),
    )

def downgrade() -> None:
    op.drop_column("articulos", "estado")