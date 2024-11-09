"""agrego agente asignado a incidente

Revision ID: f64534333474
Revises: c3018cc1862b
Create Date: 2024-11-09 15:01:44.412577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f64534333474'
down_revision: Union[str, None] = 'c3018cc1862b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "incidentes",
        sa.Column("id_agente_asignado", sa.Integer, nullable=True),
    )


def downgrade() -> None:
    op.drop_column("incidentes", "id_agente_asignado")