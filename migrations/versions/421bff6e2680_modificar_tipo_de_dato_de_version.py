"""modificar_tipo_de_dato_de_version

Revision ID: 421bff6e2680
Revises: f99ac6cf8f44
Create Date: 2024-10-14 19:42:33.806666

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "421bff6e2680"
down_revision: Union[str, None] = "7941d8eaedbb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("articulos", "version", type_=sa.Float, nullable=True)


def downgrade() -> None:
    op.alter_column("articulos", "version", type_=sa.Integer, nullable=False)
