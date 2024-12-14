"""Agrego nombre a Problema

Revision ID: 4ed126135dfe
Revises: 14547c478132
Create Date: 2024-11-15 22:26:17.209371

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4ed126135dfe"
down_revision: Union[str, None] = "14547c478132"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "problemas",
        sa.Column("nombre", sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("problemas", "nombre")
