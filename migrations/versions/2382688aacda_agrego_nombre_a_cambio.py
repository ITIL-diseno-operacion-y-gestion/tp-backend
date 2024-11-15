"""Agrego nombre a Cambio

Revision ID: 2382688aacda
Revises: 4ed126135dfe
Create Date: 2024-11-15 22:37:52.243257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2382688aacda'
down_revision: Union[str, None] = '4ed126135dfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "cambios",
        sa.Column("nombre", sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("cambios", "nombre")