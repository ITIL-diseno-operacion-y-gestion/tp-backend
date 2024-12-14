"""eliminar campos de Incidente

Revision ID: 7b8efbb17cbf
Revises: 2382688aacda
Create Date: 2024-11-15 22:49:49.121612

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "7b8efbb17cbf"
down_revision: Union[str, None] = "2382688aacda"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("incidentes", "reportador")
    op.drop_column("incidentes", "usuarios_afectados")


def downgrade() -> None:
    op.add_column(
        "incidentes",
        sa.Column("reportador", sa.String(50), nullable=True),
    )

    op.add_column(
        "incidentes",
        sa.Column("usuarios_afectados", sa.String(50), nullable=True),
    )
