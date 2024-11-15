"""add conformidad_resolucion to incidente

Revision ID: ca990995234a
Revises: 31aac62efe59
Create Date: 2024-11-02 19:48:11.518009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ca990995234a'
down_revision: Union[str, None] = '31aac62efe59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "incidentes",
        sa.Column("conformidad_resolucion", sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("incidentes", "conformidad_resolucion")