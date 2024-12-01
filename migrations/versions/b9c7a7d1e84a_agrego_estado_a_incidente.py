"""agrego_estado_a_incidente

Revision ID: b9c7a7d1e84a
Revises: 7856b6e36147
Create Date: 2024-12-01 22:29:07.818416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b9c7a7d1e84a'
down_revision: Union[str, None] = '7856b6e36147'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "incidentes",
        sa.Column("estado", sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("incidentes", "estado")