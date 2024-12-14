"""Agrego nombre a incidente

Revision ID: 14547c478132
Revises: f64534333474
Create Date: 2024-11-15 22:15:15.190592

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "14547c478132"
down_revision: Union[str, None] = "f64534333474"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "incidentes",
        sa.Column("nombre", sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("incidentes", "nombre")
