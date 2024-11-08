"""agrego fecha de resolucion a problema

Revision ID: c3018cc1862b
Revises: e61b1d97c60a
Create Date: 2024-11-05 00:56:21.127015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c3018cc1862b'
down_revision: Union[str, None] = 'e61b1d97c60a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade() -> None:
    op.add_column(
        "problemas",
        sa.Column("fecha_de_resolucion", sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("probleas", "fecha_de_resolucion")
