"""elimino_estado_anterior_de_audits

Revision ID: 7856b6e36147
Revises: 7b8efbb17cbf
Create Date: 2024-11-29 22:36:40.473569

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "7856b6e36147"
down_revision: Union[str, None] = "7b8efbb17cbf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("auditorias", "estado_anterior")


def downgrade() -> None:
    op.add_column(
        "auditorias",
        sa.Column("estado_anterior", sa.String(50), nullable=True),
    )
